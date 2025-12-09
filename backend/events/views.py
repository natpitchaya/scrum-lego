import io
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.management import call_command
from rest_framework import generics
from .models import Event, ABTestVisit
from .serializers import EventSerializer


def events_home(request):
    """Render the HTML page for browsing events"""
    return render(request, 'events_list.html')


def search_events_page(request):
    """Render the search and filter page for events"""
    return render(request, 'search_events.html')


def home(request):
    """Homepage with API documentation"""
    return render(request, 'home.html')


def analytics_page(request):
    """Render the Google Analytics dashboard page with internal A/B test stats"""
    # Calculate A/B test stats
    total_visits = ABTestVisit.objects.count()

    # Variant A stats
    visits_a = ABTestVisit.objects.filter(variant='A').count()
    conversions_a = ABTestVisit.objects.filter(variant='A', converted=True).count()
    conversion_rate_a = (conversions_a / visits_a * 100) if visits_a > 0 else 0

    # Variant B stats
    visits_b = ABTestVisit.objects.filter(variant='B').count()
    conversions_b = ABTestVisit.objects.filter(variant='B', converted=True).count()
    conversion_rate_b = (conversions_b / visits_b * 100) if visits_b > 0 else 0

    context = {
        'total_visits': total_visits,
        'visits_a': visits_a,
        'conversions_a': conversions_a,
        'conversion_rate_a': round(conversion_rate_a, 1),
        'visits_b': visits_b,
        'conversions_b': conversions_b,
        'conversion_rate_b': round(conversion_rate_b, 1),
    }
    return render(request, 'analytics.html', context)


@csrf_exempt
def record_click(request):
    """Record a button click for the A/B test"""
    if request.method == 'POST':
        session_key = request.session.session_key
        if session_key:
            # Find the most recent visit for this session
            visit = ABTestVisit.objects.filter(session_key=session_key).first()
            if visit:
                visit.converted = True
                visit.save()
                return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def abtest_endpoint(request):
    """
    A/B Test endpoint at /7232f7d (sha1 hash of 'swift-canyon')
    Implements 50/50 split test with 'kudos' (Variant A) and 'thanks' (Variant B)
    """
    # Ensure session exists
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    # Check if this session already has a variant assigned
    existing_visit = ABTestVisit.objects.filter(session_key=session_key).first()

    if existing_visit:
        # Use existing variant for consistency
        variant = existing_visit.variant
    else:
        # Assign new variant (50/50 split)
        variant = 'A' if random.random() < 0.5 else 'B'

        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # Record the visit
        ABTestVisit.objects.create(
            session_key=session_key,
            variant=variant,
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

    # Set button text based on variant
    button_text = 'kudos' if variant == 'A' else 'thanks'

    # Get total views count
    total_views = ABTestVisit.objects.count()

    context = {
        'variant': f'Variant {variant}',
        'button_text': button_text,
        'total_views': total_views,
    }

    return render(request, 'abtest_endpoint.html', context)


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
                Q(title__icontains=keyword)
                | Q(description__icontains=keyword)
            )

        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date:
            queryset = queryset.filter(start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_time__lte=end_date)

        return queryset
