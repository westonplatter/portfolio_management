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
    ordering = ['active', 'name']

class GroupDetailView(DetailView, UpdateView):
    model = Group
    template_name = "groups/detail.html"
    form_class = GroupForm
    success_url = "/ibkr/groups/"

class TradeListView(ListView):
    model = Trade
    ordering = ['-executed_at']
    template_name = "trades/list.html"
    paginate_by = 100

    def execute_query(self):
        return Trade.objects.all().prefetch_related('group')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["trades"] = Trade.objects.all()
        return context


class TradeDetailView(DetailView, UpdateView):
    model = Trade
    template_name = "trades/detail.html"
    success_url = "/ibkr/trades/"
    form_class = TradeForm
