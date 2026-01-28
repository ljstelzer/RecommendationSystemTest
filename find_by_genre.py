import os
import requests
import letterboxdpy
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

# 1. Get Details for Fight Club (ID 550) to find its genres
movie_id = 550
url_details = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
movie_data = requests.get(url_details).json()

# Extract genre IDs (e.g., Drama=18)
genre_ids = [str(g['id']) for g in movie_data['genres']]
genre_string = ",".join(genre_ids)

# Extract genre names for display
genre_names = [g['name'] for g in movie_data['genres']]
genre_names_string = ", ".join(genre_names)

print(f"Finding movies with genres: {genre_names_string}")

# 2. Discover movies with these genres
# with_genres uses comma for AND logic (must have all genres)
url_discover = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_string}&sort_by=popularity.desc"
results = requests.get(url_discover).json()

for m in results['results'][:5]:
    print(f"- {m['title']}")
