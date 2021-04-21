import datetime
from ibkr.models import Trade, Group


def create_trade(_id):
    return Trade.objects.create(
        account_id=123, transaction_id=_id, executed_at=datetime.datetime.now()
    )


def test_trades_group(db):
    trade1 = create_trade(123)
    trade2 = create_trade(890)
    group = Group.objects.create(name="group-abc")

    assert group.trades.count() == 0

    group.trades.add(trade1)
    group.trades.add(trade2)

    assert group.trades.count() == 2
    assert trade1.groups.count() == 1


def test_x(db):

    Group.objects.count() == 0
