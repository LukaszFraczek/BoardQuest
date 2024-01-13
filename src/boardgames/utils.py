import requests
from xml.etree import ElementTree

from icecream import ic

BGG_API_URL = 'https://www.boardgamegeek.com/xmlapi2'
SEARCH_CACHE_PERSISTENCE = 300


def get_search_key(query: str) -> str:
    return f'bgg_search_{query}'


class BGGSearch:
    @staticmethod
    def __clean_items_response(response):
        # Parse the XML response
        root = ElementTree.fromstring(response.content)

        # Extract information about the searched games
        games = []
        for item in root.findall('.//item'):
            game_id = item.get('id')
            name = item.find('./name').get('value')
            name_type = item.find('./name').get('type')
            release_year = item.find('./yearpublished').get('value')

            games.append({
                'id': game_id,
                'name': name,
                'name_type': name_type,
                'release_year': release_year,
            })
        return games

    @staticmethod
    def __filter_response(response, name_type='all'):
        # Check if name_type is specified and if it matches the current item
        ic(name_type)

        if not name_type or name_type == 'all':
            return response

        filtered_response = []
        for game in response:
            if game.get('name_type') == name_type:
                filtered_response.append(game)
        return filtered_response

    @classmethod
    def fetch_items(cls, name, name_type):
        # First check if data is already in cache
        cache_key = get_search_key(name)
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return cls.__filter_response(cached_data, name_type)

        # Parameters for the search query
        params = {'query': name, 'type': 'boardgame'}

        # Make the request to the API
        response = requests.get(f"{BGG_API_URL}/search", params=params)

        ic("search call to BGG")
        ic(response)

        if response.status_code == 200:
            clean_response = cls.__clean_items_response(response)
            cache.set(cache_key, clean_response, SEARCH_CACHE_PERSISTENCE)
            return cls.__filter_response(clean_response, name_type)
        else:
            print(f"BGG fetch items request error: {response.status_code}")
            return None


class BGGItemDetails:
    pass
