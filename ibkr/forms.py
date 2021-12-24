from django import forms

from ibkr.models import Group, Trade


class GroupNameChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name}"


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ["groups"]

    def __init__(self, *args, **kwargs):
        ids = kwargs.pop("group_id_choices")
        account_active_groups = Group.objects.filter(id__in=ids, active=True).order_by(
            "name"
        )

        super(TradeForm, self).__init__(*args, **kwargs)

        self.fields["groups"] = GroupNameChoiceField(
            queryset=account_active_groups,
            required=False,
            label="",
        )


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
