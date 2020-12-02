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


def resolve_create_trade(
    obj,
    info,
    symbol: str,
    tradeID: str,
    ibOrderID: str,
    ibExecID: str,
    transactionID,
    accountId,
    underlyingSymbol,
    description,
    multiplier,
    strike,
    expiry,
    putCall,
    dateTime,
    tradeDate,
    quantity,
    tradePrice,
    proceeds,
    ibCommission,
    netCash,
    closePrice,
    openCloseIndicator,
    fifoPnlRealized,
    fxPnl,
    mtmPnl,
    buySell,
):
    try:
        trade = Trade(
            symbol=symbol,
            tradeID=tradeID,
            ibOrderID=ibOrderID,
            ibExecID=ibExecID,
            transactionID=transactionID,
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


def resolve_trades(obj, info, symbol: str = "") -> Dict:
    try:
        trades = [x.to_dict() for x in Trade.query.all()]
        payload = {"success": True, "trades": trades}
    except Exception as e:
        payload = {"success": False, "errors": [str(e)]}
    return payload


query = ObjectType("Query")
query.set_field("trades", resolve_trades)


mutation = ObjectType("Mutation")
mutation.set_field("createTrade", resolve_create_trade)


type_defs = load_schema_from_path("api/schema.graphql")


schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)
