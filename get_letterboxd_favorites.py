import requests
from bs4 import BeautifulSoup

def get_user_favorites(username):
    url = f"https://letterboxd.com/{username}/"
    print(f"Fetching favorites for user: {username}...")
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Unable to fetch page (Status code: {response.status_code})")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Letterboxd favorites are usually in a section with id 'favourites'
        # The films are typically li items with class 'poster-container' or similar inside the user-poster-list
        
        # Look for the section with id="favourites"
        fav_section = soup.find(id="favourites") 
        
        if not fav_section:
            # Fallback/Check: Sometimes it might just be the top 4 films if not explicitly labeled 'favourites' 
            # or the user has no favorites.
            print("Could not find 'Favourites' section. The user might not have any favorites listed.")
            return

        # Find all list items with class that indicates a film poster
        # Usually ul.poster-list li.poster-container div.poster
        posters = fav_section.find_all("div", class_="poster")
        
        if not posters:
            print("No favorite movies found in the section.")
            return

        print(f"\n{username}'s Favorite Movies:")
        for poster in posters:
            # The title is often in the 'data-film-name' attribute or inside an img alt tag
            film_name = poster.get('data-film-name')
            film_year = poster.get('data-film-release-year')
            
            if film_name:
                output = f"- {film_name}"
                if film_year:
                    output += f" ({film_year})"
                print(output)
            else:
                # Fallback if attribute missing
                img = poster.find('img')
                if img and img.get('alt'):
                    print(f"- {img.get('alt')}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'gandalf' with any valid Letterboxd username
    # You can change this to test other users
    target_user = "ljstelzer8" 
    get_user_favorites(target_user)
