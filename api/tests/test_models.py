from django.test import TestCase
from api.models import City


class ApiModelCityTest(TestCase):

    def setUp(self):
        """Set up a sample City instance before each test."""
        self.city = City.objects.create(
            city="Kraków",
            country_code="PL",
            temperature="22",
            pressure="1015",
            humidity="60",
            main="Clear",
            icon="http://example.com/icon.png"
        )

    def test_city_str_representation(self):
        """Test the string representation of the City model."""
        self.assertEqual(str(self.city), "Kraków")

    def test_city_fields(self):
        """Test the values of each field in the City model."""
        self.assertEqual(self.city.city, "Kraków")
        self.assertEqual(self.city.country_code, "PL")
        self.assertEqual(self.city.temperature, "22")
        self.assertEqual(self.city.pressure, "1015")
        self.assertEqual(self.city.humidity, "60")
        self.assertEqual(self.city.main, "Clear")
        self.assertEqual(self.city.icon, "http://example.com/icon.png")

    def test_created_at_is_set(self):
        """Test that the created_at field is automatically set."""
        self.assertIsNotNone(self.city.created_at)
