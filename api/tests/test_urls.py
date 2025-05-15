from django.test import TestCase
from django.urls import reverse, resolve
from api import views


class ApiUrlsTest(TestCase):
    """
    Test case for verifying URL routing in the application.
    Ensures that URL patterns resolve to the correct view functions
    and that named URLs reverse to the correct paths.
    """

    def test_resolves_index_url(self):
        resolver = resolve('/')
        self.assertEqual(resolver.func, views.index_view)

    def test_resolves_autocomplete_url(self):
        resolver = resolve('/autocomplete/')
        self.assertEqual(resolver.func, views.autocomplete_view)

    def test_reverse_index_url(self):
        url = reverse('index')
        self.assertEqual(url, '/')

    def test_reverse_autocomplete_url(self):
        url = reverse('autocomplete')
        self.assertEqual(url, '/autocomplete/')
