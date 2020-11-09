import os

from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    graphql_sync,
    snake_case_fallback_resolvers,
    ObjectType,
    QueryType,
)
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


query = ObjectType("Query")
mutation = ObjectType("Mutation")


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:@localhost:5432/portfolio_manager_dev"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String)
    tradeID = db.Column(db.String)
    ibOrderID = db.Column(db.String)
    ibExecID = db.Column(db.String)
    transactionID = db.Column(db.String)
    accountId= db.Column(db.String)
    underlyingSymbol= db.Column(db.String)
    description= db.Column(db.String)
    multiplier= db.Column(db.Integer)
    strike= db.Column(db.String)
    expiry= db.Column(db.String)
    putCall= db.Column(db.String)
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


db.create_all()


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

def resolve_trades(obj, info):
    try:
        trades = [x.to_dict() for x in Trade.query.all()]
        payload = {"success": True, "trades": trades}
    except Exception as e:
        payload = {"success": False, "errors": [str(e)]}
    return payload


mutation.set_field("createTrade", resolve_create_trade)

query.set_field("trades", resolve_trades)

type_defs = load_schema_from_path("schema.graphql")

schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)
