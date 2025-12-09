# Sprint 3 Review

**Sprint Goal:** Deliver a functional end-to-end event browsing experience.
**Status:** Partially Met

## Executive Summary
We successfully deployed a stable public version on Render where users can view aggregated events from various Yale sources. The core event-browsing journey works. However, we did not fully complete the planned filtering, tagging metadata, or user accounts due to higher-than-expected complexity in data ingestion.

## User Journey Demo
The following full journey is currently demonstrable:
1.  **Landing:** User lands on the homepage and sees a clean, scrollable feed of aggregated Yale events.
2.  **Browsing:** Events are chronologically ordered; users can scan titles, descriptions, and dates.
3.  **Details:** User clicks into an event to open the official page in a new tab.
4.  **Calendar:** User adds events to Google Calendar, Outlook, or downloads an .ics file.
5.  **Navigation:** Page loads consistently across devices via Render deployment.

## Completed Work
**Total Points Completed:** 33 (based on story sum) / Velocity Tracking indicates 20.

*   **Event Source API Integration (8 pts):** Backend ingestion/cleaning of Yale + New Haven feeds.
*   **Unified Event Feed (5 pts):** Consolidated list rendered on frontend.
*   **Keyword Search (5 pts):** Full-text search implementation.
*   **Add to Calendar (4 pts):** Google/Outlook/.ics support.
*   **Event Card Display (3 pts):** UI components for event details.
*   **Filter by Date (3 pts):** "Today" and "This Week" filters.
*   **Responsive Web UI (3 pts):** Mobile/Desktop optimization.
*   **"More Info" Link (2 pts):** External linking.

## Velocity Tracking
*   **Sprint 2 Velocity:** 13 points
*   **Sprint 3 Velocity:** 20 points
*   **Average Velocity:** 16.5 points

## Technical Progress
### What’s Working Well
*   Stable aggregation pipeline pulling events reliably.
*   Production deployment is stable with no major downtime.
*   Unified event schema simplifies future filtering.
*   Frontend rendering is clean and performant.

### Remaining Challenges
*   **Data Normalization:** Inconsistent fields from different sources.
*   **Scraping:** Occasional failures to retrieve accurate time data.
*   **Missing Features:** Auth, personalization, and non-Yale events.
*   **Performance:** Need caching/pagination for growth.
