from fastmcp.server import FastMCP
from tools.tmdb_client import TMDBClient
from tools.base_config import get_logger
from tools.omdb_client import OMDBClient

logger = get_logger()

mcp = FastMCP("Film Finder MCP Server", version="0.1.0")
logger.info(f"FastMCP app created")
tmdb_client = TMDBClient()
logger.info(f"TMDB client created")
omdb_client = OMDBClient()
logger.info(f"OMDB client created")


@mcp.tool
def authenticate_api_key() -> str:
    """Authenticate the API key with the TMDB API, check if the API key is valid and returns success or error message"""
    result = tmdb_client.authenticate_api_key()
    if result:
        return "Successfully authenticated API key"
    else:
        return "Failed to authenticate API key"


@mcp.tool
def get_popular_movies(language: str = "en-US", page: int = 1) -> list[dict]:
    """Get the popular movies from the TMDB API for a given language and page"""
    result = tmdb_client.get_popular_movies(language, page)
    if result:
        return [
            {
                "id": movie["id"],
                "title": movie["title"],
                "overview": movie["overview"],
                "release_date": movie["release_date"],
                "vote_average": movie["vote_average"],
                "popularity": movie["popularity"],
            }
            for movie in result[:7]
        ]
    return []


@mcp.tool
def get_movie_details(movie_id: int) -> dict:
    """Get the details of a movie from the TMDB API for a given movie ID"""
    result = tmdb_client.get_movie_details(movie_id)
    if result:
        return [
            {
                "id": result["id"],
                "title": result["title"],
                "overview": result["overview"],
                "release_date": result["release_date"],
                "vote_average": result["vote_average"],
                "popularity": result["popularity"],
            }
        ]
    return []


@mcp.tool
def get_popular_tv_shows(language: str = "en", page: int = 1) -> list[dict]:
    """Get the popular TV shows from the TMDB API for a given language and page"""
    result = tmdb_client.get_popular_tv_shows(language, page)
    if result:
        return [
            {
                "id": tv_show["id"],
                "name": tv_show["name"],
                "overview": tv_show["overview"],
                "first_air_date": tv_show["first_air_date"],
                "vote_average": tv_show["vote_average"],
                "vote_count": tv_show["vote_count"],
                "popularity": tv_show["popularity"],
                "original_language": tv_show["original_language"],
                "origin_country": tv_show["origin_country"],
            }
            for tv_show in result[:7]
        ]
    return []
    # if result:
    #     return popular_tv_shows_prompt(language, page, result)
    # return []


@mcp.tool()
def get_movie_recommendation(language: str, genre_id: str = None) -> list[dict]:
    """Get a movie recommendation based on the movie name"""
    response = tmdb_client.discover_movies(language, genre_id)
    results = response.get("results", [])
    if results:
        return [
            {
                "id": movie["id"],
                "title": movie["title"],
                "overview": movie["overview"],
                "release_date": movie["release_date"],
                "vote_average": movie["vote_average"],
                "popularity": movie["popularity"],
            }
            for movie in results[:7]
        ]
    else:
        return []


@mcp.tool
def get_top_rated_movies(language: str = "en-US", page: int = 1) -> list[dict]:
    """
    Get the top rated movies from the TMDB API for a given language and page

    Args:
        language: The language of the movies to get, default is "en-US"
        page: The page number of the movies to get, default is 1

    Returns:
        A list of dictionaries containing the details of the top rated movies
    """
    result = tmdb_client.get_top_rated_movies(language, page)
    if result:
        return [
            {
                "title": movie["title"],
                "overview": movie["overview"],
                "vote_average": movie["vote_average"],
                "popularity": movie["popularity"],
                "id": movie["id"],
                "release_date": movie["release_date"],
            }
            for movie in result[:10]
        ]
    return []


@mcp.tool
def get_top_rated_tv_shows(language: str = "en-US", page: int = 1) -> list[dict]:
    """
    Get the top rated TV shows from the TMDB API for a given language and page

    Args:
        language: The language of the movies to get, default is "en-US"
        page: The page number of the movies to get, default is 1

    Returns:
        A list of dictionaries containing the details of the top rated TV shows
    """
    result = tmdb_client.get_top_rated_tv_shows(language, page)
    if result:
        return [
            {
                "title": tv_show["name"],
                "overview": tv_show["overview"],
                "vote_average": tv_show["vote_average"],
                "popularity": tv_show.get("popularity"),
                "id": tv_show["id"],
                "first_air_date": tv_show["first_air_date"],
            }
            for tv_show in result[:10]
        ]
    return []


@mcp.tool
def get_movie_details_by_title(title: str) -> list[dict]:
    """
    Get the details of a movie from the OMDB API for a given movie title
    """
    result = omdb_client.get_movie_details_by_title(title)
    if result:
        return [
            {
                "title": result["Title"],
                "year": result["Year"],
                "plot": result["Plot"],
                "genre": result["Genre"],
                "imdb_rating": result["imdbRating"],
                "imdb_votes": result["imdbVotes"],
                "imdb_id": result["imdbID"],
            }
            for movie in result
        ]
    return []


@mcp.tool
def get_movie_details_by_imdb_id(imdb_id: str) -> list[dict]:
    """
    Get the details of a movie from the OMDB API for a given IMDB ID
    """
    result = omdb_client.get_movie_details_by_imdb_id(imdb_id)
    if result:
        return [
            {
                "title": result["Title"],
                "year": result["Year"],
                "plot": result["Plot"],
                "genre": result["Genre"],
                "imdb_rating": result["imdbRating"],
                "imdb_votes": result["imdbVotes"],
                "imdb_id": result["imdbID"],
            }
            for movie in result
        ]
    return []


# MCP PROMPTS

"""
Concept: Prompts allow the server to guide the LLM to generate text/decisions.
  Use Cases:
  - Guide the LLM to generate movie/tv recommendation
  - Guide the LLM to generate movie/tv analysis
"""


@mcp.prompt()
def movie_recommendation_prompt() -> str:
    """Guide for getting a movie recommendation"""
    return """
    You are a movie recommendation assistant, when user asks for a movie recommendation, you should follow these steps:
    1. Ask the user for the language they want the movie in, if not provided, use the default language "en".
    2. Ask the user for the page number they want to see the movies on, if not provided, use the default page number 1.
    3. Get the popular movies from the TMDB API for the given language and page number.
    4. Select a few movies and return the details of the movies in a list of dictionaries.
    5. Along with WHY did you select the movies.
    """


@mcp.prompt()
def tv_show_recommendation_prompt() -> str:
    """Guide for getting a TV show recommendation"""
    return """
    You are a TV show recommendation assistant, when user asks for a TV show recommendation, you should follow these steps:
    1. Ask the user for the language they want the TV show in, if not provided, use the default language "en".
    2. Ask the user for the page number they want to see the TV shows on, if not provided, use the default page number 1.
    3. Get the popular TV shows from the TMDB API for the given language and page number.
    4. Select a few TV shows and return the details of the TV shows in a list of dictionaries.
    5. Along with WHY did you select the TV shows.
    """


@mcp.prompt()
def movie_analysis_prompt() -> str:
    """Guide for analyzing movies: use get_popular_movies, get_top_rated_movies, get_movie_details_by_title, then compare and pick the best."""
    return """
    You are a movie analysis assistant. When the user asks for movie analysis, follow these steps:
    1. Get popular movies from the TMDB API using get_popular_movies tool.
    2. Get top rated movies from the TMDB API using get_top_rated_movies tool.
    3. Get details for selected titles from the OMDB API using get_movie_details_by_title(title).
    4. Compare ratings, details, and popularity across the movies.
    5. Share the best movie and a short justification.
    """


# Prompt Template
@mcp.prompt()
def compare_movie_sources_prompt(title: str) -> str:
    """Compare movie data from TMDB and OMDB"""
    return f"""
    Compare data for "{title}" across sources:
    1. Search TMDB using get_popular_movies or get_top_rated_movies
    2. Get OMDB details using get_movie_details_by_title("{title}")
    3. Compare ratings, plots, and metadata
    4. Highlight differences and recommend which source is more complete
    """


## MCP Resources
"""
Concept: Resources allow the server to expose information to the client.
- Resources = Data (read-only, expose information)
  Use Cases:
  - Expose API configuration, documentation, endpoints and usage information etc
"""


@mcp.resource("omdb://config")
def get_omdb_config() -> str:
    """Expose OMDB API configuration Information"""
    return f"""
    OMDB API Configuration Information:
    ================================
    Base URL: {omdb_client.BASE_URL}
    OMDB API Queried using title or IMDB ID, type i.e movie or tv show. 
    """


@mcp.resource("tmdb://config")
def get_tmdb_config() -> str:
    """Expose TMDB API configuration (live from TMDB API)."""
    languages = tmdb_client.get_languages()
    movie_genres = tmdb_client.get_movie_genres()
    tv_genres = tmdb_client.get_tv_show_genres()
    languages_list = ", ".join(
        f"{x.get('english_name', x.get('name', ''))}" for x in (languages or [])[:15]
    )
    movie_genres_list = ", ".join(
        g.get("name", "")
        for g in (
            movie_genres
            if isinstance(movie_genres, list)
            else (movie_genres or {}).get("genres", [])
        )[:10]
    )
    tv_genres_list = ", ".join(
        g.get("name", "")
        for g in (
            tv_genres
            if isinstance(tv_genres, list)
            else (tv_genres or {}).get("genres", [])
        )[:10]
    )
    return f"""
    TMDB API Configuration Information:
    ================================
    Base URL: {tmdb_client.BASE_URL}
    Available Languages: {languages_list or "—"}
    Available Movie Genres: {movie_genres_list or "—"}
    Available TV Show Genres: {tv_genres_list or "—"}
    """


@mcp.resource("tmdb://movie/top_rated")
def get_tmdb_top_rated_movies_resource() -> str:
    """Expose TMDB top rated movies as text. URI: tmdb://movie/top_rated"""
    result = tmdb_client.get_top_rated_movies()
    if not result:
        return "No top rated movies found."
    lines = ["TMDB Top Rated Movies (live)\n" + "=" * 40]
    for i, movie in enumerate(result[:5], 1):
        title = movie.get("title", "—")
        overview = (movie.get("overview") or "—")[:150]
        vote = movie.get("vote_average", "—")
        release = movie.get("release_date", "—")
        lines.append(f"\n{i}. {title} ({release}) — {vote}\n   {overview}...")
    return "\n".join(lines)


# Dynamic Resources
@mcp.resource("tmdb://movie/{movie_id}")
def get_tmdb_movie_resource(movie_id: str) -> str:
    """Dynamically load a movie's details when this resource is read. URI e.g. tmdb://movie/550"""
    try:
        mid = int(movie_id)
        movie = tmdb_client.get_movie_details(mid)
    except ValueError:
        return f"Invalid movie ID: {movie_id}"
    if not movie:
        return f"No movie found for ID: {movie_id}"
    return f"""movie
    Title: {movie.get("title", "—")}
    Overview: {(movie.get("overview") or "—")[:400]}
    Release: {movie.get("release_date", "—")}
    Vote average: {movie.get("vote_average", "—")}
    """


@mcp.resource("omdb://movie/{imdb_id}")
def get_omdb_movie_resource(imdb_id: str) -> str:
    """Expose OMDB movie resource as text. URI: omdb://movie/tt0111161"""
    result = omdb_client.get_movie_details_by_imdb_id(imdb_id)
    if not result:
        return "No movie found for IMDB ID: {imdb_id}"
    return f"""
    OMDB Movie Resource Information:
    ================================
    Title: {result["Title"]}
    Year: {result["Year"]}
    Plot: {result["Plot"]}
    Genre: {result["Genre"]}
    IMDB Rating: {result["imdbRating"]}
    IMDB Votes: {result["imdbVotes"]}
    IMDB ID: {result["imdbID"]}
    """


# MCP Sampling
"""
Concept: Sampling allows the server to request the LLM to
  generate text/decisions. The server asks questions, and the
  client's LLM responds.

  Use Cases:
  - Generate movie descriptions/summaries
  - Create personalized recommendations
  - Generate creative content based on movie data
  - Make intelligent selections from options
"""


@mcp.tool()
async def generate_recommendation_explanation(movie_ids: list[int] | dict) -> str:
    """Generate natural language explanation for why these movies are recommended. Pass movie_ids as a list of TMDB movie IDs, e.g. [550, 155], or as an object: {"movie_ids": [550, 155]}."""
    if isinstance(movie_ids, dict):
        movie_ids = movie_ids.get("movie_ids", [])
    if not movie_ids:
        return "No movie IDs provided. Pass a list of TMDB movie IDs, e.g. [550, 155]."
    # Fetch the movie details from tmdb client api
    movies = [tmdb_client.get_movie_details(movie_id) for movie_id in movie_ids]
    movies_info = "\n".join(
        [
            f"- {m.get('title', 'Unknown')}: {(m.get('overview') or '')[:200]}"
            for m in movies
            if m
        ]
    )
    if not movies_info:
        return "Could not fetch details for the given movie IDs."
    try:
        result = await mcp.sample(
            messages=[
                {
                    "role": "user",
                    "content": f"Explain why these movies would appeal to someone:\n{movies_info}",
                }
            ],
            max_tokens=500,
        )
        # Using the mcp.sample method to generate the recommendation explanation
        logger.info(f"Generated recommendation explanation: {result.content}")
        return result.content
    except Exception as e:
        logger.warning(f"LLM sample not available ({e}), returning movie list instead.")
        return f"Movies considered:\n{movies_info}"


"""
MCP Elicitation:
The purpose of elicitation is to allow the server to seek additional information from the user.
Whenever the user input is invalid or insufficient, the server should seek additional information from the user.
  - Ask the user for content type if not provided or only language is provided
"""


@mcp.tool()
def search_popular_content_type_elicitation(
    language: str = "en-US", content_type: str | None = None, page: int = 1
) -> dict | list[dict]:
    """
    Ask the user for content type to search for if not provided or only language is provided

    Args:
        language: The language of the content to search, default is "en-US"
        content_type: The type of content to search, default is None
        page: The page number of the content to search, default is 1

    Returns:
        A string asking the user for content type if not provided or only language is provided
    """
    if content_type is None:
        # elicitation if content type is not provided
        logger.info(f"Elicitation: Ask the user for content type to search")
        return {
            "elicit": {
                "message": f"I see that you are searching for popular content in {language}, Please let me know what would you like to search for tv shows or movies?",
                "fields": {
                    "content_type": {
                        "type": "string",
                        "enum": ["tv shows", "movies"],
                        "required": True,
                        "description": "The type of content to search, default is None",
                    }
                },
            }
        }

    elif content_type not in [
        "tv shows",
        "movies",
        "tv_show",
        "movie",
        "TV Show",
        "MOVIE",
        "MOVIES",
    ]:
        # elicitation if content type is not valid
        logger.info(
            f"Invalid content type {content_type}, Elicitation: Ask the user for content type to search"
        )
        return {
            "elicit": {
                "message": f"I see that you are searching for popular content for content type {content_type}, it is invalid. Please let me know what would you like to search either tv shows or movies?",
                "fields": {
                    "content_type": {
                        "type": "string",
                        "enum": ["tv shows", "movies"],
                        "required": True,
                        "description": "The valid content types are tv shows or movies",
                    }
                },
            }
        }
    elif content_type in ["tv shows", "TV Shows", "tv_show", "tv_shows"]:
        # elicitation if content type is tv shows
        logger.info(f"Fetching popular tv shows from the TMDB API")
        res = tmdb_client.get_popular_tv_shows(language, page)
        if res:
            return [
                {
                    "id": tv_show["id"],
                    "name": tv_show["name"],
                    "overview": tv_show["overview"],
                    "first_air_date": tv_show["first_air_date"],
                    "vote_average": tv_show["vote_average"],
                    "vote_count": tv_show["vote_count"],
                    "popularity": tv_show["popularity"],
                    "original_language": tv_show["original_language"],
                    "origin_country": tv_show["origin_country"],
                }
                for tv_show in res[:7]
            ]
        return []
    else:
        logger.info(f"Fetching popular movies from the TMDB API")
        res = tmdb_client.get_popular_movies(language, page)
        if res:
            return [
                {
                    "id": movie["id"],
                    "title": movie["title"],
                    "overview": movie["overview"],
                    "release_date": movie["release_date"],
                    "vote_average": movie["vote_average"],
                    "popularity": movie["popularity"],
                    "original_language": movie["original_language"],
                }
                for movie in res[:7]
            ]
        return []


if __name__ == "__main__":
    logger.info(f"Strarting TMDB MCP Server on http://localhost:8000")
    # mcp.run(transport="http", port=8000)
    mcp.run()
