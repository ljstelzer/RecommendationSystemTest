import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

def get_actor_id(actor_name):
    """
    Search for an actor by name and return the ID of the first result.

    Parameters:
        actor_name (str): The name of the actor to search for.

    Returns:
        int or None: The TMDB ID of the first matching actor, or None if no results found.
    """
    url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}"
    response = requests.get(url).json()

    if response['results']:
        return response['results'][0]['id']
    return None

def get_movies_by_actor(actor_name):
    """
    Find movies featuring the given actor.

    Parameters:
        actor_name (str): The name of the actor to find movies for.

    Returns:
        list[str]: A list of titles of movies featuring the actor.
    """
    actor_id = get_actor_id(actor_name)
    
    if not actor_id:
        print(f"Actor '{actor_name}' not found.")
        return []
    
    print(f"Found Actor ID: {actor_id} for '{actor_name}'")
    
    # Discover movies with this actor
    url_discover = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_cast={actor_id}&sort_by=popularity.desc"
    results = requests.get(url_discover).json()
    
    movie_titles = [m['title'] for m in results['results']]
    return movie_titles

if __name__ == "__main__":
    # Example usage
    target_actor = "Brad Pitt"
    movies = get_movies_by_actor(target_actor)
    
    print(f"Movies with {target_actor}:")
    for title in movies[:5]:
        print(f"- {title}")
