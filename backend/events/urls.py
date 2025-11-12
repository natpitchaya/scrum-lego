from django.urls import path
from .views import EventListView, home

urlpatterns = [
    path('', home, name='home'),
    path('api/events/', EventListView.as_view(), name='event-list'),
]
