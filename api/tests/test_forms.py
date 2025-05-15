from django.test import TestCase
from api.forms import WeatherQueryForm


class ApiWeatherQueryFormTest(TestCase):
 
    def test_valid_city_name(self):
        """Form should be valid with a proper city name."""
        form = WeatherQueryForm(data={'city': 'New-York'})
        self.assertTrue(form.is_valid())

    def test_valid_city_with_spaces(self):
        """Form should be valid with a city name that contains spaces."""
        form = WeatherQueryForm(data={'city': 'San Francisco'})
        self.assertTrue(form.is_valid())

    def test_city_with_digits_should_fail(self):
        """Form should be invalid if the city contains digits."""
        form = WeatherQueryForm(data={'city': 'Paris123'})
        self.assertFalse(form.is_valid())
        self.assertIn('city', form.errors)

    def test_city_with_special_chars_should_fail(self):
        """Form should be invalid if the city contains special characters."""
        form = WeatherQueryForm(data={'city': 'Lo$Angeles'})
        self.assertFalse(form.is_valid())
        self.assertIn('city', form.errors)

    def test_city_empty_string_should_fail(self):
        """Form should be invalid if the city is an empty string."""
        form = WeatherQueryForm(data={'city': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('city', form.errors)
