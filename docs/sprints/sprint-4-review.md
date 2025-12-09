# Sprint 4 Review

**Sprint Goal:** Finish the MVP and prepare for final submission (Stable Prod, A/B Test, Polish).
**Status:** Met

## Completed User Stories
We completed ~24 story points.

1.  **Production Deployment Hardening (8 pts):**
    *   *Demo:* Production URL is live at `https://yale-events-aggregator.onrender.com/`.
    *   *Notes:* Staging environment also active. Environment variables secured in Render.
2.  **A/B Test Endpoint (5 pts):**
    *   *Demo:* Endpoint `/7232f7d/` is public.
    *   *Notes:* Lists team nicknames. Button toggles "kudos"/"thanks" (50/50 split) with session persistence.
3.  **Analytics + A/B Tracking (5 pts):**
    *   *Demo:* Internal analytics view shows page views and button clicks per variant.
4.  **Search & Filter Polish (3 pts):**
    *   *Demo:* Users can filter by org/date and clear filters easily.
5.  **Docs & Code Quality (3 pts):**
    *   *Demo:* README updated with deployment instructions. Linting improved.

## Incomplete User Stories
*   **Advanced Admin Tools:** De-prioritized to focus on stability.
*   **Deep Test Coverage:** Partially addressed, but remains a focus for the final submission window.

## Metrics
*   **Planned Points:** ~24
*   **Completed Points:** 24
*   **Velocity Trend:**
    *   Sprint 2: 13
    *   Sprint 3: 20
    *   Sprint 4: 24
    *   *Average:* ~19
*   **Completion Rate:** 100% of committed core stories.

## Stakeholder Feedback
*   The MVP user journey is strong (Discover -> Filter -> Click-through -> Calendar).
*   Navigation across Home/Search/Analytics is consistent.
*   Edge cases like "no events found" need better messaging.
