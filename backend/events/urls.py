from django.urls import path
from .views import EventListView, home, fetch_events_view, search_events_page, ab_testing_page, analytics_page, abtest_endpoint

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_events_page, name='search-events'),
    path('ab-testing/', ab_testing_page, name='ab-testing'),
    path('analytics/', analytics_page, name='analytics'),
    path('7232f7d/', abtest_endpoint, name='abtest-endpoint'),  # SHA1 hash of 'swift-canyon'
    path('api/events/', EventListView.as_view(), name='event-list'),
    path('fetch/', fetch_events_view, name='fetch-events'),
]
