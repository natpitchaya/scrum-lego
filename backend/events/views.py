from rest_framework import generics
from django.shortcuts import render
from .models import Event
from .serializers import EventSerializer


def events_home(request):
    """Render the HTML page for browsing events"""
    return render(request, 'events_list.html')


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all().order_by('start_time')
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        source = self.request.query_params.get('source', None)
        if source:
            queryset = queryset.filter(source=source)
        return queryset
