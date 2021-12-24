from typing import Optional

import graphene
from graphene_django import DjangoObjectType

from ibkr.models import Contract, Trade
from ingest.schema_types import BigInt

DEFAULT_USER_ID = 1


class TradeType(DjangoObjectType):
    transaction_id = graphene.Field(BigInt)

    class Meta:
        model = Trade
        fields = ("id", "transaction_id", "account_id")
        # TODO create a serializer to send down trades and the groups they are apart of
        # for Main Fund, I want to be able to see all trades in the Crude Long Carry Position.


class ContractType(DjangoObjectType):
    class Meta:
        model = Contract
        fields = ("id", "con_id")


class Query(graphene.ObjectType):
    trades = graphene.List(TradeType)

    trades_by_account_id = graphene.List(
        TradeType, accountId=graphene.String(required=True)
    )

    lastTradeDate = graphene.String(accountId=graphene.String())

    def resolve_trades(root, info):
        return Trade.objects.all()

    def resolve_trades_by_account_id(root, info, accountId: str):
        return Trade.objects.filter(account_id=accountId)

    def resolve_lastTradeDate(root, info, accountId: Optional[str] = None):
        qs = Trade.objects
        if accountId:
            qs = qs.filter(account_id=accountId)

        if qs.count() == 0:
            return None

        latest_trade = qs.latest("executed_at")
        return latest_trade.executed_at.strftime("%Y-%m-%d")


class TradeMutation(graphene.Mutation):
    class Arguments:
        transactionId = BigInt(required=True)
        executedAt = graphene.DateTime(required=True)
        # optional
        tradeId = BigInt(required=False)
        accountId = graphene.String(required=False)
        assetCategory = graphene.String(required=False)
        symbol = graphene.String(required=False)
        underlyingSymbol = graphene.String(required=False)
        openCloseIndicator = graphene.String(required=False)
        fifoPnlRealized = graphene.Float(required=False)
        fxPnl = graphene.Float(required=False)
        mtmPnl = graphene.Float(required=False)
        buySell = graphene.String(required=False)
        description = graphene.String(required=False)
        expiry = graphene.DateTime(required=False)
        strike = graphene.Float(required=False)
        multiplier = graphene.Float(required=False)

    trade = graphene.Field(TradeType)

    @classmethod
    def mutate(
        cls,
        root,
        info,
        transactionId,
        accountId=None,
        assetCategory=None,
        symbol=None,
        underlyingSymbol=None,
        openCloseIndicator=None,
        fifoPnlRealized=None,
        fxPnl=None,
        mtmPnl=None,
        buySell=None,
        executedAt=None,
        description=None,
        tradeId=None,
        expiry=None,
        strike=None,
        multiplier=None,
    ):
        defaults = dict(
            user_id=DEFAULT_USER_ID,
            account_id=accountId,
            asset_category=assetCategory,
            symbol=symbol,
            underlying_symbol=underlyingSymbol,
            open_close_indicator=openCloseIndicator,
            fifo_pnl_realized=fifoPnlRealized,
            fx_pnl=fxPnl,
            mtm_pnl=mtmPnl,
            buy_sell=buySell,
            executed_at=executedAt,
            description=description,
            trade_id=tradeId,
            expiry=expiry,
            strike=strike,
            multiplier=multiplier,
        )
        kwargs = dict(transaction_id=transactionId)
        trade, _ = Trade.objects.get_or_create(**kwargs, defaults=defaults)
        return TradeMutation(trade=trade)


class Mutation(graphene.ObjectType):
    create_or_get_trade = TradeMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
