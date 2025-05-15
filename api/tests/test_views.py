from django.test import TestCase, Client
from unittest.mock import patch
from django.urls import reverse
import requests


class ApiViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_view_get(self):
        """GET request to index_view should return 200 and use the correct template."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @patch('api.views.requests.get')
    def test_index_view_post_valid_city(self, mock_get):
        """POST request with valid city should render weather data."""
        mock_response_data = {
            "location": {
                "name": "London",
                "country": "UK",
                "lon": -0.13,
                "lat": 51.51
            },
            "current": {
                "temp_c": 12.3,
                "pressure_mb": 1015,
                "humidity": 60,
                "condition": {"text": "Sunny", "icon": "icon_url"},
                "air_quality": {"us-epa-index": 2}
            },
            "forecast": {
                "forecastday": [
                    {},  # skip current day
                    {
                        "date": "2025-05-16",
                        "day": {
                            "avgtemp_c": 15,
                            "condition": {"text": "Cloudy", "icon": "icon_url"}
                        }
                    }
                ]
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        response = self.client.post(reverse('index'), {'city': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "London")
        self.assertContains(response, "Sunny")
        self.assertContains(response, "Cloudy")

    @patch('api.views.requests.get')
    def test_autocomplete_view_success(self, mock_get):
        """autocomplete_view should return JSON list of cities."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"name": "London"}, {"name": "Lodz"}]

        response = self.client.get(reverse('autocomplete') + '?q=Lo')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            '[{"name": "London"}, {"name": "Lodz"}]'
        )

    @patch('api.views.requests.get')
    def test_autocomplete_view_empty_query(self, mock_get):
        """autocomplete_view with empty query should return empty list."""
        response = self.client.get(reverse('autocomplete'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), '[]')
        mock_get.assert_not_called()

    @patch('api.views.requests.get')
    def test_autocomplete_view_api_error(self, mock_get):
        """autocomplete_view should handle API errors gracefully."""
        mock_get.side_effect = requests.RequestException("API error")
        response = self.client.get(reverse('autocomplete') + '?q=Error')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), '[]')
