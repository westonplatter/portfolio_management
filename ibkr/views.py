from ibkr.models import Group
from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.

class GroupListView(ListView):
    model = Group
    paginate_by = 100
    template_name = 'groups/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context

