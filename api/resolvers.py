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


def execute_get_all_results(query: str, params: Dict = {}) -> List[Dict]:
    with db.engine.connect() as con:
        res = con.execute(query, **params).fetchall()
        results = [dict(row) for row in res]
        return results


def resolve_accounts(obj, info) -> Dict:
    try:
        sql_query = """
      select "accountId"
      from trades
      group by "accountId"
    """
        accounts = execute_get_all_results(sql_query)
        total = len(accounts)
        payload = {"success": True, "accounts": accounts, "total": total}
    except Exception as e:
        payload = {"success": False, "errors": [str(e)]}
    return payload


def resolve_create_trade(
    obj,
    info,
    assetCategory: str = None,
    symbol: str = None,
    conId=None,
    tradeId: str = None,
    ibOrderId: str = None,
    ibExecId: str = None,
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
    notes: str = None,
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
            notes=notes,
        )
        db.session.add(trade)
        db.session.commit()
        payload = {"success": True, "trade": trade.to_dict()}
    except Exception as e:
        payload = {"success": False, "errors": [str(e)]}
    return payload


def resolve_trades(
    obj,
    info,
    symbols: List[str] = [],
    underlyingSymbols: List[str] = [],
    accountIds: List[str] = [],
    openClose: str = "C",
    pageSize: int = 100,
    pageIndex: int = 0,
) -> Dict:
    try:
        query = Trade.query.filter(Trade.id > 0)

        # apply filters
        if openClose:
          query = query.filter(Trade.openCloseIndicator == openClose)

        if len(symbols) > 0:
          query = query.filter(Trade.symbols.in_(symbols))

        if len(underlyingSymbols) > 0:
          query = query.filter(Trade.underlyingSymbol.in_(underlyingSymbols))

        if len(accountIds) > 0:
          query = query.filter(Trade.accountId.in_(accountIds))

        # apply orderings
        query = query.order_by(Trade.dateTime.desc())

        # apply pagination and offsets
        trades = query.limit(pageSize).all()

        trades = [x.to_dict() for x in trades]
        total_count = Trade.query.count()
        payload = {"success": True, "trades": trades, "totalCount": total_count}

    except Exception as e:
        payload = {"success": False, "errors": [str(e)]}
    return payload


# queries
query = ObjectType("Query")
query.set_field("trades", resolve_trades)
query.set_field("accounts", resolve_accounts)

# mutations
mutation = ObjectType("Mutation")
mutation.set_field("createTrade", resolve_create_trade)

# connect queries and mutations to schema
type_defs = load_schema_from_path("api/schema.graphql")
schema = make_executable_schema(type_defs, query, mutation)
