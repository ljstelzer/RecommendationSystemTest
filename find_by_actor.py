import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

movie_id = 550 # Fight Club

# 1. Get Credits to find Cast IDs
url_credits = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
credits = requests.get(url_credits).json()

# Find Brad Pitt's ID
actor_id = None
for cast_member in credits['cast']:
    if cast_member['name'] == "Brad Pitt":
        actor_id = cast_member['id']
        break

if actor_id:
    print(f"Found Brad Pitt (ID: {actor_id})")
    
    # 2. Discover movies with this actor
    url_discover = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_cast={actor_id}&sort_by=popularity.desc"
    results = requests.get(url_discover).json()

    for m in results['results'][:5]:
        print(f"- {m['title']}")
