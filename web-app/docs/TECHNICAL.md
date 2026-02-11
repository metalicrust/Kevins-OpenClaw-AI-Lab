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
| `/usage` | GET | API usage dashboard |
| `/usage/log` | POST | Log API usage |
| `/usage/thresholds` | POST | Update thresholds |

## Key Functions

### Data Operations

```python
load_daily_logs()      # Load all daily logs
save_daily_logs(logs)  # Save daily logs
load_projects()        # Load all projects
save_projects(projects) # Save projects
get_or_create_today_log() # Get/create today's log
```

### Usage Data Model

```json
{
  "tasks": {
    "REF-001": [
      {
        "timestamp": "2026-02-10T20:00:00",
        "tokens_in": 1000,
        "tokens_out": 500,
        "model": "moonshot/kimi-k2.5",
        "cost": 0.006
      }
    ]
  },
  "daily_totals": {
    "2026-02-10": {
      "tokens": 1500,
      "cost": 0.006
    }
  },
  "thresholds": {
    "daily": 5.0,
    "task": 1.0
  }
}
```

### Usage Functions

```python
load_usage()                    # Load usage data
save_usage(usage)              # Save usage data
estimate_cost(tokens_in, tokens_out, model)  # Calculate cost
log_task_usage(task_ref, tokens_in, tokens_out, model)  # Log usage
get_task_usage_summary(task_ref)  # Get summary for task
check_thresholds()             # Check if thresholds crossed
```

### Model Pricing

```python
MODEL_PRICING = {
    'moonshot/kimi-k2.5': {'input': 0.002, 'output': 0.008},
    'openai/gpt-4o': {'input': 0.005, 'output': 0.015},
    'openai/gpt-4o-mini': {'input': 0.00015, 'output': 0.0006},
    'default': {'input': 0.002, 'output': 0.008}
}
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

- [x] API usage tracking per task ✓ (Completed v1.2)
- [x] Cost estimation and budget alerts ✓ (Completed v1.2)
- [ ] Automatic usage logging (integrate with OpenClaw API)
- [ ] Export data to CSV/JSON
- [ ] Integration with external calendars
- [ ] Mobile app version
- [ ] Real-time notifications
- [ ] Task reference numbers (REF-XXX)
- [ ] Priority queue reordering
- [ ] Stop button for active tasks

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
