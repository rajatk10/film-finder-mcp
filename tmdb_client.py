import requests
import os
import logging
from datetime import timedelta
from cachetools import cached, TTLCache
from base_config import get_logger, setup_api_key_config


logger = get_logger()

popular_movies_cache = TTLCache(maxsize=100, ttl=timedelta(hours=3).total_seconds())
popular_tv_shows_cache = TTLCache(maxsize=100, ttl=timedelta(hours=3).total_seconds())


class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        self.api_key, _ = setup_api_key_config()
        self.session = requests.Session()
        self.session.headers.update(
            {"accept": "application/json", "Authorization": f"Bearer {self.api_key}"}
        )

    def authenticate_api_key(self) -> bool:
        url = f"{self.BASE_URL}/authentication"
        try:
            response = self.session.get(url, params={"api_key": self.api_key})
            response_json = response.json()
            if response_json["success"] != True:
                logger.error(f"Error authenticating API key: {response.status_code}")
                return False
            logger.info(f"API key authenticated successfully")
            return response_json["success"]
        except Exception as e:
            logger.error(f"Error authenticating API key: {e}")
            return False

    def get_popular_movies(self, language: str = "en-US", page: int = 1) -> list[dict]:
        url = f"{self.BASE_URL}/movie/popular"
        params = {
            "language": language,
            "page": page,
        }
        cache_key = f"popular_movies_{language}_{page}"
        if cache_key in popular_movies_cache:
            logger.info(f"Getting popular movies from cache: {cache_key}")
            return popular_movies_cache[cache_key]
        logger.info(f"Cache miss for popular movies: {cache_key}")
        try:
            response = self.session.get(url, params=params)
            if response.status_code != 200:
                logger.error(f"Error getting popular movies: {response.status_code}")
                return []
            res = response.json()["results"]
            popular_movies_cache[cache_key] = res
            return res
        except Exception as e:
            logger.error(f"Error getting popular movies: {e}")
            return []

    def get_movie_details(self, movie_id: int) -> dict:
        url = f"{self.BASE_URL}/movie/{movie_id}"
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                logger.error(
                    f"Error getting movie details for movie ID {movie_id}: {response.status_code}"
                )
                return {}
            return response.json()
        except Exception as e:
            logger.error(f"Error getting movie details: {e}")
            return {}

    def get_popular_tv_shows(self, language: str = "en", page: int = 1) -> list[dict]:
        cache_key = f"popular_tv_shows_{language}_{page}"
        url = f"{self.BASE_URL}/tv/popular"
        params = {
            "language": language,
            "page": page,
        }
        if cache_key in popular_tv_shows_cache:
            logger.info(f"Getting popular TV shows from cache: {cache_key}")
            return popular_tv_shows_cache[cache_key]
        logger.info(f"Cache miss for popular TV shows: {cache_key}")
        try:
            response = self.session.get(url, params=params)
            if response.status_code != 200:
                logger.error(f"Error getting popular TV shows: {response.status_code}")
                return []
            popular_tv_shows_cache[cache_key] = response.json()["results"]
            return response.json()["results"]
        except Exception as e:
            logger.error(f"Error getting popular TV shows: {e}")
            return []

    def get_tv_show_details(self, tv_show_id: int) -> dict:
        url = f"{self.BASE_URL}/tv/{tv_show_id}"
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                logger.error(
                    f"Error getting TV show details for TV show ID {tv_show_id}: {response.status_code}"
                )
                return {}
            return response.json()
        except Exception as e:
            logger.error(f"Error getting TV show details: {e}")
            return {}

    def discover_movies(self, language=None, genre_id=None):
        params = {"sort_by": "vote_average.desc", "vote_count.gte": 500}
        if language:
            params["language"] = language
        if genre_id:
            params["with_genres"] = f"{genre_id}"

        url = f"{self.BASE_URL}/discover/movie"
        try:
            logger.info(f"Discovering movies with params: {params}")
            response = self.session.get(url, params=params)
            response_json = response.json()
            if response.status_code != 200:
                logger.error(f"Error discovering movies: {response.status_code}")
                return []
            return response_json
        except Exception as e:
            logger.error(f"Error discovering movies: {e}")
            return []

    def get_top_rated_movies(
        self, language: str = "en-US", page: int = 1
    ) -> list[dict]:
        url = f"{self.BASE_URL}/movie/top_rated"
        params = {
            "language": language,
            "page": page,
        }
        try:
            logger.info(f"Getting top rated movies with params: {params}")
            response = self.session.get(url, params=params)
            if response.status_code != 200:
                logger.error(f"Error getting top rated movies: {response.status_code}")
                return []
            logger.info(f"Successfully got top rated movies")
            return response.json()["results"]
        except Exception as e:
            logger.error(f"Error getting top rated movies: {e}")
            return []

    def get_top_rated_tv_shows(
        self, language: str = "en-US", page: int = 1
    ) -> list[dict]:
        url = f"{self.BASE_URL}/tv/top_rated"
        params = {
            "language": language,
            "page": page,
        }
        try:
            logger.info(f"Getting top rated TV shows with params: {params}")
            response = self.session.get(url, params=params)
            if response.status_code != 200:
                logger.error(
                    f"Error getting top rated TV shows: {response.status_code}"
                )
                return []
            logger.info(f"Successfully got top rated TV shows")
            return response.json()["results"]
        except Exception as e:
            logger.error(f"Error getting top rated TV shows: {e}")
            return []

    def get_languages(self) -> list[dict]:
        url = f"{self.BASE_URL}/configuration/languages"
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                logger.error(f"Error getting languages: {response.status_code}")
                return []
            logger.info(f"Successfully got languages from TMDB")
            return response.json()
        except Exception as e:
            logger.error(f"Error getting languages from TMDB: {e}")
            return []

    def get_movie_genres(self) -> list[dict]:
        url = f"{self.BASE_URL}/genre/movie/list"
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                logger.error(f"Error getting movie genres: {response.status_code}")
                return []
            logger.info(f"Successfully got movie genres from TMDB")
            return response.json()
        except Exception as e:
            logger.error(f"Error getting movie genres from TMDB: {e}")
            return []

    def get_tv_show_genres(self) -> list[dict]:
        url = f"{self.BASE_URL}/genre/tv/list"
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                logger.error(f"Error getting TV show genres: {response.status_code}")
                return []
            logger.info(f"Successfully got TV show genres from TMDB")
            return response.json()
        except Exception as e:
            logger.error(f"Error getting TV show genres from TMDB: {e}")
            return []
