from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    graphql_sync,
    snake_case_fallback_resolvers,
    ObjectType,
    QueryType,
)
from api.models import Trade
from typing import List, Dict
from api.extensions import db
from loguru import logger


def resolve_create_trade(
    obj,
    info,
    assetCategory: str = None,
    symbol: str = None,
    conId = None,
    tradeId: str = None,
    ibOrderId: str = None,
    ibExecId: str = None,
    transactionId = None,
    accountId = None,
    underlyingSymbol = None,
    description = None,
    multiplier = None,
    strike = None,
    expiry = None,
    putCall = None,
    dateTime = None,
    tradeDate = None,
    quantity = None,
    tradePrice = None,
    proceeds = None,
    ibCommission = None,
    netCash = None,
    closePrice = None,
    openCloseIndicator = None,
    fifoPnlRealized = None,
    fxPnl = None,
    mtmPnl = None,
    buySell = None
):
  try:
    trade = Trade(
      assetCategory=assetCategory,
      conId=conId,
      symbol=symbol,
      tradeId=tradeId,
      ibOrderId=ibOrderId,
      ibExecId=ibExecId,
      transactionId=transactionId,
      accountId=accountId,
      underlyingSymbol=underlyingSymbol,
      description=description,
      multiplier=multiplier,
      strike=strike,
      expiry=expiry,
      putCall=putCall,
      dateTime=dateTime,
      tradeDate=tradeDate,
      quantity=quantity,
      tradePrice=tradePrice,
      proceeds=proceeds,
      ibCommission=ibCommission,
      netCash=netCash,
      closePrice=closePrice,
      openCloseIndicator=openCloseIndicator,
      fifoPnlRealized=fifoPnlRealized,
      fxPnl=fxPnl,
      mtmPnl=mtmPnl,
      buySell=buySell,
    )
    db.session.add(trade)
    db.session.commit()
    payload = {"success": True, "trade": trade.to_dict()}
  except Exception as e:
    payload = {"success": False, "errors": [str(e)]}
  return payload


def resolve_trades(obj, info, symbols: List[str] = [], pageSize: int = 100, pageIndex: int = 0) -> Dict:
  try:
    trades = []

    if symbols != []:
      trades = Trade.query.filter(Trade.symbol.in_(symbols)).limit(pageSize).all()
    else:
      trades = Trade.query.limit(pageSize).all()

    trades = [x.to_dict() for x in trades]

    total_count = Trade.query.count()
    payload = {"success": True, "trades": trades, "totalCount": 100}
  except Exception as e:
    payload = {"success": False, "errors": [str(e)]}
  return payload

# queries
query = ObjectType("Query")
query.set_field("trades", resolve_trades)

# mutations
mutation = ObjectType("Mutation")
mutation.set_field("createTrade", resolve_create_trade)

# connect queries and mutations to schema
type_defs = load_schema_from_path("api/schema.graphql")
schema = make_executable_schema(type_defs, query, mutation)
