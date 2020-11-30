import unittest
from api.app import create_app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def tearDown(self):
        pass
