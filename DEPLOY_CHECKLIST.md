# Quick Deployment Checklist

## Before Deploying

1. **Commit and push to GitHub:**
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

Wait for the deployment to complete. The app will automatically:
- Allow all `.onrender.com` domains
- Set `DEBUG=False` for production
- Generate a secure `SECRET_KEY`

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
