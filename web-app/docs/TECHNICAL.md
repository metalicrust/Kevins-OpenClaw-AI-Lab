# 🤖 Jarvis Agent Dashboard - Technical Documentation

## Architecture

```
web-app/
├── app.py              # Flask application (all routes)
├── data/               # JSON data storage
│   ├── daily_logs.json
│   └── projects.json
├── static/
│   └── css/
│       └── style.css   # Dark theme styles
├── templates/          # Jinja2 HTML templates
│   ├── dashboard.html
│   ├── daily-log.html
│   ├── projects.html
│   ├── project_new.html
│   ├── project_edit.html
│   ├── project_detail.html
│   ├── completed.html
│   ├── completed_search.html
│   └── history.html
└── docs/
    └── USER_GUIDE.md   # User documentation
```

## Technology Stack

- **Backend:** Flask (Python 3)
- **Frontend:** HTML5, CSS3, vanilla JavaScript
- **Data:** JSON files (no database required)
- **Template Engine:** Jinja2

## Data Models

### Daily Log Entry

```json
{
  "2026-02-10": {
    "date": "2026-02-10",
    "doing": ["Task 1", "Task 2"],
    "completed": ["Done task"],
    "next": ["Upcoming task"],
    "notes": "Optional notes"
  }
}
```

### Project

```json
{
  "id": "uuid-string",
  "name": "Project Name",
  "goal": "Project goal description",
  "priority": "high|medium|low",
  "status": "active|completed",
  "deadline": "2026-02-15",
  "created": "2026-02-10T20:00:00",
  "updated": "2026-02-10T20:00:00",
  "tasks": [
    {"text": "Task 1", "completed": false},
    {"text": "Task 2", "completed": true}
  ]
}
```

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Dashboard homepage |
| `/daily-log` | GET/POST | Daily task management |
| `/daily-log/move/<task>` | POST | Move task between columns |
| `/daily-log/complete/<task>` | POST | Mark task complete |
| `/daily-log/delete/<task>` | POST | Delete task |
| `/daily-log/history` | GET | View past logs |
| `/projects` | GET | List all projects |
| `/projects/new` | GET/POST | Create new project |
| `/projects/<id>` | GET | Project detail |
| `/projects/<id>/edit` | GET/POST | Edit project |
| `/projects/<id>/delete` | POST | Delete project |
| `/projects/<id>/tasks` | POST | Add task to project |
| `/projects/<id>/tasks/<idx>/toggle` | POST | Toggle task completion |
| `/completed` | GET | Completed tasks archive |
| `/completed/search` | GET/POST | Search completed tasks |

## Key Functions

### Data Operations

```python
load_daily_logs()      # Load all daily logs
save_daily_logs(logs)  # Save daily logs
load_projects()        # Load all projects
save_projects(projects) # Save projects
get_or_create_today_log() # Get/create today's log
```

### Template Helpers

```python
# Dashboard context
today_log      # Today's log entry
total_completed # All-time completed count
active_projects # Number of active projects
recent_projects # Last 5 updated projects
```

## Styling

### Color Scheme (Dark Theme)

- **Background:** `#0a0e27` (navy)
- **Card Background:** `#16213e`
- **Card Border:** `#0f3460`
- **Accent (Pink):** `#e94560`
- **Text Primary:** `#eee`
- **Text Secondary:** `#888`

### CSS Classes

```css
.sidebar          /* Navigation sidebar */
.main             /* Main content area */
.stats-grid       /* Stats cards grid */
.card             /* Content cards */
.priority-queue   /* Priority queue banner */
.three-columns    /* 3-column layout */
.task-list        /* Task list styling */
.completed-column /* Completed tasks column */
```

## Running the App

```bash
cd web-app
source venv/bin/activate
python app.py
# Open http://localhost:5051
```

## Future Enhancements

- [ ] API usage tracking per task
- [ ] Cost estimation and budget alerts
- [ ] Export data to CSV/JSON
- [ ] Integration with external calendars
- [ ] Mobile app version
- [ ] Real-time notifications

## Git Workflow

1. Create feature branch: `git checkout -b feature/name`
2. Make changes
3. Commit: `git commit -m "description"`
4. Push: `git push origin feature/name`
5. Create PR via GitHub CLI
6. Merge to main after review

---

*Created: 2026-02-10*  
*Maintainer: Jarvis (Kevin's AI Assistant)*
