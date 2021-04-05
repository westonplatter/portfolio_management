import re
import glob

from python_graphql_client import GraphqlClient
from pydantic import BaseModel
import pandas as pd
import numpy as np

GRAPHQL_ENDPOINT = "http://localhost:8000/ingest/graphql"

client = GraphqlClient(endpoint=GRAPHQL_ENDPOINT)


class Mutation(BaseModel):
    def execute(self, client):
        query = self.gen_mutation()
        variables = self.gen_variables()

        # print(f"query = {query}")
        # print(f"variables = {variables}")

        return client.execute(query=query, variables=variables)

    def gen_variables(self):
        return self.dict()


class Query(BaseModel):
    pass


class CreateTradeMutation(Mutation):
    transactionId: int

    # tradeId: str
    # accountId: str
    # assetCategory: str
    # conId: str
    # description: str
    # ibOrderId: str
    # ibExecId: str
    # symbol: str
    # tradeId: str
    # underlyingSymbol: str
    # #
    # multiplier: int
    # strike: str
    # expiry: str
    # putCall: str
    # dateTime: str
    # tradeDate: str
    # quantity: float
    # tradePrice: float
    # proceeds: float
    # ibCommission: float
    # netCash: float
    # closePrice: float
    # openCloseIndicator: str
    # fifoPnlRealized: float
    # fxPnl: float
    # mtmPnl: float
    # buySell: str
    # notes: str

    def gen_mutation(self):
        return """
            mutation x($transactionId: BigInt!) {
                createOrGetTrade(transactionId: $transactionId) {
                    trade {
                        transactionId
                    }
                }
            }
        """

    # def gen_mutation(self):
    #     return """
    #         mutation (
    #             $assetCategory: String,
    #             $conId: String,
    #             $symbol: String,
    #             $tradeId: String,
    #             $ibOrderId: String,
    #             $ibExecId: String,
    #             $transactionId: String,
    #             $accountId: String,
    #             $underlyingSymbol: String,
    #             $description: String,
    #             $multiplier: Int,
    #             $strike: String,
    #             $expiry: String,
    #             $putCall: String,
    #             $dateTime: String,
    #             $tradeDate: String,
    #             $quantity: Float,
    #             $tradePrice: Float,
    #             $proceeds: Float,
    #             $ibCommission: Float,
    #             $netCash: Float,
    #             $closePrice: Float,
    #             $openCloseIndicator: String,
    #             $fifoPnlRealized: Float,
    #             $fxPnl: Float,
    #             $mtmPnl: Float,
    #             $buySell: String,
    #             $notes: String,
    #         )
    #             {
    #                 createTrade(
    #                     assetCategory: $assetCategory,
    #                     conId: $conId,
    #                     symbol: $symbol,
    #                     tradeId: $tradeId,
    #                     ibOrderId: $ibOrderId,
    #                     ibExecId: $ibExecId,
    #                     transactionId: $transactionId,
    #                     accountId: $accountId,
    #                     underlyingSymbol: $underlyingSymbol,
    #                     description: $description,
    #                     multiplier: $multiplier,
    #                     strike: $strike,
    #                     expiry: $expiry,
    #                     putCall: $putCall,
    #                     dateTime: $dateTime,
    #                     tradeDate: $tradeDate,
    #                     quantity: $quantity,
    #                     tradePrice: $tradePrice,
    #                     proceeds: $proceeds,
    #                     ibCommission: $ibCommission,
    #                     netCash: $netCash,
    #                     closePrice: $closePrice,
    #                     openCloseIndicator: $openCloseIndicator,
    #                     fifoPnlRealized: $fifoPnlRealized,
    #                     fxPnl: $fxPnl,
    #                     mtmPnl: $mtmPnl,
    #                     buySell: $buySell,
    #                     notes: $notes
    #                 ) {
    #                     trade {
    #                         id
    #                     }
    #                 }
    #             }
    #     """


def rename_columns(ddf):
    return ddf.rename(
        columns={
            "tradeID": "tradeId",
            "ibExecID": "ibExecId",
            "ibOrderID": "ibOrderId",
            "transactionID": "transactionId",
            "conid": "conId",
        }
    )


def transform(ddf):
    return ddf

def submit_trades_from_file(fn: str):
    print(f"\n{fn}")
    trades = pd.read_csv(fn) # static type import the data
    trades = rename_columns(trades)
    trades = transform(trades)
    fields_to_extract = list(CreateTradeMutation.schema()["properties"].keys())
    data = trades[fields_to_extract]

    for _, row in data.iterrows():
        create_trade_mutation = CreateTradeMutation(**row)
        res = create_trade_mutation.execute(client)
        print(res)
        print(".", end="", flush=True)


def execute():
    for fn in glob.glob("*.csv"):
        # if re.search("[0-9]_trades.csv", fn):
        submit_trades_from_file(fn)
