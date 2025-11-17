from django.urls import path
from .views import EventListView, home, fetch_events_view, search_events_page

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_events_page, name='search-events'),
    path('api/events/', EventListView.as_view(), name='event-list'),
    path('fetch/', fetch_events_view, name='fetch-events'),
]
