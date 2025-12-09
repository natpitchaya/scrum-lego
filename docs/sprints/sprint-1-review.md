# Sprint 1 Review

**Sprint Goal:** Establish the problem definition, user personas, product vision, wireframes, and technical blueprint for the Event Integration App.

**Status:** Completed

## Deliverables & Achievements

### 1. Executive Summary & Problem Definition
*   **Outcome:** Validated the need for a centralized event platform.
*   **Findings:**
    *   Current state involves fragmented calendars (Yale SOM, YSPH, Eventbrite, etc.).
    *   80% of survey respondents attend Yale events, but only 20% know where to find them in advance.
    *   Goal set: Reduce search time from >10 mins to <2 mins.

### 2. User Research
*   **Outcome:** Three core personas defined.
    1.  **Yale MBA Student:** Needs centralized feed for professional/academic events.
    2.  **New Haven Resident:** Wants to discover and promote public Yale events.
    3.  **Yale Faculty:** Requires simple interface to post departmental seminars.

### 3. Wireframes (Prototype)
*   **Outcome:** Figma mockups completed for three main screens.
    *   **Home Feed:** Filters for "Today", "This Week", "Public/Yale-only".
    *   **Event View:** Details (time, host) and "Add to Calendar" button.
    *   **Submit Form:** For community/faculty submissions.
*   **Feedback:** Mockups demonstrate clear navigation and mobile-responsive layout.

### 4. Technical Architecture
*   **Outcome:** Blueprint finalized.
    *   **Backend:** Django + DRF.
    *   **Data Processing:** `feedparser`, `icalendar`, `BeautifulSoup`, `rapidfuzz`.
    *   **Async Tasks:** Celery + Redis.
    *   **Database:** PostgreSQL (chosen for JSONB/Search support).
    *   **Hosting:** Render.

### 5. Process Setup
*   **Outcome:** Fully operational Scrum workflow.
    *   GitHub Project Board active with views for Backlog and Sprint.
    *   GitHub Flow established (PRs, Code Review).
    *   Automated testing configured via GitHub Actions.
    *   Documentation stored in `/docs/`.

## Metrics
*   **Story Points Completed:** N/A (Design Sprint).
*   **Artifacts Created:** Wireframes, Architecture Doc, Repo Setup, User Research Report.
