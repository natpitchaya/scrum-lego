from django.contrib import admin
from django.urls import path, include
from events.views import events_home

urlpatterns = [
    path('', events_home, name='home'),  # Home page
    path('admin/', admin.site.urls),
    path('api/events/', include('events.urls')),
]
