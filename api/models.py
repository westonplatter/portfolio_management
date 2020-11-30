from api.extensions import db
from enum import Enum


class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String)
    tradeID = db.Column(db.String)
    ibOrderID = db.Column(db.String)
    ibExecID = db.Column(db.String)
    transactionID = db.Column(db.String)
    accountId = db.Column(db.String)
    underlyingSymbol = db.Column(db.String)
    description = db.Column(db.String)
    multiplier = db.Column(db.Integer)
    strike = db.Column(db.String)
    expiry = db.Column(db.String)
    putCall = db.Column(db.String)
    dateTime = db.Column(db.String)
    tradeDate = db.Column(db.String)
    quantity = db.Column(db.Float)
    tradePrice = db.Column(db.Float)
    proceeds = db.Column(db.Float)
    ibCommission = db.Column(db.Float)
    netCash = db.Column(db.Float)
    closePrice = db.Column(db.Float)
    openCloseIndicator = db.Column(db.String)
    fifoPnlRealized = db.Column(db.Float)
    fxPnl = db.Column(db.Float)
    mtmPnl = db.Column(db.Float)
    buySell = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "tradeID": self.tradeID,
            "ibOrderID": self.ibOrderID,
            "ibExcID": self.ibExecID,
            "transactionID": self.transactionID,
            "accountId": self.accountId,
            "underlyingSymbol": self.underlyingSymbol,
            "description": self.description,
            "multiplier": self.multiplier,
            "strike": self.strike,
            "expiry": self.expiry,
            "putCall": self.putCall,
            "dateTime": self.dateTime,
            "tradeDate": self.tradeDate,
            "quantity": self.quantity,
            "tradePrice": self.tradePrice,
            "proceeds": self.proceeds,
            "ibCommission": self.ibCommission,
            "netCash": self.netCash,
            "closePrice": self.closePrice,
            "openCloseIndicator": self.openCloseIndicator,
            "fifoPnlRealized": self.fifoPnlRealized,
            "fxPnl": self.fxPnl,
            "mtmPnl": self.mtmPnl,
            "buySell": self.buySell,
        }
