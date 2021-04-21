from django import forms

from ibkr.models import Trade, Group


class GroupNameChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name}'


class TradeForm(forms.ModelForm):
    groups = GroupNameChoiceField(
        queryset=Group.objects.filter(active=True).all().order_by("name"),
        required=False,
        label='',
    )

    class Meta:
        model = Trade
        fields = ["groups"]


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'active']
