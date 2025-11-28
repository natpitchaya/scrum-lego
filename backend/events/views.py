from rest_framework import generics
from django.shortcuts import render
from django.db.models import Q
from .models import Event
from .serializers import EventSerializer


def events_home(request):
    """Render the HTML page for browsing events"""
    return render(request, 'events_list.html')


def search_events_page(request):
    """Render the search and filter page for events"""
    return render(request, 'search_events.html')


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from django.core.management import call_command
import io

def home(request):
    """Homepage with API documentation"""
    return render(request, 'home.html')


def ab_testing_page(request):
    """Render the A/B testing dashboard page"""
    return render(request, 'ab_testing.html')


def analytics_page(request):
    """Render the Google Analytics dashboard page"""
    return render(request, 'analytics.html')

@csrf_exempt
def fetch_events_view(request):
    """Trigger event fetching manually via web interface"""
    if request.method == 'POST':
        try:
            # Capture command output
            out = io.StringIO()
            call_command('fetch_events', stdout=out)
            output = out.getvalue()
            return JsonResponse({
                'status': 'success',
                'message': 'Events fetched successfully',
                'output': output,
                'event_count': Event.objects.count()
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    # GET request - show current stats
    return JsonResponse({
        'event_count': Event.objects.count(),
        'som_count': Event.objects.filter(source='SOM').count(),
        'ysph_count': Event.objects.filter(source='YSPH').count(),
        'message': 'Send POST request to /fetch/ to trigger event fetching'
    })

class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        queryset = Event.objects.all()
        
        # Filter by source (organization)
        source = self.request.query_params.get('source', None)
        if source:
            queryset = queryset.filter(source=source)
        
        # Filter by keyword search (in title and description)
        keyword = self.request.query_params.get('keyword', None)
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | 
                Q(description__icontains=keyword)
            )
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_time__lte=end_date)
        
        return queryset
