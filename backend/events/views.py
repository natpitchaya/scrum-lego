from rest_framework import generics
from django.shortcuts import render
from .models import Event
from .serializers import EventSerializer


def events_home(request):
    """Render the HTML page for browsing events"""
    return render(request, 'events_list.html')


from django.shortcuts import render
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

def home(request):
    """Homepage with API documentation"""
    return render(request, 'home.html')

class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        queryset = Event.objects.all()
        source = self.request.query_params.get('source', None)
        if source:
            queryset = queryset.filter(source=source)
        return queryset
