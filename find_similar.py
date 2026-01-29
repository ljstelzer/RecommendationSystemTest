import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

def get_movie_id(movie_name):
    """
    Search for a movie by name and return the ID of the first result.

    Parameters:
        movie_name (str): The name of the movie to search for.

    Returns:
        int or None: The TMDB ID of the first matching movie, or None if no results found.
    """
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    response = requests.get(url).json()
    
    if response['results']:
        # Return the first match
        return response['results'][0]['id']
    return None

def get_similar_movies(movie_name):
    """
    Find similar movies to the given movie name.

    Parameters:
        movie_name (str): The name of the movie to find similarities for.

    Returns:
        list[str]: A list of titles of similar movies.
    """
    movie_id = get_movie_id(movie_name)
    
    if not movie_id:
        print(f"Movie '{movie_name}' not found.")
        return []
    
    # Get Similar Movies directly
    url_similar = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={api_key}"
    results = requests.get(url_similar).json()
    
    movie_titles = [m['title'] for m in results['results']]
    return movie_titles

if __name__ == "__main__":
    # Example usage
    target_movie = "Fight Club"
    similar_movies = get_similar_movies(target_movie)
    
    print(f"Movies similar to {target_movie}:")
    for title in similar_movies[:5]:
        print(f"- {title}")
