import unittest
from unittest.mock import MagicMock, patch
from src.maps.search import MapsService

class TestMapsService(unittest.TestCase):
    @patch('googlemaps.Client')
    def test_search_repair_shops(self, mock_gmaps):
        # Mocking the googlemaps client response
        mock_instance = mock_gmaps.return_value
        mock_instance.places.return_value = {
            'results': [{'place_id': 'test_id'}]
        }
        mock_instance.place.return_value = {
            'result': {
                'name': 'Test Shop',
                'formatted_phone_number': '0555 123 45 67',
                'formatted_address': 'Test Address'
            }
        }

        svc = MapsService(api_key="test_key")
        results = svc.search_repair_shops("Istanbul")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Test Shop')
        self.assertEqual(results[0]['phone'], '0555 123 45 67')

if __name__ == '__main__':
    unittest.main()
