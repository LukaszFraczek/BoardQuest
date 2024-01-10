import requests
from xml.etree import ElementTree

from icecream import ic


class BGGSearch:
    BGG_API_URL = 'https://www.boardgamegeek.com/xmlapi2/search'

    @staticmethod
    def __clean_xml_response(response):
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
        response = requests.get(cls.BGG_API_URL, params=params)

        ic(response.content)

        if response.status_code == 200:
            return cls.__clean_xml_response(response)
        else:
            print(f"BGG request error: {response.status_code}")
            return None


class BGGItemSearch:
    pass
