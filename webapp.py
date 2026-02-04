from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from collections import defaultdict
import networkx as nx
import gravis as gv

from movie_recs import get_last_logged, get_actors_in_movie

app = FastAPI(title="Letterboxd Movie Graph")
templates = Jinja2Templates(directory="templates")


def build_movie_graph(username: str, num_movies: int = 50):
    """Fetch movies and build a graph based on shared actors."""
    movies = get_last_logged(username, num_movies)

    if not movies:
        return None, 0, 0

    movie_actors = {}
    actor_movies = defaultdict(list)

    for movie in movies:
        actors = get_actors_in_movie(movie)
        movie_actors[movie] = actors
        for actor in actors:
            actor_movies[actor].append(movie)

    # Build graph
    G = nx.Graph()
    G.add_nodes_from(movies)

    for actor, actor_movie_list in actor_movies.items():
        if len(actor_movie_list) > 1:
            for i in range(len(actor_movie_list)):
                for j in range(i + 1, len(actor_movie_list)):
                    m1, m2 = actor_movie_list[i], actor_movie_list[j]
                    if G.has_edge(m1, m2):
                        G[m1][m2]['weight'] += 1
                        G[m1][m2]['actors'].append(actor)
                    else:
                        G.add_edge(m1, m2, weight=1, actors=[actor])

    # Add node/edge metadata for gravis with Letterboxd colors
    for node in G.nodes():
        G.nodes[node]['label'] = node
        G.nodes[node]['color'] = '#ff8000'  # Letterboxd orange
        actors_list = movie_actors.get(node, [])
        G.nodes[node]['hover'] = f"Actors: {', '.join(actors_list[:5])}{'...' if len(actors_list) > 5 else ''}"

    for u, v, data in G.edges(data=True):
        G[u][v]['hover'] = f"Shared actors: {', '.join(data['actors'])}"
        G[u][v]['size'] = data['weight']
        G[u][v]['color'] = '#40bcf4'  # Letterboxd blue

    return G, len(movies), G.number_of_edges()


def generate_graph_html(G):
    """Generate gravis HTML for embedding with Letterboxd colors."""
    fig = gv.d3(
        G,
        graph_height=600,
        node_size_factor=1.5,
        node_label_size_factor=0.7,
        edge_size_factor=0.5,
        use_node_size_normalization=True,
        node_hover_neighborhood=True,
        show_menu=True,
        show_details=True,
    )
    return fig.to_html_partial()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/graph", response_class=HTMLResponse)
async def show_graph(request: Request, username: str = Form(...)):
    username = username.strip()

    if not username:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Please enter a username"
        })

    try:
        G, num_movies, num_edges = build_movie_graph(username)

        if G is None or num_movies == 0:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": f"No movies found for user '{username}'. Check the username and try again."
            })

        graph_html = generate_graph_html(G)

        return templates.TemplateResponse("graph.html", {
            "request": request,
            "username": username,
            "num_movies": num_movies,
            "num_edges": num_edges,
            "graph_html": graph_html,
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Error fetching data: {str(e)}"
        })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
