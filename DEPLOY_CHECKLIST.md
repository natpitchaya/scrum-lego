# Quick Deployment Checklist

## Before Deploying

1. **Update ALLOWED_HOSTS in render.yaml** (line 13):
   ```yaml
   value: YOUR-SERVICE-NAME.onrender.com,localhost,127.0.0.1
   ```
   Replace `YOUR-SERVICE-NAME` with your actual Render service name.

2. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin trial1
   ```

## On Render

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo: `natpitchaya/scrum-lego`
4. Select branch: `trial1`
5. Render will auto-detect `render.yaml` settings
6. Click **"Create Web Service"**

## After Initial Deploy

1. Note your service URL (e.g., `https://yale-events-aggregator.onrender.com`)
2. Go to **Environment** tab in Render
3. Update `ALLOWED_HOSTS` with your actual URL:
   ```
   yale-events-aggregator.onrender.com,localhost,127.0.0.1
   ```
4. Save and wait for automatic redeployment

## Verify Deployment

Visit these URLs (replace with your service name):
- Homepage: `https://your-service.onrender.com/`
- API: `https://your-service.onrender.com/api/events/`

## Optional: Create Admin User

In Render Dashboard → Shell, run:
```bash
cd backend
python manage.py createsuperuser
```

Then access admin at: `https://your-service.onrender.com/admin/`

## Done! 🎉

Your Yale Events Aggregator is now live with:
- ✅ Event search and filtering
- ✅ Date range filtering
- ✅ Organization filtering
- ✅ Calendar export (Google, Outlook, ICS)
- ✅ Pagination (25 events/page)
- ✅ Auto-updated events from Yale sources
