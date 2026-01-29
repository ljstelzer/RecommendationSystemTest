import requests
from bs4 import BeautifulSoup

def get_last_logged(username, num_movies=10):
    """
    Scrape a Letterboxd user's RSS feed to retrieve the N most recently logged movies.
    
    Parameters:
        username (str): The Letterboxd username.
        num_movies (int): The number of movies to retrieve. Note: RSS feed is limited to the last 50 items.
        
    Returns:
        list[str]: A list of movie titles.
    """
    url = f"https://letterboxd.com/{username}/rss/"
    print(f"Fetching last {num_movies} logged movies for user: {username} via RSS...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: Unable to fetch page (Status code: {response.status_code})")
            return []

        # Use 'xml' parser for RSS feeds
        soup = BeautifulSoup(response.content, 'xml')
        
        items = soup.find_all('item')
        
        if not items:
            print("No diary entries found in RSS feed.")
            return []
            
        if num_movies > 50:
            print("Warning: Letterboxd RSS feed is limited to the last 50 items.")

        movies = []
        count = 0
        
        for item in items:
            if count >= num_movies:
                break
            
            # The 'letterboxd:filmTitle' tag contains the accurate title
            # Note: bs4 with xml parser lowercases tag names usually, but lxml keeps case or namespaces handling varies.
            # We can try finding by tag name ignoring namespace if needed, or precise name.
            # Using find() with specific tag name is usually robust in bs4 xml mode.
            
            title_tag = item.find('letterboxd:filmTitle')
            
            if title_tag:
                movies.append(title_tag.text)
                count += 1
            else:
                # Fallback to parsing the <title> tag "Movie Name, Year - Rating"
                full_title = item.title.text
                # Simple heuristic: split by comma to get title, though this fails for titles with commas.
                # Better to trust the namespaced tag which we know exists in Letterboxd feeds.
                pass
                
        return movies

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    target_user = "ljstelzer8"
    limit = 5
    recent_movies = get_last_logged(target_user, limit)
    
    print(f"\nLast {limit} movies logged by {target_user}:")
    for movie in recent_movies:
        print(f"- {movie}")
