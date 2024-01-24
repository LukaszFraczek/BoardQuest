from django.core.cache import cache
from django.conf import settings
from http import HTTPStatus

import requests
from xml.etree import ElementTree

from icecream import ic


def get_search_key(query: str) -> str:
    return f'bgg_search_{query}'


def get_item_details_key(bgg_id: int) -> str:
    return f'bgg_item_{bgg_id}'


class BGGSearch:
    @staticmethod
    def __clean_items_response(response) -> list:
        # Parse the XML response
        root = ElementTree.fromstring(response.content)

        # Extract information about the searched games
        games = []
        for item in root.findall('.//item'):
            game_id = item.get('id')
            name = item.find('./name').get('value')
            name_type = item.find('./name').get('type')
            release_year_element = item.find('./yearpublished')
            if release_year_element is not None:
                release_year = release_year_element.get('value')
            else:
                release_year = 'Unspecified'

            games.append({
                'bgg_id': game_id,
                'name': name,
                'name_type': name_type,
                'release_year': release_year,
            })
        return games

    @staticmethod
    def __filter_response(response, name_type='all') -> list:
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
    def fetch_items(cls, name, name_type) -> list:
        name = name.lower()

        # First check if data is already in cache
        cache_key = get_search_key(name)
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return cls.__filter_response(cached_data, name_type)

        # Request to BGG API
        params = {'query': name, 'type': 'boardgame'}
        response = requests.get(f"{settings.BGG_API_URL}/search", params=params)

        ic("search call to BGG")
        ic(response)

        if response.status_code == HTTPStatus.OK:
            clean_response = cls.__clean_items_response(response)
            cache.set(cache_key, clean_response, settings.SEARCH_CACHE_PERSISTENCE)
            return cls.__filter_response(clean_response, name_type)
        else:
            print(f"BGG fetch items request error: {response.status_code}")
            return []


class BGGItemDetails:
    @staticmethod
    def __clean_details_response(response) -> dict:
        # Parse the XML response
        root = ElementTree.fromstring(response.content)

        # Extract game details
        item = root.find('.//item')

        bgg_id = item.get('id')
        thumbnail_url = item.find('./thumbnail').text.strip()
        image_url = item.find('./image').text.strip()
        primary_name = item.find('./name[@type="primary"]').get('value')
        release_year = item.find('./yearpublished').get('value')
        description = item.find('./description').text.strip()
        players_min = item.find('./minplayers').get('value')
        players_max = item.find('./maxplayers').get('value')
        playtime_min = item.find('./minplaytime').get('value')
        playtime_max = item.find('./maxplaytime').get('value')

        details = {
            'bgg_id': bgg_id,
            'thumbnail_url': thumbnail_url,
            'image_url': image_url,
            'primary_name': primary_name,
            'release_year': release_year if release_year != 0 else None,
            'description': description.replace("&#10;", "<br>"),
            'players_min': players_min,
            'players_max': players_max,
            'playtime_min': playtime_min,
            'playtime_max': playtime_max,
        }

        return details

    @classmethod
    def fetch_item(cls, bgg_id: int) -> dict:
        # First check if data is already in cache
        cache_key = get_item_details_key(bgg_id)
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return cached_data

        params = {'id': bgg_id}
        response = requests.get(f"{settings.BGG_API_URL}/thing/", params=params)

        ic("details call to BGG")
        ic(response)

        if response.status_code == HTTPStatus.OK:
            clean_response = cls.__clean_details_response(response)
            cache.set(cache_key, clean_response, settings.DETAILS_CACHE_PERSISTENCE)
            return clean_response
        else:
            print(f"BGG fetch items details request error: {response.status_code}")
            return {}
