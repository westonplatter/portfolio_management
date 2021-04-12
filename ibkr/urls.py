from django.urls import path

from ibkr.views import GroupListView

app_name = "ibkr"

urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group-list'),
]
