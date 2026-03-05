import requests
import os
from datetime import timedelta
from cachetools import cached,TTLCache
from tools.base_config import get_logger, setup_api_key_config

logger = get_logger()

movie_details_cache = TTLCache(maxsize=100, ttl=timedelta(hours=3).total_seconds())


class OMDBClient:
    BASE_URL = "http://www.omdbapi.com/"

    def __init__(self):
        _, self.api_key = setup_api_key_config()
        self.session = requests.Session()

    def get_movie_details_by_title(self, title: str) -> list[dict]:
        cache_key = f"movie_details_{title}"
        params = {"apikey": self.api_key, "t": title}
        if cache_key in movie_details_cache:
            logger.info(f"Getting movie details from cache: {cache_key}")
            return movie_details_cache[cache_key]
        logger.info(f"CACHE MISS for movie details: {cache_key}")
        try:
            response = self.session.get(self.BASE_URL, params=params)
            if response.status_code != 200:
                logger.error(
                    f"Error getting movie details for title {title}: {response.status_code}"
                )
                return {}
            logger.info(f"Successfully got movie details for movie title {title}")
            movie_details_cache[cache_key] = response.json()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting movie details for movie title {title}: {e}")
            return {}

    def get_movie_details_by_imdb_id(self, imdb_id: str) -> list[dict]:
        params = {"apikey": self.api_key, "i": imdb_id}
        cache_key = f"movie_details_{imdb_id}"
        if cache_key in movie_details_cache:
            logger.info(f"Getting movie details for IMDB ID from cache: {cache_key}")
            return movie_details_cache[cache_key]
        logger.info(f"CACHE MISS for movie details for IMDB ID: {cache_key}")
        try:
            response = self.session.get(self.BASE_URL, params=params)
            if response.status_code != 200:
                logger.error(
                    f"Error getting movie details for IMDB ID {imdb_id}: {response.status_code}"
                )
                return {}
            logger.info(f"Successfully got movie details for IMDB ID {imdb_id}")
            movie_details_cache[cache_key] = response.json()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting movie details for IMDB ID {imdb_id}: {e}")
            return {}
