from django.test import TestCase, Client
from django.urls import reverse
from .models import Event, ABTestVisit
from django.utils import timezone
from datetime import timedelta


class EventModelTest(TestCase):
    """Test cases for Event model"""

    def setUp(self):
        self.event = Event.objects.create(
            title='Test Event',
            description='Test description',
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=2),
            location='Test Location',
            source='SOM',
            url='https://example.com/event',
            uid='test-uid-123',
        )

    def test_create_event(self):
        """Test event creation"""
        self.assertEqual(self.event.title, 'Test Event')
        self.assertEqual(self.event.source, 'SOM')
        self.assertEqual(self.event.uid, 'test-uid-123')

    def test_event_str(self):
        """Test event string representation"""
        self.assertTrue(str(self.event).startswith('Test Event'))

    def test_event_ordering(self):
        """Test events are ordered by start_time"""
        future_event = Event.objects.create(
            title='Future Event',
            start_time=timezone.now() + timedelta(days=1),
            uid='future-uid',
        )
        events = Event.objects.all()
        self.assertEqual(events[0], self.event)
        self.assertEqual(events[1], future_event)


class ABTestVisitModelTest(TestCase):
    """Test cases for ABTestVisit model"""

    def test_create_abtest_visit(self):
        """Test A/B test visit creation"""
        visit = ABTestVisit.objects.create(
            session_key='test-session-123',
            variant='A',
            ip_address='127.0.0.1',
            user_agent='Mozilla/5.0',
        )
        self.assertEqual(visit.variant, 'A')
        self.assertEqual(visit.session_key, 'test-session-123')

    def test_abtest_visit_str(self):
        """Test A/B test visit string representation"""
        visit = ABTestVisit.objects.create(
            session_key='test-session-456',
            variant='B',
        )
        self.assertIn('Variant B', str(visit))


class ViewsTest(TestCase):
    """Test cases for views"""

    def setUp(self):
        self.client = Client()
        # Create test events
        Event.objects.create(
            title='SOM Event',
            description='Test SOM event',
            start_time=timezone.now(),
            source='SOM',
            uid='som-uid-1',
        )
        Event.objects.create(
            title='YSPH Event',
            description='Test YSPH event',
            start_time=timezone.now() + timedelta(days=1),
            source='YSPH',
            uid='ysph-uid-1',
        )

    def test_home_page(self):
        """Test home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yale Events Calendar')

    def test_search_page(self):
        """Test search page loads successfully"""
        response = self.client.get(reverse('search-events'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search Yale Events')

    def test_analytics_page(self):
        """Test analytics page loads successfully"""
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Google Analytics')

    def test_abtest_endpoint(self):
        """Test A/B test endpoint loads successfully"""
        response = self.client.get(reverse('abtest-endpoint'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'swift-canyon')
        self.assertContains(response, 'id="abtest"')
        # Check that button shows either kudos or thanks
        content = response.content.decode()
        self.assertTrue('kudos' in content or 'thanks' in content)

    def test_abtest_endpoint_session_consistency(self):
        """Test A/B test variant is consistent per session"""
        # First request
        response1 = self.client.get(reverse('abtest-endpoint'))
        content1 = response1.content.decode()

        # Second request with same session
        response2 = self.client.get(reverse('abtest-endpoint'))
        content2 = response2.content.decode()

        # Check variant is the same
        variant1 = 'kudos' if 'kudos' in content1 else 'thanks'
        variant2 = 'kudos' if 'kudos' in content2 else 'thanks'
        self.assertEqual(variant1, variant2)

    def test_event_list_api(self):
        """Test event list API endpoint"""
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 2)

    def test_event_list_api_filter_by_source(self):
        """Test filtering events by source"""
        response = self.client.get(reverse('event-list') + '?source=SOM')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['source'], 'SOM')

    def test_event_list_api_search_by_keyword(self):
        """Test searching events by keyword"""
        response = self.client.get(reverse('event-list') + '?keyword=YSPH')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertIn('YSPH', data['results'][0]['title'])

    def test_fetch_events_view_get(self):
        """Test fetch events view GET request"""
        response = self.client.get(reverse('fetch-events'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('event_count', data)
        self.assertEqual(data['event_count'], 2)


class URLPatternsTest(TestCase):
    """Test URL patterns are correctly configured"""

    def test_home_url_resolves(self):
        """Test home URL resolves correctly"""
        url = reverse('home')
        self.assertEqual(url, '/')

    def test_search_url_resolves(self):
        """Test search URL resolves correctly"""
        url = reverse('search-events')
        self.assertEqual(url, '/search/')

    def test_analytics_url_resolves(self):
        """Test analytics URL resolves correctly"""
        url = reverse('analytics')
        self.assertEqual(url, '/analytics/')

    def test_abtest_endpoint_url_resolves(self):
        """Test A/B test endpoint URL resolves correctly"""
        url = reverse('abtest-endpoint')
        self.assertEqual(url, '/7232f7d/')

    def test_api_events_url_resolves(self):
        """Test API events URL resolves correctly"""
        url = reverse('event-list')
        self.assertEqual(url, '/api/events/')
