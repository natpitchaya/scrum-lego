import hashlib
import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from dateutil import parser as dateparser
import requests
from bs4 import BeautifulSoup
from events.models import Event
import urllib.parse
import re


def make_uid(url: str, title: str = '') -> str:
    base = (url or title or '')
    return hashlib.sha1(base.encode('utf-8')).hexdigest()


def parse_date(text: str):
    """Parse a date string and return a timezone-aware datetime object."""
    try:
        dt = dateparser.parse(text)
        if dt:
            # Make timezone-aware if naive
            if dt.tzinfo is None:
                dt = timezone.make_aware(dt)
        return dt
    except Exception:
        return None


def fetch_yale_som():
    """Heuristic scraper for Yale SOM events. Adjust selectors as needed."""
    url = 'https://som.yale.edu/events'
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    items = []
    # try common structures: articles, divs with event class, list items
    candidates = soup.find_all(['article', 'div', 'li'])
    for c in candidates:
        classes = ' '.join(c.get('class') or [])
        if 'event' in classes.lower() or 'listing' in classes.lower() or c.find('time') or c.find('a'):
            title_tag = c.find(['h1', 'h2', 'h3', 'a'])
            title = (title_tag.get_text(strip=True) if title_tag else '').strip()
            link = None
            if title_tag and title_tag.name == 'a':
                link = title_tag.get('href')
            else:
                a = c.find('a')
                if a:
                    link = a.get('href')
            date_text = ''
            time_tag = c.find('time')
            if time_tag:
                date_text = time_tag.get_text(' ', strip=True)
            else:
                # maybe there's a date span
                ds = c.find(class_=lambda v: v and 'date' in v.lower())
                if ds:
                    date_text = ds.get_text(' ', strip=True)
            items.append({'title': title, 'url': requests.compat.urljoin(url, link) if link else None, 'date_text': date_text, 'source': 'Yale SOM', 'description': ''})
    return items


def fetch_ysph():
    """Heuristic scraper for Yale School of Public Health events (YSPH)."""
    url = 'https://publichealth.yale.edu/events/'
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    items = []
    candidates = soup.find_all(['article', 'div', 'li'])
    for c in candidates:
        classes = ' '.join(c.get('class') or [])
        if 'event' in classes.lower() or 'listing' in classes.lower() or c.find('time') or c.find('a'):
            title_tag = c.find(['h1', 'h2', 'h3', 'a'])
            title = (title_tag.get_text(strip=True) if title_tag else '').strip()
            link = None
            if title_tag and title_tag.name == 'a':
                link = title_tag.get('href')
            else:
                a = c.find('a')
                if a:
                    link = a.get('href')
            date_text = ''
            time_tag = c.find('time')
            if time_tag:
                date_text = time_tag.get_text(' ', strip=True)
            else:
                ds = c.find(class_=lambda v: v and 'date' in v.lower())
                if ds:
                    date_text = ds.get_text(' ', strip=True)
            items.append({'title': title, 'url': requests.compat.urljoin(url, link) if link else None, 'date_text': date_text, 'source': 'YSPH', 'description': ''})
    return items


def fetch_som_api(limit: int = 200):
    """Use the CampusGroups mobile webservice to fetch structured JSON for Yale SOM events."""
    base = 'https://groups.som.yale.edu'
    url = f'{base}/mobile_ws/v17/mobile_events_list?range=0&limit={limit}'
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    items = []
    for obj in data:
        # Skip separators
        if obj.get('listingSeparator'):
            continue
        # fields mapping (based on observed JSON): p1=eventId, p2=eventUid, p3=eventName, p4=eventDates (HTML), p6=eventLocation, p18=eventUrl, p30=ariaEventDetails
        title = obj.get('p3') or obj.get('p1')
        dates_html = obj.get('p4') or ''
        date_text = BeautifulSoup(dates_html, 'html.parser').get_text(' ', strip=True) if dates_html else ''
        
        # Parse start and end dates from the date_text
        start_dt = None
        end_dt = None
        if date_text:
            # Date format: "Sat, Nov 1, 2025 12:00 AM – Sun, Nov 30, 2025 11:55 PM"
            parts = date_text.split('–') if '–' in date_text else date_text.split('-')
            if len(parts) >= 1:
                start_dt = parse_date(parts[0].strip())
            if len(parts) >= 2:
                end_dt = parse_date(parts[1].strip())
        
        loc = obj.get('p6') or ''
        rel = obj.get('p18') or ''
        url_full = requests.compat.urljoin(base, rel) if rel else None
        description_html = obj.get('p30') or ''
        description = BeautifulSoup(description_html, 'html.parser').get_text(' ', strip=True) if description_html else ''
        uid = obj.get('p2') or make_uid(url_full or title or date_text)
        items.append({
            'title': title, 
            'url': url_full, 
            'date_text': date_text, 
            'source': 'Yale SOM', 
            'description': description, 
            'uid': uid, 
            'location': loc,
            'start_dt': start_dt,
            'end_dt': end_dt
        })
    return items


def fetch_ysph_ics():
    """Find the site ICS feed on the YSPH calendar page and parse events from it."""
    page_url = 'https://ysph.yale.edu/yale-school-of-public-health-event-calendar/'
    resp = requests.get(page_url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    a = soup.find('a', href=lambda h: h and 'feed-organization-events-download' in h)
    if not a:
        # fallback to the main events page
        raise RuntimeError('YSPH ICS feed link not found on page')
    href = a.get('href')
    ical_base = requests.compat.urljoin(page_url, href.split('?')[0])
    # build start/end dates for one year range
    now = timezone.now()
    start = (now - timezone.timedelta(days=1)).strftime('%m/%d/%Y %H:%M:%S')
    end = (now + timezone.timedelta(days=365)).strftime('%m/%d/%Y %H:%M:%S')
    qs = urllib.parse.urlencode({'startDate': start, 'endDate': end})
    ical_url = ical_base + '?' + qs
    r = requests.get(ical_url, timeout=15)
    r.raise_for_status()
    raw = r.text
    items = []
    parts = raw.split('BEGIN:VEVENT')
    for seg in parts[1:]:
        lines = seg.splitlines()
        ev = {}
        # naive parse of ICS keys
        for ln in lines:
            if ln.startswith('SUMMARY:'):
                ev['title'] = ln.split('SUMMARY:', 1)[1].strip()
            elif ln.startswith('DTSTART'):
                v = ln.split(':', 1)[1].strip()
                ev['dtstart'] = parse_date(v)
            elif ln.startswith('DTEND'):
                v = ln.split(':', 1)[1].strip()
                ev['dtend'] = parse_date(v)
            elif ln.startswith('LOCATION:'):
                ev['location'] = ln.split('LOCATION:', 1)[1].strip()
            elif ln.startswith('DESCRIPTION:'):
                ev['description'] = ln.split('DESCRIPTION:', 1)[1].strip().replace('\\n', '\n')
            elif ln.startswith('UID:'):
                ev['uid'] = ln.split('UID:', 1)[1].strip()
            elif ln.startswith('URL:'):
                ev['url'] = ln.split('URL:', 1)[1].strip()
        if not ev.get('title'):
            continue
        uid = ev.get('uid') or make_uid(ev.get('url') or ev.get('title'))
        items.append({'title': ev.get('title'), 'url': ev.get('url'), 'date_text': '', 'source': 'YSPH', 'description': ev.get('description', ''), 'uid': uid, 'location': ev.get('location', ''), 'start_dt': ev.get('dtstart'), 'end_dt': ev.get('dtend')})
    return items


def fetch_yale_events_api(days: int = 365):
    """Fetch events from Yale Events calendar via Localist API."""
    url = f'https://events.yale.edu/api/2/events?days={days}'
    items = []
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    
    for entry in data.get('events', []):
        evt = entry.get('event', {})
        title = evt.get('title', 'Untitled')
        description_html = evt.get('description', '')
        description = BeautifulSoup(description_html, 'html.parser').get_text(' ', strip=True) if description_html else evt.get('description_text', '')
        
        # Get first event instance for date/time
        instances = evt.get('event_instances', [])
        start_dt = None
        end_dt = None
        if instances:
            inst = instances[0].get('event_instance', {})
            start_str = inst.get('start')
            end_str = inst.get('end')
            if start_str:
                start_dt = parse_date(start_str)
            if end_str:
                end_dt = parse_date(end_str)
        
        # Location info
        location = evt.get('location_name', '') or evt.get('location', '')
        if evt.get('room_number'):
            location = f"{location}, {evt['room_number']}".strip(', ')
        
        # URL
        event_url = evt.get('localist_url') or evt.get('url')
        
        # UID
        uid = str(evt.get('id', '')) or make_uid(event_url or title)
        
        items.append({
            'title': title,
            'url': event_url,
            'date_text': '',
            'source': 'Yale Events',
            'description': description,
            'uid': uid,
            'location': location,
            'start_dt': start_dt,
            'end_dt': end_dt
        })
    
    return items


def fetch_ysm():
    """Fetch events from Yale School of Medicine calendar by parsing embedded JSON."""
    url = 'https://medicine.yale.edu/calendar/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    resp = requests.get(url, timeout=15, headers=headers)
    resp.raise_for_status()
    
    # Extract JSON from the embedded script tag
    import json
    soup = BeautifulSoup(resp.text, 'html.parser')
    scripts = soup.find_all('script', string=re.compile('window\\[\'pageModel\'\\]'))
    
    if not scripts:
        raise RuntimeError('Could not find embedded event data on YSM calendar page')
    
    # Parse the JSON from the script tag
    script_content = scripts[0].string
    json_match = re.search(r'window\[\'pageModel\'\]\s*=\s*(\{.*?\});', script_content, re.DOTALL)
    if not json_match:
        raise RuntimeError('Could not extract JSON data from YSM calendar page')
    
    data = json.loads(json_match.group(1))
    
    items = []
    # Navigate to events in the JSON structure
    main_components = data.get('mainComponents', [])
    for component in main_components:
        if component.get('key') == 'EventsHome':
            events_data = component.get('model', {}).get('events', {}).get('collection', [])
            
            for evt in events_data:
                title = evt.get('title', 'Untitled')
                subtitle = evt.get('subTitle', '')
                if subtitle:
                    title = f"{title}: {subtitle}"
                
                description_html = evt.get('description', '')
                description = BeautifulSoup(description_html, 'html.parser').get_text(' ', strip=True) if description_html else ''
                
                # Parse dates
                start_str = evt.get('startDate')
                end_str = evt.get('endDate')
                start_dt = parse_date(start_str) if start_str else None
                end_dt = parse_date(end_str) if end_str else None
                
                # Location info
                event_location = evt.get('eventLocation', {}) or {}
                location = event_location.get('building', '')
                if event_location.get('streetAddress'):
                    location = f"{location}, {event_location['streetAddress']}".strip(', ')
                
                # URL
                detail_url = evt.get('detailsEventUrl', '')
                event_url = requests.compat.urljoin(url, detail_url) if detail_url else None
                
                # UID
                uid = str(evt.get('id', '')) or make_uid(event_url or title)
                
                items.append({
                    'title': title,
                    'url': event_url,
                    'date_text': '',
                    'source': 'Yale School of Medicine',
                    'description': description,
                    'uid': uid,
                    'location': location,
                    'start_dt': start_dt,
                    'end_dt': end_dt
                })
    
    return items


class Command(BaseCommand):
    help = 'Fetch events from configured Yale sites and upsert into DB'

    def handle(self, *args, **options):
        all_items = []
        # Prefer structured sources when available
        try:
            som = fetch_som_api()
            self.stdout.write(f'Found {len(som)} candidate items from Yale SOM API')
            all_items.extend(som)
        except Exception as e:
            self.stderr.write(f'Yale SOM API fetch failed: {e}')
            # fallback to heuristic page scrape
            try:
                som_fallback = fetch_yale_som()
                self.stdout.write(f'Found {len(som_fallback)} candidate items on Yale SOM (fallback)')
                all_items.extend(som_fallback)
            except Exception as e2:
                self.stderr.write(f'Yale SOM fallback fetch failed: {e2}')

        try:
            ysph = fetch_ysph_ics()
            self.stdout.write(f'Found {len(ysph)} candidate items from YSPH ICS')
            all_items.extend(ysph)
        except Exception as e:
            self.stderr.write(f'YSPH ICS fetch failed: {e}')
            # fallback to heuristic page scrape
            try:
                ysph_fallback = fetch_ysph()
                self.stdout.write(f'Found {len(ysph_fallback)} candidate items on YSPH (fallback)')
                all_items.extend(ysph_fallback)
            except Exception as e2:
                self.stderr.write(f'YSPH fallback fetch failed: {e2}')

        try:
            yale_events = fetch_yale_events_api()
            self.stdout.write(f'Found {len(yale_events)} candidate items from Yale Events API')
            all_items.extend(yale_events)
        except Exception as e:
            self.stderr.write(f'Yale Events API fetch failed: {e}')

        try:
            ysm = fetch_ysm()
            self.stdout.write(f'Found {len(ysm)} candidate items from Yale School of Medicine')
            all_items.extend(ysm)
        except Exception as e:
            self.stderr.write(f'Yale School of Medicine fetch failed: {e}')

        created = 0
        updated = 0
        for it in all_items:
            title = it.get('title') or 'Untitled'
            url = it.get('url')
            # prefer explicit parsed datetimes from source
            dt = it.get('start_dt') if it.get('start_dt') else parse_date(it.get('date_text') or '')
            if not dt:
                # fallback to now
                dt = timezone.now()
            uid = it.get('uid') or make_uid(url or (title + str(dt)))
            defaults = {
                'title': title,
                'description': it.get('description') or '',
                'start_time': dt,
                'location': it.get('location') or '',
                'source': it.get('source') or '',
                'url': url,
            }
            # include end_time if provided
            if it.get('end_dt'):
                defaults['end_time'] = it.get('end_dt')
            obj, was_created = Event.objects.update_or_create(
                uid=uid,
                defaults=defaults,
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f'Upserted events: created={created} updated={updated}'))
