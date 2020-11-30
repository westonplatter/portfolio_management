from test.app_test_case import AppTestCase


class AppTest(AppTestCase):
    def test_root_path(self):
        res = self.client.get("/")
        assert res.status_code == 200

    def test_invalid_path(self):
        res = self.client.get("/invalid")
        assert res.status_code == 404

    def test_one_more(self):
        assert 1 == 1
