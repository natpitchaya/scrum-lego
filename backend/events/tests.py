from django.test import TestCase
from .models import Event
from django.utils import timezone


class EventModelTest(TestCase):
    def test_create_event(self):
        e = Event.objects.create(
            title='Test',
            description='desc',
            start_time=timezone.now(),
            uid='test-uid',
        )
        self.assertEqual(str(e).startswith('Test'), True)
