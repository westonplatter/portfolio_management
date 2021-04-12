import re
import glob
from typing import Optional

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
        return client.execute(query=query, variables=variables)

    def gen_variables(self):
        return self.dict()


class Query(BaseModel):
    pass


class CreateTradeMutation(Mutation):
    transactionId: int
    executedAt: str

    tradeId: Optional[int]
    accountId: str
    assetCategory: str
    # conId: str
    description: str
    # ibOrderId: str
    # ibExecId: str
    symbol: str
    # tradeId: str
    underlyingSymbol: str
    #
    multiplier: Optional[float]
    strike: Optional[float]
    expiry: Optional[str]
    # putCall: str
    # tradeDate: str
    # quantity: float
    # tradePrice: float
    # proceeds: float
    # ibCommission: float
    # netCash: float
    # closePrice: float
    openCloseIndicator: str
    fifoPnlRealized: float
    fxPnl: float
    mtmPnl: float
    buySell: str
    # notes: str

    def gen_mutation(self):
        return """
            mutation x(
                $transactionId: BigInt!,
                $executedAt: DateTime!,
                $tradeId: BigInt,
                $accountId: String,
                $assetCategory: String,
                $symbol: String,
                $underlyingSymbol: String,
                $openCloseIndicator: String,
                $fifoPnlRealized: Float,
                $fxPnl: Float,
                $mtmPnl: Float,
                $buySell: String,
                $description: String,
                $expiry: DateTime,
                $strike: Float,
                $multiplier: Float,
            ) {
                createOrGetTrade(
                    transactionId: $transactionId,
                    executedAt: $executedAt,
                    tradeId: $tradeId,
                    accountId: $accountId,
                    assetCategory: $assetCategory,
                    symbol: $symbol,
                    underlyingSymbol: $underlyingSymbol,
                    openCloseIndicator: $openCloseIndicator,
                    fifoPnlRealized: $fifoPnlRealized,
                    fxPnl: $fxPnl,
                    mtmPnl: $mtmPnl,
                    buySell: $buySell,
                    description: $description,
                    expiry: $expiry,
                    strike: $strike,
                    multiplier: $multiplier,
                ) {
                    trade {
                        transactionId
                    }
                }
            }
        """


def rename_columns(ddf) -> pd.DataFrame:
    return ddf.rename(
        columns={
            "tradeID": "tradeId",
            "ibExecID": "ibExecId",
            "ibOrderID": "ibOrderId",
            "transactionID": "transactionId",
            "conid": "conId",
            "dateTime": "executedAt"
        }
    )


def transform(df) -> pd.DataFrame:
    df.executedAt = pd.to_datetime(df['executedAt']).dt.strftime('%Y-%m-%dT%H:%M%:%SZ')

    df.expiry = pd.to_datetime(df['expiry']).dt.strftime('%Y-%m-%dT%H:%M%:%SZ')
    df.expiry = df.expiry.replace({np.nan: None})

    df.strike = df.strike.replace({np.nan: None})

    df.tradeId = df.tradeId.replace({np.nan: None})

    return df

def submit_trades_from_file(fn: str):
    print(f"\n{fn}")
    trades = pd.read_csv(fn) # static type import the data
    trades = rename_columns(trades)
    trades = transform(trades)
    fields_to_extract = list(CreateTradeMutation.schema()["properties"].keys())
    data = trades[fields_to_extract]

    for _, row in data.iterrows():
        create_trade_mutation = CreateTradeMutation(**row)
        _ = create_trade_mutation.execute(client)
        print(".", end="", flush=True)


def execute():
    for fn in glob.glob("*.csv"):
        # if re.search("[0-9]_trades.csv", fn):
        submit_trades_from_file(fn)
