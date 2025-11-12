from django.urls import path
from .views import EventListView, home, fetch_events_view

urlpatterns = [
    path('', home, name='home'),
    path('api/events/', EventListView.as_view(), name='event-list'),
    path('fetch/', fetch_events_view, name='fetch-events'),
]
