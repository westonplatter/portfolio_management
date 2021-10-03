from django import forms
from django.db import models

from ibkr.models import Group, Trade


class GroupNameChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name}"


class TradeForm(forms.ModelForm):
    groups = GroupNameChoiceField(
        queryset=Group.objects.filter(active=True).all().order_by("name"),
        required=False,
        label="",
    )

    class Meta:
        model = Trade
        fields = ["groups"]


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "active", "account_id"]

    def __init__(self, *args, **kwargs):
        ids = kwargs.pop("account_id_choices")
        ACCOUNT_ID_CHOICES = [("", "")]
        ACCOUNT_ID_CHOICES.extend([(x, x) for x in ids])

        super(GroupForm, self).__init__(*args, **kwargs)

        self.fields["account_id"] = forms.ChoiceField(choices=ACCOUNT_ID_CHOICES)
