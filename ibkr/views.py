from typing import Any, Dict, List

import django_filters
import django_filters.views
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView

from ibkr.forms import GroupForm, TradeForm
from ibkr.models import Group, Trade
from ibkr.filter_sets import TradeListFilterSet


class GroupListView(ListView):
    model = Group
    paginate_by = 100
    template_name = "groups/list.html"
    ordering = ["active", "name"]


class GroupDetailView(DetailView, UpdateView):
    model = Group
    template_name = "groups/detail.html"
    form_class = GroupForm
    success_url = "/ibkr/groups/"


class TradeListView(django_filters.views.FilterView):
    model = Trade
    template_name = "trades/list.html"
    paginate_by = 100
    filterset_class = TradeListFilterSet
    ordering = ["-executed_at"]

    def get_queryset(self):
        qs = super().get_queryset() # to work with django-filters
        qs = qs.prefetch_related("groups")
        return qs


class TradeDetailView(DetailView, UpdateView):
    model = Trade
    template_name = "trades/detail.html"
    success_url = "/ibkr/trades/"
    form_class = TradeForm
