import os
import requests
from dotenv import load_dotenv
from .find_similar import get_movie_id

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

def get_actors_in_movie(movie_name):
    """
    Retrieve a list of actors (cast members) for a given movie.
    
    Parameters:
        movie_name (str): The name of the movie.
        
    Returns:
        list[str]: A list of actor names (top 10).
    """
    movie_id = get_movie_id(movie_name)
    
    if not movie_id:
        print(f"Movie '{movie_name}' not found.")
        return []
        
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
    response = requests.get(url).json()
    
    actors = []
    # Get top 10 cast members
    for cast in response.get('cast', [])[:10]:
        actors.append(cast['name'])
        
    return actors
