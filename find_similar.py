import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

movie_id = 550 # Fight Club

# Get Similar Movies directly
url_similar = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={api_key}"
results = requests.get(url_similar).json()

print(f"Movies similar to Fight Club:")
for m in results['results'][:5]:
    print(f"- {m['title']}")
