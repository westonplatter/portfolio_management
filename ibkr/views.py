from typing import List, Dict, Any

from django.views.generic.edit import UpdateView

from ibkr.models import Group, Trade
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from ibkr.forms import GroupForm, TradeForm


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


class TradeListView(ListView):
    model = Trade
    template_name = "trades/list.html"
    paginate_by = 100

    def get_queryset(self):
        qs = Trade.objects

        symbol = self.request.GET.get('symbol', None)
        if symbol:
            qs = qs.filter(symbol__icontains=symbol)

        qs = qs.prefetch_related("groups")
        qs = qs.order_by("-executed_at")
        return qs



class TradeDetailView(DetailView, UpdateView):
    model = Trade
    template_name = "trades/detail.html"
    success_url = "/ibkr/trades/"
    form_class = TradeForm
