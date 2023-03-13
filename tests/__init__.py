import unittest

from flaskr import create_app


class TestBase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()

    def _when_the_test_client_calls_a_route(self, route):
        return self.app.get(route, follow_redirects=True)

    def _when_the_test_client_posts_on_a_route(self, route, data):
        return self.app.post(route, data=data, follow_redirects=True)

    def _then_the_page_header_contains_the_correct_text(
        self, response, header_text
    ):
        assert header_text in response.data
