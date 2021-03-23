from django.db import models
from django.db.models.fields import reverse_related


class BaseModelMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Contract(models.Model, BaseModelMixin):
    con_id = models.IntegerField()


char_field_defaults = dict(max_length=255, null=True)
int_field_defaults = dict(null=True)
class Trade(models.Model, BaseModelMixin):
    account_id = models.IntegerField(**int_field_defaults)
    asset_category = models.CharField(**char_field_defaults)
    symbol = models.CharField(**char_field_defaults)
    description = models.CharField(**char_field_defaults)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, related_name='contract', null=True)
    security_id = models.CharField(**char_field_defaults)
    security_id_type = models.CharField(**char_field_defaults)
    cusip = models.IntegerField(**int_field_defaults)
    isin = models.CharField(**char_field_defaults)
    listing_exchange = models.CharField(**char_field_defaults)
    underlying_contract = models.ForeignKey('Contract', on_delete=models.CASCADE, related_name='underlying_contract', null=True)
    underlying_symbol = models.CharField(null=True, max_length=20)
    underlying_security_id = models.CharField(**char_field_defaults)
    underlying_listing_exchange = models.CharField(**char_field_defaults)
    issuer = models.CharField(**char_field_defaults)
    multiplier = models.IntegerField(**int_field_defaults)
    strike = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10, default=None)
    expiry = models.DateTimeField(null=True, blank=True, default=None)

    # other fields

    trade_id = models.IntegerField()
    transaction_id = models.IntegerField(**int_field_defaults)


