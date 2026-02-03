# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python movie recommendation system integrating TMDB (The Movie Database) API and Letterboxd web scraping for movie discovery features.

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Required: Set TMDB API key in .env file
TMDB_API_KEY=your_key_here
```

Python version: 3.11.11 (specified in `.python-version`)

## Running the Project

```bash
# Run the example/test script (actor cross-reference demo)
python test_package.py
```

No formal test suite exists. Manual testing via `test_package.py`.

## Architecture

The `movie_recs/` package is the core module with functions exported via `__init__.py`:

**TMDB API Functions:**
- `find_by_actor.py` - `get_movies_by_actor()`, `get_actor_id()` - Actor-based movie search
- `find_by_genre.py` - `get_movies_by_genre()`, `get_genre_map()` - Genre-based filtering (uses AND logic for multiple genres)
- `find_similar.py` - `get_similar_movies()`, `get_movie_id()` - TMDB similarity recommendations
- `get_actors_in_movie.py` - `get_actors_in_movie()` - Get top 10 cast members (depends on `find_similar.get_movie_id()`)

**Letterboxd Scraping Functions:**
- `get_last_logged_movies.py` - `get_last_logged()` - Scrapes RSS feed for recent user activity (max 50 items)
- `get_letterboxd_favorites.py` - `get_user_favorites()` - Scrapes HTML profile for user favorites

## Key Dependencies

- `requests` - HTTP requests
- `beautifulsoup4` + `lxml` - Letterboxd HTML/XML parsing
- `python-dotenv` - Environment variable loading
- `letterboxdpy` - Listed but deprecated/abandoned per commit history

## External APIs

- **TMDB**: `https://api.themoviedb.org/3/` - Requires API key
- **Letterboxd**: Web scraping (RSS feeds and HTML profiles) - No API key needed

## Important Notes

- Letterboxd scraping is fragile and may break if site HTML structure changes
- No rate limiting implemented for API/scraping requests
- The `letterboxdpy` library in requirements.txt is not actively used
