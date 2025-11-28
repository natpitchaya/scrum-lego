# Yale Events Aggregator - Team Swift Canyon

A Django-based web application that aggregates and displays events from Yale School of Management (SOM) and Yale School of Public Health (YSPH). Features include event search, filtering, A/B testing, and Google Analytics integration.

## Team Members
- Nat Chairuengjitjaras
- Ted Wu
- Iris Yang
- Emily Yu

## Features

- **Event Aggregation**: Automatically fetches events from Yale SOM and YSPH
- **Search & Filter**: Advanced search by keyword, organization, and date range
- **A/B Testing**: Experimental testing endpoint with session-based variant assignment
- **Google Analytics**: Comprehensive analytics tracking across all pages
- **REST API**: RESTful API for programmatic event access
- **Admin Interface**: Django admin for event and test data management

## Technology Stack

- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL (production), SQLite (development)
- **Web Server**: Gunicorn with WhiteNoise for static files
- **Deployment**: Render.com
- **Testing**: Django TestCase with 21 comprehensive tests
- **Linting**: Flake8 for code quality

## Project Structure

```
scrum-lego/
├── backend/
│   ├── backend/          # Django project settings
│   ├── events/           # Main application
│   │   ├── management/   # Custom management commands
│   │   ├── migrations/   # Database migrations
│   │   ├── templates/    # HTML templates
│   │   ├── admin.py      # Admin interface configuration
│   │   ├── models.py     # Database models
│   │   ├── serializers.py # API serializers
│   │   ├── tests.py      # Test suite (21 tests)
│   │   ├── urls.py       # URL routing
│   │   └── views.py      # View functions
│   ├── db.sqlite3        # Development database
│   └── manage.py         # Django management script
├── .flake8               # Flake8 configuration
├── .pylintrc             # Pylint configuration
├── requirements.txt      # Python dependencies
├── build.sh              # Render build script
├── Procfile              # Render process configuration
└── README.md             # This file
```

## Installation & Setup

### Prerequisites
- Python 3.12+
- pip
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/natpitchaya/scrum-lego.git
   cd scrum-lego
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   cd backend
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Home: http://localhost:8000/
   - API: http://localhost:8000/api/events/
   - A/B Test: http://localhost:8000/7232f7d/
   - Admin: http://localhost:8000/admin/

## Testing

### Run Tests
```bash
cd backend
python manage.py test events --verbosity=2
```

### Test Coverage
- 21 comprehensive tests covering:
  - Model creation and validation
  - URL routing
  - View rendering
  - API endpoints
  - A/B testing functionality
  - Session consistency

### Run Linting
```bash
# Flake8
flake8 events/ backend/

# With statistics
flake8 events/ backend/ --statistics --count
```

## API Endpoints

### Events API
- **GET** `/api/events/` - List all events
- **GET** `/api/events/?source=SOM` - Filter by organization
- **GET** `/api/events/?keyword=research` - Search by keyword
- **GET** `/api/events/?start_date=2025-11-01&end_date=2025-11-30` - Filter by date

### Pages
- **GET** `/` - Home page with event browsing
- **GET** `/search/` - Advanced search page
- **GET** `/ab-testing/` - A/B testing dashboard
- **GET** `/analytics/` - Google Analytics dashboard
- **GET** `/7232f7d/` - A/B test endpoint (SHA1 of "swift-canyon")
- **POST** `/fetch/` - Manual event fetching trigger

## Deployment to Render

### Prerequisites
- Render.com account
- GitHub repository connected to Render

### Deployment Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Deployment ready"
   git push origin main
   ```

2. **Configure Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Create a new Web Service
   - Connect your GitHub repository
   - Use the following settings:
     - **Build Command**: `./build.sh`
     - **Start Command**: `cd backend && gunicorn backend.wsgi:application`
     - **Environment**: Python 3.12

3. **Set Environment Variables** (in Render dashboard)
   ```
   PYTHON_VERSION=3.12.0
   DEBUG=False
   SECRET_KEY=<generate-secure-key>
   ALLOWED_HOSTS=<your-app>.onrender.com
   DATABASE_URL=<postgresql-url>  # If using PostgreSQL
   ```

4. **Deploy**
   - Render will automatically build and deploy
   - Access your app at: `https://<your-app>.onrender.com`

### Post-Deployment

1. **Run migrations** (if needed)
   ```bash
   # Via Render shell
   python backend/manage.py migrate
   ```

2. **Create superuser** (if needed)
   ```bash
   python backend/manage.py createsuperuser
   ```

3. **Verify deployment**
   - Check all pages load correctly
   - Test A/B endpoint: `https://<your-app>.onrender.com/7232f7d/`
   - Verify Google Analytics tracking (Tracking ID: G-WWESKXQCQY)

## 12-Factor App Compliance

✅ **Codebase**: Single codebase tracked in Git
✅ **Dependencies**: Explicitly declared in `requirements.txt`
✅ **Config**: Configuration via environment variables (.env, Render env vars)
✅ **Backing Services**: Database attachable via DATABASE_URL
✅ **Build, Release, Run**: Separated via `build.sh`, Render deployment
✅ **Processes**: Stateless processes (session data in DB)
✅ **Port Binding**: Self-contained with Gunicorn
✅ **Concurrency**: Horizontal scaling via Render
✅ **Disposability**: Fast startup and graceful shutdown
✅ **Dev/Prod Parity**: Same codebase, different configs
✅ **Logs**: Output to stdout (captured by Render)
✅ **Admin Processes**: Management commands via `manage.py`

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEBUG` | Enable debug mode | `False` | No |
| `SECRET_KEY` | Django secret key | - | Yes |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost` | Yes |
| `DATABASE_URL` | PostgreSQL connection URL | SQLite | No |

### Google Analytics
- Tracking ID: `G-WWESKXQCQY`
- Integrated on all pages

## Management Commands

### Fetch Events
```bash
python manage.py fetch_events
```
Fetches latest events from Yale SOM and YSPH websites.

## A/B Testing

### Endpoint: `/7232f7d/`
- **Button ID**: `abtest`
- **Variants**: 
  - Variant A: "kudos"
  - Variant B: "thanks"
- **Split**: 50/50 random assignment
- **Persistence**: Consistent per session
- **Tracking**: All visits recorded in database

## Code Quality

### Linting
- **Flake8**: Configured with `.flake8`
- **Max Line Length**: 100 characters
- **Excluded**: migrations, staticfiles, __pycache__

### Testing
- **Framework**: Django TestCase
- **Coverage**: 21 tests
- **Test Types**: Unit, integration, URL routing
- **Status**: ✅ All tests passing

## Contributing

1. Create a feature branch
2. Make changes
3. Run tests: `python manage.py test`
4. Run linting: `flake8 events/ backend/`
5. Commit and push
6. Create pull request

## License

MIT License

## Support

For issues or questions, contact the team members or create an issue on GitHub.

---

**Team Swift Canyon** | Yale University | 2025
