from django.test import TestCase, RequestFactory
from api.middleware import LoggingMiddleware
from django.http import HttpResponse
import io
import sys

class ApiLoggingMiddlewareTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        # Fake response function for middleware to call
        self.get_response = lambda request: HttpResponse("OK")

        # Create instance of the middleware
        self.middleware = LoggingMiddleware(self.get_response)

    def test_middleware_prints_log(self):
        """Middleware should log the HTTP method and path to stdout."""
        request = self.factory.get('/test-path/')

        # Capture printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call middleware
        response = self.middleware(request)

        # Restore stdout
        sys.stdout = sys.__stdout__

        self.assertEqual(response.status_code, 200)
        self.assertIn("Handling request: 'GET' for path: '/test-path/'", captured_output.getvalue())
