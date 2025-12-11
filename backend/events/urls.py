from django.urls import path
from .views import EventListView, home, fetch_events_view, search_events_page, analytics_page, abtest_endpoint, record_click

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_events_page, name='search-events'),
    path('analytics/', analytics_page, name='analytics'),
    path('7232f7d/', abtest_endpoint, name='abtest-endpoint'),  # SHA1 hash of 'swift-canyon'
    path('api/events/', EventListView.as_view(), name='event-list'),
    path('api/record-click/', record_click, name='record-click'),
    path('fetch/', fetch_events_view, name='fetch-events'),
]
