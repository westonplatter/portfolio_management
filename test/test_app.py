from test.app_test_case import AppTestCase


class AppTest(AppTestCase):
    def test_root_path(self):
        res = self.client.get("/")
        assert res.status_code == 200
