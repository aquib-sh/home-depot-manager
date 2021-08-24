# Cache Memory Utilities
# Author: Shaikh Aquib
# Date: August 2021

import os
import json


class CacheSaver:
    """Saves Cache of the application."""
    def __init__(self, basefile):
        self.__cache_dir__ = os.path.abspath('cache')
        self.__cache_f__ = os.path.abspath(os.path.join(
            self.__cache_dir__, basefile))

        if not os.path.exists(self.__cache_dir__) : os.mkdir(self.__cache_dir__)

    def save_cache(self, cache: dict) -> None:
        with open(self.__cache_f__, "w") as f:
            json.dump(cache, f, indent=4)


class CacheRetriever:
    def __init__(self, basefile):
        self.__cache_dir__ = os.path.abspath('cache')
        self.__cache_f__ = os.path.abspath(os.path.join(
            self.__cache_dir__, basefile))
        if not os.path.exists(self.__cache_dir__) : os.mkdir(self.__cache_dir__)

    def cache_exists(self):
        return os.path.exists(self.__cache_f__)

    def retrieve_cache(self) -> dict:
        cache: dict = {}
        with open(self.__cache_f__, "r") as f:
            cache = json.load(f)
        return cache