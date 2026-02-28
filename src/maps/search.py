import googlemaps
import os
from typing import List, Dict

class MapsService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        if not self.api_key:
            raise ValueError("Google Maps API Key is required.")
        self.gmaps = googlemaps.Client(key=self.api_key)

    def search_repair_shops(self, location: str, query: str = "Otomobil Tamiri") -> List[Dict]:
        """
        Searches for repair shops in a specific location.
        """
        places_result = self.gmaps.places(query=f"{query} in {location}")

        shops = []
        for place in places_result.get('results', []):
            shop_id = place['place_id']
            # Fetch detailed information including phone number
            details = self.gmaps.place(place_id=shop_id, fields=['name', 'formatted_phone_number', 'international_phone_number', 'formatted_address'])

            result = details.get('result', {})
            phone = result.get('international_phone_number') or result.get('formatted_phone_number')

            if phone:
                shops.append({
                    'place_id': shop_id,
                    'name': result.get('name'),
                    'address': result.get('formatted_address'),
                    'phone': phone
                })

        return shops

if __name__ == "__main__":
    # Example usage (requires API key)
    # svc = MapsService()
    # print(svc.search_repair_shops("Istanbul"))
    pass
