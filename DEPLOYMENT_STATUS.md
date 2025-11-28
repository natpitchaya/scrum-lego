# Deployment Notes

## Latest Deployment: November 28, 2025

### Changes Included:
- Google Analytics tracking (G-WWESKXQCQY) on all pages
- A/B Test button added to home page navigation
- A/B test endpoint at /7232f7d/ with session-based variant assignment
- 21 comprehensive tests (all passing)
- Flake8 linting configuration and fixes
- Complete README documentation with deployment instructions

### Pages:
- Home: /
- Search: /search/
- A/B Test Endpoint: /7232f7d/
- A/B Testing Dashboard: /ab-testing/
- Analytics Dashboard: /analytics/
- API: /api/events/

### Render Deployment:
If changes are not reflected on Render:
1. Check Render dashboard for deployment status
2. Manually trigger deployment from Render dashboard
3. Check build logs for any errors
4. Verify environment variables are set correctly

### Force Deployment:
To force Render to rebuild, make a trivial change and push:
```bash
# Add a comment to a file or update this file
git add .
git commit -m "Force Render deployment"
git push origin main
```
