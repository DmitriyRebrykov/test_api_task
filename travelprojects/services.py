import requests
from typing import Optional, Dict, Any
from django.core.cache import cache


class ArtInstituteAPIError(Exception):
    pass

class ArtInstituteService:
    BASE_URL = "https://api.artic.edu/api/v1"
    CACHE_TIMEOUT = 3600  # 1 hour

    @classmethod
    def get_artwork(cls, artwork_id: int) -> Optional[Dict[str, Any]]:
        cache_key = f"artwork_{artwork_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        try:
            url = f"{cls.BASE_URL}/artworks/{artwork_id}"
            response = requests.get(url, timeout=10)

            if response.status_code == 404:
                return None

            response.raise_for_status()
            data = response.json()

            artwork_data = data.get('data')
            if not artwork_data:
                return None

            cache.set(cache_key, artwork_data, cls.CACHE_TIMEOUT)

            return artwork_data

        except requests.exceptions.RequestException as e:
            raise ArtInstituteAPIError(f"Failed to fetch artwork: {str(e)}")

    @classmethod
    def validate_artwork_exists(cls, artwork_id: int) -> bool:
        try:
            artwork = cls.get_artwork(artwork_id)
            return artwork is not None
        except ArtInstituteAPIError:
            return False

    @classmethod
    def search_artworks(cls, query: str, limit: int = 10) -> Dict[str, Any]:
        try:
            url = f"{cls.BASE_URL}/artworks/search"
            params = {
                'q': query,
                'limit': limit,
                'fields': 'id,title,artist_display,date_display,place_of_origin,artwork_type_title,image_id'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            raise ArtInstituteAPIError(f"Failed to search artworks: {str(e)}")

    @classmethod
    def extract_place_data(cls, artwork_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'external_id': artwork_data.get('id'),
            'title': artwork_data.get('title', 'Unknown'),
            'artist_display': artwork_data.get('artist_display'),
            'date_display': artwork_data.get('date_display'),
            'place_of_origin': artwork_data.get('place_of_origin'),
            'artwork_type': artwork_data.get('artwork_type_title'),
            'image_id': artwork_data.get('image_id'),
        }