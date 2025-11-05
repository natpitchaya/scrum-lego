# scrum-lego
Final Project for Scrum Lego Team!
6. GitHub Project Setup
You must set up a GitHub Project (V2) with:

Custom fields:

Story Points (Number field or Single Select: 1, 2, 3, 5, 8, 13, ?)
Status (Single Select: To Do, In Progress, In Review, Done)
Priority (Single Select: High, Medium, Low)
Sprint (Iteration Field with 1-2 week sprints)
Three required views:

Product Backlog (Table View)

Filter: label:"user story"
Sort by: Priority (High to Low), then Story Points
Visible columns: Title, Assignees, Story Points, Priority, Status
Sprint 2 Backlog (Table View)

Filter: label:"user story" iteration:"Sprint 2"
Visible columns: Title, Assignees, Story Points, Status, Sprint
Sprint 2 Task Board (Board View)

Filter: (label:"task" OR label:"spike") iteration:"Sprint 2"
Columns: To Do, In Progress, In Review, Done
Group by: Status
Labels configured:

user story (blue)
task (green)
bug (red)
epic (purple)
spike (yellow)
documentation (gray)
Issue templates created:

.github/ISSUE_TEMPLATE/user-story.md
.github/ISSUE_TEMPLATE/task.md
.github/ISSUE_TEMPLATE/bug.md
