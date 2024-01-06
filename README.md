# WhatNeedsBe
### Trello-inspired task tracker.

### MVP
A simple list of tasks.
1) Right now, just a simple CRUD app for tasks
    - Create
    - Read
    - Update
    - Delete
2) Due dates
3) Linking tasks
   - Like sub-tasks but tasks can block multiple other tasks rather than just a single parent.
   - Able to create link types, links are more than just blocking.
5) Task groups within categories (possibly allow dragging)
4) Divide tasks into categories: life, game dev, etc.

### Nice to haves
- Users
- Timer for how long until a task fails
- Descriptions like Trello where it shows an icon if there is one, but doesn't bug you to add one
- Hard deadline - go full duolingo on the user
- Available after - a task can become available again after a set time has elapsed.
  - A month before my liscense expires, create a task for renewing it with a hard deadline.
- Reuse tasks - rather than a set schedule, one-off tasks can be reused, maybe from a template system.
  - Take cat to vet
- If this then that tasks: if this task is completed, schedule a follow-up task.
  - When dishes are clean, schedule a task for putting them away (find better example)
- A "not doing" button
  - does it mark the task as failed?
  - Option for what state to put the task in by clicking the "not doing" button when creating a series of tasks.
  - Could go the iPhone Bedtime route and ask every time if not doing counts as failure. (Annoy the user for not doing a task).
     Maybe just confirmation.
- Collated failure rate for a task series
  - User can select time range, total, 6 months, this month, this week

### Notes
- Missing due date marks task as failed.
  - Why? - Data can be collated to show a task completion rate improvement over time.
  - When? - Daily?
- Tasks can be assigned a completion state at any time.
- Most common states as buttons for easy select, dropdown for other states.
- Dropdown button on the task for editing instead of navigating to its own page. Description length might be a problem.

### Linked Tasks
- Dropdown for linked tasks
- Page for task shows subtasks focused, clicking a subtask takes you to the page for that task
