import requests
from xml.etree import ElementTree

from icecream import ic

BGG_API_URL = 'https://www.boardgamegeek.com/xmlapi2'
SEARCH_CACHE_PERSISTENCE = 300


def get_search_key(query: str) -> str:
    return f'bgg_search_{query}'


class BGGSearch:
    BGG_API_URL = 'https://www.boardgamegeek.com/xmlapi2'

    @staticmethod
    def __clean_items_response(response):
        # Parse the XML response
        root = ElementTree.fromstring(response.content)

        # Extract information about the searched games
        games = []
        for item in root.findall('.//item'):
            game_id = item.get('id')
            name = item.find('./name').get('value')

            games.append({
                'id': game_id,
                'name': name,
            })
        return games

    @classmethod
    def fetch_items(cls, name):
        # First check if data is already in cache
        cache_key = get_search_key(name)
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return cached_data

        # Parameters for the search query
        params = {'query': name, 'type': 'boardgame'}

        # Make the request to the API
        response = requests.get(f"{BGG_API_URL}/search", params=params)

        ic("search call to BGG")
        ic(response)

        if response.status_code == 200:
            clean_response = cls.__clean_items_response(response)
            cache.set(cache_key, clean_response, SEARCH_CACHE_PERSISTENCE)
            return clean_response
        else:
            print(f"BGG fetch items request error: {response.status_code}")
            return None


class BGGItemDetails:
    pass
