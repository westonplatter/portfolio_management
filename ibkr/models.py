from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import reverse_related


char_field_defaults = dict(max_length=255, null=True)
int_field_defaults = dict(null=True)
decimal_field_defaults = dict(max_digits=16, decimal_places=4, null=True)

class BaseModelMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Contract(models.Model, BaseModelMixin):
    con_id = models.IntegerField()


class Trade(models.Model, BaseModelMixin):
    transaction_id = models.BigIntegerField(**int_field_defaults)
    account_id = models.CharField(**char_field_defaults)

    open_close_indicator = models.CharField(**char_field_defaults)
    fifo_pnl_realized = models.DecimalField(**decimal_field_defaults)
    fx_pnl = models.DecimalField(**decimal_field_defaults)
    mtm_pnl = models.DecimalField(**decimal_field_defaults)
    buy_sell = models.CharField(**char_field_defaults)

    executed_at = models.DateTimeField(null=False)

    # other fields

    asset_category = models.CharField(**char_field_defaults)
    symbol = models.CharField(**char_field_defaults)
    description = models.CharField(**char_field_defaults)
    contract = models.ForeignKey(
        "Contract", on_delete=models.CASCADE, related_name="contract", null=True
    )
    security_id = models.CharField(**char_field_defaults)
    security_id_type = models.CharField(**char_field_defaults)
    cusip = models.IntegerField(**int_field_defaults)
    isin = models.CharField(**char_field_defaults)
    listing_exchange = models.CharField(**char_field_defaults)
    underlying_contract = models.ForeignKey(
        "Contract",
        on_delete=models.CASCADE,
        related_name="underlying_contract",
        null=True,
    )
    underlying_symbol = models.CharField(null=True, max_length=20)
    underlying_security_id = models.CharField(**char_field_defaults)
    underlying_listing_exchange = models.CharField(**char_field_defaults)
    issuer = models.CharField(**char_field_defaults)
    multiplier = models.DecimalField(
        null=True, blank=True, decimal_places=0, max_digits=6, default=None
    )
    strike = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=10, default=None
    )
    expiry = models.DateTimeField(null=True, blank=True, default=None)
    trade_id = models.BigIntegerField(**int_field_defaults)


class Group(models.Model, BaseModelMixin):
    name = models.CharField(**char_field_defaults)

    @property
    def trades(self):
        group_trades = GroupTrade.objects.filter(group_id=self.id).all()
        trade_ids = [x.trade_id for x in group_trades]
        return Trade.objects.filter(id__in=trade_ids)

    @property
    def trades_realized_pnl(self):
        return sum([x.fifo_pnl_realized for x in self.trades])

    @property
    def trades_mtm_pnl(self):
        return sum([x.mtm_pnl for x in self.trades])


class GroupTrade(models.Model, BaseModelMixin):
    group = models.ForeignKey(Group, on_delete=CASCADE)
    trade = models.ForeignKey(Trade, on_delete=CASCADE)
