import requests
from xml.etree import ElementTree

from icecream import ic


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
    def fetch_items(cls, query):
        # Parameters for the search query
        params = {'query': query, 'type': 'boardgame'}

        # Make the request to the API
        response = requests.get(f"{cls.BGG_API_URL}/search", params=params)

        ic("search call to BGG")
        ic(response)

        if response.status_code == 200:
            return cls.__clean_items_response(response)
        else:
            print(f"BGG request error: {response.status_code}")
            return None


class BGGItemDetails:
    pass
