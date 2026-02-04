from movie_recs import *
import networkx as nx
import gravis as gv
from collections import defaultdict

username = "ljstelzer8"

# Fetch data
last50 = get_last_logged(username, 50)
movie_actors = {}  # movie -> list of actors
actor_movies = defaultdict(list)  # actor -> list of movies

for movie in last50:
    actors = get_actors_in_movie(movie)
    movie_actors[movie] = actors
    for actor in actors:
        actor_movies[actor].append(movie)

# Build graph: movies are nodes, shared actors create edges
G = nx.Graph()
G.add_nodes_from(last50)

# Add edges between movies that share actors
for actor, movies in actor_movies.items():
    if len(movies) > 1:
        for i in range(len(movies)):
            for j in range(i + 1, len(movies)):
                if G.has_edge(movies[i], movies[j]):
                    G[movies[i]][movies[j]]['weight'] += 1
                    G[movies[i]][movies[j]]['actors'].append(actor)
                else:
                    G.add_edge(movies[i], movies[j], weight=1, actors=[actor])

# Print graph stats
print(f"\nGraph Statistics:")
print(f"  Movies (nodes): {G.number_of_nodes()}")
print(f"  Connections (edges): {G.number_of_edges()}")

# Print connections
print(f"\nMovie connections (shared actors):")
for u, v, data in sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True):
    print(f"  {u} <-> {v}")
    print(f"    Shared actors ({data['weight']}): {', '.join(data['actors'])}")

# Prepare graph for gravis visualization
# Add node labels and hover info
for node in G.nodes():
    G.nodes[node]['label'] = node
    actors_list = movie_actors.get(node, [])
    G.nodes[node]['hover'] = f"Actors: {', '.join(actors_list[:5])}{'...' if len(actors_list) > 5 else ''}"

# Add edge hover info showing shared actors
for u, v, data in G.edges(data=True):
    G[u][v]['hover'] = f"Shared actors: {', '.join(data['actors'])}"
    G[u][v]['size'] = data['weight']  # Edge thickness based on shared actor count

# Create interactive visualization with gravis
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

# Save to HTML file
html_filepath = "movie_graph_interactive.html"
fig.export_html(html_filepath)
print(f"\nInteractive graph saved to: {html_filepath}")

# Display in Jupyter if running in notebook, otherwise just save
try:
    from IPython import get_ipython
    if get_ipython() is not None:
        fig
except:
    print("Open the HTML file in a browser to view the interactive graph.")
