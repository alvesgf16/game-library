import unittest

from flaskr import create_app


class TestBase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()
