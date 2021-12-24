from typing import Any, Dict, List, T

import django_filters
import django_filters.views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from ibkr.filter_sets import GroupListFilterSet, TradeListFilterSet
from ibkr.forms import GroupForm, TradeForm
from ibkr.models import Group, Trade


def get_distinct_account_ids(user_id: int):
    trades = Trade.objects.filter(user_id=user_id).values("account_id").distinct()
    account_ids = [x["account_id"] for x in trades]
    return account_ids


class GroupListView(LoginRequiredMixin, django_filters.views.FilterView):
    model = Group
    paginate_by = 100
    template_name = "groups/list.html"
    ordering = ["account_id", "-active", "name"]
    filterset_class = GroupListFilterSet

    def get_queryset(self) -> QuerySet[T]:
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class GroupsCreateView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = "groups/create.html"
    form_class = GroupForm
    success_url = reverse_lazy("ibkr:group-list")

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["account_id_choices"] = get_distinct_account_ids(self.request.user.id)
        return kwargs

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class GroupDetailView(LoginRequiredMixin, DetailView, UpdateView):
    model = Group
    template_name = "groups/detail.html"
    form_class = GroupForm
    success_url = reverse_lazy("ibkr:group-list")

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["account_id_choices"] = get_distinct_account_ids(self.request.user.id)
        return kwargs


class TradeListView(LoginRequiredMixin, django_filters.views.FilterView):
    model = Trade
    template_name = "trades/list.html"
    paginate_by = 100
    filterset_class = TradeListFilterSet
    ordering = ["-executed_at"]

    def get_queryset(self) -> QuerySet[T]:
        qs = super().get_queryset()  # to work with django-filters
        qs = qs.filter(user=self.request.user)
        qs = qs.prefetch_related("groups")
        return qs


class TradeDetailView(LoginRequiredMixin, DetailView, UpdateView):
    model = Trade
    template_name = "trades/detail.html"
    success_url = reverse_lazy("ibkr:trade-list")
    form_class = TradeForm

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["group_id_choices"] = self.possible_group_ids(self.object.account_id)
        return kwargs

    @staticmethod
    def possible_group_ids(account_id: str) -> List[str]:
        return Group.objects.filter(account_id=account_id).values("id")
