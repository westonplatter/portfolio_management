import graphene
from graphene_django import DjangoObjectType

from ibkr.models import Trade, Contract

from graphene.types import Scalar
from graphql.language import ast
from graphene.types.scalars import MIN_INT, MAX_INT
class BigInt(Scalar):
    """
    BigInt is an extension of the regular Int field
        that supports Integers bigger than a signed
        32-bit integer.
    """
    @staticmethod
    def big_to_float(value):
        num = int(value)
        if num > MAX_INT or num < MIN_INT:
            return float(int(num))
        return num

    serialize = big_to_float
    parse_value = big_to_float

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.IntValue):
            num = int(node.value)
            if num > MAX_INT or num < MIN_INT:
                return float(int(num))
            return num

class TradeType(DjangoObjectType):
    transaction_id = graphene.Field(BigInt)
    class Meta:
        model = Trade
        fields = ("id", "transaction_id")

class ContractType(DjangoObjectType):
    class Meta:
        model = Contract
        fields = ("id", "con_id")


class Query(graphene.ObjectType):
    trades = graphene.List(TradeType)

    def resolve_trades(root, info):
        return Trade.objects.all()

class TradeMutation(graphene.Mutation):
    class Arguments:
        transactionId = BigInt(required=True)

    trade = graphene.Field(TradeType)

    @classmethod
    def mutate(cls, root, info, transactionId):

        print("\n-------------------\nhi")

        defaults = {}
        kwargs = {"transaction_id": transactionId}
        trade, _ = Trade.objects.get_or_create(**kwargs, defaults=defaults)
        return TradeMutation(trade=trade)

class Mutation(graphene.ObjectType):
    create_or_get_trade = TradeMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
