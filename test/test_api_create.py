from flask import url_for
import json
from io import StringIO
from urllib.parse import urlencode
import unittest

from api.app import create_app
from api.models import Trade


class TestApiCreate(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

        # initiate a context
        ctx = self.app.app_context()
        ctx.push()

        self.client = self.app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def tearDown(self):
        pass

    def url_string(self, **url_params):
        with self.app.test_request_context():
            string = url_for("graphql_server")

        if url_params:
            string += "?" + urlencode(url_params)

        return string

    def response_json(self, res):
        return json.loads(res.data.decode())

    def json_dump_kwarg(self, **kwargs):
        return json.dumps(kwargs)

    def execute_query_with_variables(self, query, variables):

        return self.client.post(
            self.url_string(),
            data=self.json_dump_kwarg(query=query, variables=variables),
            content_type="application/json")


    def test_trades_all_empty(self):
        res = self.client.post(
            self.url_string(),
            data=self.json_dump_kwarg(query="query { trades { trades { id }}}"),
            content_type="application/json",
        )
        data = self.response_json(res)
        assert data == {"data": {"trades": {"trades": []}}}

    def test_trades_create_simple(self):
        Trade.query.delete()
        query="""
            mutation($transactionId: String) {
                createTrade (transactionId: $transactionId) {
                    trade {
                        transactionId
                    }
                }
            }
        """
        variables = dict(transactionId="123")
        res = self.execute_query_with_variables(query, variables)
        data = self.response_json(res)
        assert data == {'data': {'createTrade': {'trade': {'transactionId': '123'}}}}

    def test_trades_create_transform_trade_date(self):
        Trade.query.delete()
        query="""
            mutation($dateTime: String) {
                createTrade (dateTime: $dateTime) {
                    trade {
                        dateTime
                    }
                }
            }
        """
        variables = dict(dateTime="2020-09-14;15:07:30")
        res = self.execute_query_with_variables(query, variables)
        data = self.response_json(res)
        # import ipdb; ipdb.set_trace()
        # assert data == {'data': {'createTrade': {'trade': {'transactionId': '123'}}}}


    def gen_data(self):
        data = dict(
            assetCategory=None,
            symbol=None,
            conId=None,
            tradeId=None,
            ibOrderId=None,
            ibExecId=None,
            transactionId=None,
            accountId=None,
            underlyingSymbol=None,
            description=None,
            multiplier=None,
            strike=None,
            expiry=None,
            putCall=None,
            dateTime=None,
            tradeDate=None,
            quantity=None,
            tradePrice=None,
            proceeds=None,
            ibCommission=None,
            netCash=None,
            closePrice=None,
            openCloseIndicator=None,
            fifoPnlRealized=None,
            fxPnl=None,
            mtmPnl=None,
            buySell=None,
            notes=None,
        )
