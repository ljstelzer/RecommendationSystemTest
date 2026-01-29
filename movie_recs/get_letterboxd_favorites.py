import requests
from bs4 import BeautifulSoup

def get_user_favorites(username):
    """
    Fetch the favorite movies of a Letterboxd user.

    Parameters:
        username (str): The Letterboxd username.

    Returns:
        list[str]: A list of favorite movie titles (with year if available).
    """
    url = f"https://letterboxd.com/{username}/"
    print(f"Fetching favorites for user: {username}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: Unable to fetch page (Status code: {response.status_code})")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the section with id="favourites"
        fav_section = soup.find(id="favourites") 
        
        if not fav_section:
            print("Could not find 'Favourites' section. The user might not have any favorites listed.")
            return []

        # Find all list items with class that indicates a film poster
        posters = fav_section.find_all("div", class_="poster")
        
        if not posters:
            print("No favorite movies found in the section.")
            return []

        favorites = []
        for poster in posters:
            film_name = poster.get('data-film-name')
            film_year = poster.get('data-film-release-year')
            
            if film_name:
                title_entry = film_name
                if film_year:
                    title_entry += f" ({film_year})"
                favorites.append(title_entry)
            else:
                img = poster.find('img')
                if img and img.get('alt'):
                    favorites.append(img.get('alt'))
        
        return favorites

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    target_user = "ljstelzer8" 
    favorites = get_user_favorites(target_user)
    
    print(f"\n{target_user}'s Favorite Movies:")
    for movie in favorites:
        print(f"- {movie}")
