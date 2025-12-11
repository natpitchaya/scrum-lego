# Sprint 4 Planning

**Sprint Goal:** Finish the MVP and prepare for final submission by having a stable production deployment, implementing the A/B test endpoint with analytics, polishing the event browsing experience, and cleaning up code/docs.

## Sprint Details
*   **Sprint:** 4
*   **Start Date:** [Date]
*   **End Date:** [Date]
*   **Team Capacity:** ~25 Story Points (Estimated based on increasing velocity)

## Backlog Items Committed
The team has committed to the following user stories (~24 points total):

### Infrastructure & Deployment
*   **Production Deployment Hardening (8 pts):** Finalize production DB config on Render, ensure key routes load without errors, and set up basic monitoring.

### Features & Experiments
*   **A/B Test Endpoint (5 pts):** Implement `/7232f7d/` based on team nickname hash. Add randomized "kudos/thanks" button with session persistence.
*   **Analytics + A/B Tracking (5 pts):** Wire analytics for the A/B endpoint and core pages. Log variant exposures and button clicks.

### UI/UX Polish
*   **Search & Filter Polish (3 pts):** Clean up filters (organization + date range), improve "clear filters" behavior, and refine search result ordering.

### Documentation & Quality
*   **Docs & Code Quality (3 pts):** Update README with local setup/deployment instructions. Document staging vs production URLs. Run linting and fix main style issues.

## Dependencies & Risks
*   **Risk:** Test coverage is currently low.
*   **Risk:** A/B analytics might not capture enough traffic naturally.
*   **Dependency:** Render deployment pipeline stability.
