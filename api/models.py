from api.extensions import db
from enum import Enum
from pydantic_sqlalchemy import sqlalchemy_to_pydantic


class Trade(db.Model):
    __tablename__ = "trades"
    __table_args__ = (
        db.UniqueConstraint("transactionId", name="unique_transaction_id"),
    )
    # primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # fields
    accountAlias = db.Column(db.String)
    accountId = db.Column(db.String)
    assetCategory = db.Column(db.String)
    buySell = db.Column(db.String)
    conId = db.Column(db.String)
    closePrice = db.Column(db.Float)
    dateTime = db.Column(db.String)
    description = db.Column(db.String)
    expiry = db.Column(db.String)
    fifoPnlRealized = db.Column(db.Float)
    fxPnl = db.Column(db.Float)
    ibCommission = db.Column(db.Float)
    ibExecId = db.Column(db.String)
    ibOrderId = db.Column(db.String)
    mtmPnl = db.Column(db.Float)
    multiplier = db.Column(db.Integer)
    netCash = db.Column(db.Float)
    openCloseIndicator = db.Column(db.String)
    proceeds = db.Column(db.Float)
    putCall = db.Column(db.String)
    quantity = db.Column(db.Float)
    strike = db.Column(db.String)
    symbol = db.Column(db.String)
    tradeDate = db.Column(db.String)
    tradeId = db.Column(db.String)
    tradePrice = db.Column(db.Float)
    transactionId = db.Column(db.String)
    underlyingSymbol = db.Column(db.String)
    notes = db.Column(db.String)

    def to_dict(self):
        return PydanticTrade.from_orm(self)


PydanticTrade = sqlalchemy_to_pydantic(Trade)
