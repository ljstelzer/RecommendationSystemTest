from movie_recs import *

username = "ljstelzer8"

last50 = get_last_logged(username, 50)
actor_count = {}
stars_in = {}
for movie in last50:
    actors = get_actors_in_movie(movie)
    for actor in actors:
        if actor in actor_count:
            stars_in[actor].append(movie)
            actor_count[actor] = actor_count[actor] + 1
        else:
            stars_in[actor] = [movie]
            actor_count[actor] = 1

# Sort by count (descending)
sorted_actors = sorted(actor_count.items(), key=lambda item: item[1], reverse=True)

print(f"\nTop actors in last {len(last50)} logged movies:")
for actor, count in sorted_actors[:30]:
    movies_list = stars_in[actor]
    print(f"{actor}: {count}")
    for movie in movies_list:
        print(f"  - {movie}")
    print("-" * 30)
    
