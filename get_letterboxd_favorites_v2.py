import time
from letterboxdpy.user import User

def get_user_favorites(username):
    print(f"Fetching favorites for user: {username}...")
    try:
        user = User(username)
        # Accessing favorites - assuming it returns the list/dict of favorites
        favorites = user.favorites
        
        if not favorites:
            print("No favorites found or user profile is private/empty.")
            return

        print(f"\n{username}'s Favorite Movies:")
        # Based on library behavior, iterate through the results
        # If favorites is a dictionary, keys are usually titles.
        for movie in favorites:
            if isinstance(movie, tuple):
                 # Some versions return tuples (id, title)
                 print(f"- {movie[1]}")
            else:
                 print(f"- {movie}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    target_user = "ljstelzer8"
    get_user_favorites(target_user)
