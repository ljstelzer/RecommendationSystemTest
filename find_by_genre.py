import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

def get_genre_map():
    """
    Fetch all movie genres from TMDB and return a dictionary mapping 
    lowercase genre names to their IDs.

    Returns:
        dict: A dictionary where keys are lowercase genre names (str) and values are genre IDs (int).
    """
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}"
    response = requests.get(url).json()
    
    genre_map = {}
    for genre in response.get('genres', []):
        genre_map[genre['name'].lower()] = genre['id']
    return genre_map

def get_movies_by_genre(genre_names):
    """
    Find movies that match ALL of the given genre names.

    Parameters:
        genre_names (list[str]): A list of genre names to filter by (e.g. ["Action", "Thriller"]).

    Returns:
        list[str]: A list of titles of movies matching all specified genres.
    """
    genre_map = get_genre_map()
    valid_ids = []
    found_names = []
    
    for name in genre_names:
        key = name.lower()
        if key in genre_map:
            valid_ids.append(str(genre_map[key]))
            found_names.append(name)
        else:
            print(f"Warning: Genre '{name}' not found.")
            
    if not valid_ids:
        print("No valid genres found.")
        return []
        
    genre_string = ",".join(valid_ids)
    print(f"Searching for movies with genres: {', '.join(found_names)} (IDs: {genre_string})")
    
    # Discover movies with these genres
    # with_genres uses comma for AND logic (must have all genres)
    url_discover = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_string}&sort_by=popularity.desc"
    results = requests.get(url_discover).json()
    
    movie_titles = [m['title'] for m in results['results']]
    return movie_titles

if __name__ == "__main__":
    # Example usage
    target_genres = ["Drama", "Thriller"]
    movies = get_movies_by_genre(target_genres)
    
    print(f"Movies in genres {target_genres}:")
    for title in movies[:5]:
        print(f"- {title}")
