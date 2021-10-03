import django_filters
from django_filters import FilterSet

from ibkr.models import Group, Trade


class TradeListFilterSet(FilterSet):
    ungrouped = django_filters.BooleanFilter(
        field_name="groups", lookup_expr="isnull", label="Ungrouped?"
    )

    # TODO should be authentication specific
    choices = [
        (x["account_id"], x["account_id"])
        for x in Trade.objects.values("account_id").distinct()
    ]
    account_id = django_filters.ChoiceFilter(choices=choices, label="Account Alias")

    class Meta:
        model = Trade
        fields = {
            "symbol": ["icontains"],
            "underlying_symbol": ["icontains"],
            "description": ["icontains"],
        }

class GroupListFilterSet(FilterSet):

    # TODO should be authentication specific
    choices = [
        (x["account_id"], x["account_id"])
        for x in Trade.objects.values("account_id").distinct()
    ]
    account_id = django_filters.ChoiceFilter(choices=choices, label="Account Alias")
    class Meta:
        model = Group
        fields = {
            "name": ["icontains"],
        }
