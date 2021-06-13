from ibkr.models import Trade
import django_filters
from django_filters import FilterSet


class TradeListFilterSet(FilterSet):
    ungrouped = django_filters.BooleanFilter(field_name='groups', lookup_expr='isnull', label='Ungrouped?')

    class Meta:
        model = Trade
        fields = {
            'symbol': ['icontains'],
            'underlying_symbol': ['icontains'],
            'description': ['icontains'],
        }

