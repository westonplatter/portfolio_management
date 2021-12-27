import datetime
import glob
from typing import Dict, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel
from python_graphql_client import GraphqlClient

GRAPHQL_ENDPOINT = "http://localhost:8000/ingest/graphql"

client = GraphqlClient(endpoint=GRAPHQL_ENDPOINT)


class Mutation(BaseModel):
    def gen_variables(self):
        return self.dict()

    def execute(self, client):
        query = self.gen_mutation()
        variables = self.gen_variables()
        return client.execute(query=query, variables=variables)


class Query(BaseModel):
    def gen_variables(self) -> Dict:
        return {}

    def execute(self, client):
        query = self.gen_query()
        variables = self.gen_variables()
        return client.execute(query=query, variables=variables)


class GetLastTradeDate(Query):
    accountId: Optional[str]

    def gen_query(self) -> str:
        return """
        query x ($accountId: String) {
            lastTradeDate(accountId: $accountId)
        }
        """


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
            "dateTime": "executedAt",
        }
    )


def transform(df) -> pd.DataFrame:
    df.executedAt = pd.to_datetime(df["executedAt"]).dt.strftime("%Y-%m-%dT%H:%M%:%SZ")

    df.expiry = pd.to_datetime(df["expiry"]).dt.strftime("%Y-%m-%dT%H:%M%:%SZ")
    df.expiry = df.expiry.replace({np.nan: None})

    df.strike = df.strike.replace({np.nan: None})

    df.tradeId = df.tradeId.replace({np.nan: None})

    return df


def get_latest_trade_executed_at_per_account_id(
    graphql_client, account_id: str
) -> datetime.date:
    query = GetLastTradeDate(accountId=account_id)
    data = query.execute(graphql_client)["data"]
    latest_trade_executed_at = data["lastTradeDate"]
    year, month, day = [int(x) for x in latest_trade_executed_at.split("-")]
    latest_trade_executed_at: datetime.date = datetime.date(year, month, day)
    min_date: datetime.date = latest_trade_executed_at - datetime.timedelta(days=2)
    return min_date


def submit_trades_from_file(fn: str, import_all: bool):
    print(f"\nSubmitting trades for {fn}")
    df = pd.read_csv(fn)  # static type import the data
    df = rename_columns(df)
    df = transform(df)
    fields_to_extract = list(CreateTradeMutation.schema()["properties"].keys())
    df = df[fields_to_extract].copy()

    # if not import_all:
        # # get min date
        # account_id = df['accountId'].values[0]
        # min_date = get_latest_trade_executed_at_per_account_id(client, account_id)

        # # filter down data to exclude all trades before min_date
        # df["executed_at_date"] = pd.to_datetime(df["executedAt"]).dt.date
        # df = df.query("@min_date <= executed_at_date").copy()

        # print(f"AccountId={account_id}: importing {len(df)} new trades")

    for _, row in df.iterrows():
        create_trade_mutation = CreateTradeMutation(**row)
        _ = create_trade_mutation.execute(client)
        print(".", end="", flush=True)


def execute(import_all):
    for fn in glob.glob("*.csv"):
        submit_trades_from_file(fn, import_all)
