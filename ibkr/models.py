from django.db import models


class BaseModelMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Contract(models.Model, BaseModelMixin):
    con_id = models.IntegerField()


class Trade(models.Model, BaseModelMixin):
    account_id = models.IntegerField()
    asset_category = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)


