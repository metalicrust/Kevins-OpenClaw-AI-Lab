# 🤖 Jarvis Agent Dashboard - User Guide

## Overview

The Agent Dashboard is a web-based tracking system for monitoring Jarvis's work as Kevin's AI assistant. It provides real-time visibility into what tasks are being worked on, what's queued up, and what's been completed.

**URL:** http://localhost:5051  
**Data Storage:** JSON files in `data/` directory

---

## Dashboard Sections

### 1. 📊 Stats Overview (Top Cards)

| Stat | Description |
|------|-------------|
| **Currently Working On** | Number of active tasks in progress |
| **Completed Today** | Tasks finished today |
| **Active Projects** | Long-term projects in progress |
| **Total Completed** | All-time completed tasks |

### 2. ⏭️ Priority Queue (What's Next)

Tasks queued up for future work. Kevin can add tasks here, and Jarvis will pull from this queue when ready for new work.

**How to add:**
1. Go to "📝 My Work Log"
2. Add task to "Up Next" column
3. Task appears in Priority Queue

### 3. 🎯 Currently Working On

Tasks Jarvis is actively working on right now.

**How tasks get here:**
- Kevin moves them from Priority Queue
- Or Kevin adds them directly via Daily Log

### 4. 📁 Active Projects

Long-term projects with multiple tasks. Shows:
- Project name
- Priority level (high/medium/low)
- Goal description
- Progress bar

### 5. ✅ Recently Completed

History of today's completed work with timestamps.

---

## Daily Log (Task Management)

**URL:** http://localhost:5051/daily-log

### Columns:

| Column | Purpose |
|--------|---------|
| **Currently Doing** | Tasks in progress |
| **Up Next** | Priority queue tasks |
| **Completed** | Finished tasks |

### Actions:

- **Add Task:** Type task, select column, click "Add Task"
- **Start Task:** Click ▶ to move from "Up Next" → "Currently Doing"
- **Complete Task:** Click ✓ to mark done
- **Delete Task:** Click × to remove

---

## Projects

**URL:** http://localhost:5051/projects

### Creating a Project:
1. Click "+ New Project"
2. Fill in:
   - **Name:** Project title
   - **Goal:** What we're trying to achieve
   - **Priority:** High / Medium / Low
   - **Deadline:** (optional)
3. Click "Create Project"

### Adding Tasks to Projects:
1. Open project detail page
2. Click "+ Add Task"
3. Task appears in project task list
4. Progress bar updates automatically

### Project Status:
- **Active:** In progress
- **Completed:** All tasks done

---

## Completed Archive

**URL:** http://localhost:5051/completed

### Features:
- Browse all completed tasks by date
- Search completed tasks
- View statistics:
  - Tasks completed this week
  - Tasks completed this month
  - Total all-time

---

## API Usage & Cost Tracking

**URL:** http://localhost:5051/usage

Track API token usage and costs per task. Helps monitor AI spending and stay within budget.

### Dashboard Overview:
- **Today's Tokens** - Total tokens used today
- **Today's Cost** - Estimated cost for today
- **Daily Threshold** - Warning limit for daily spending
- **Task Threshold** - Warning limit per task

### Task Usage Summary:
Shows each task with:
- Number of API calls
- Total tokens used
- Total cost (with color coding: green=under threshold, red=over)
- AI models used

### Daily History:
View usage for the last 30 days:
- Date
- Total tokens
- Total cost

### Logging Usage:
Manually log API usage for a task:
1. Enter **Task Reference** (e.g., REF-002)
2. Enter **Input Tokens** (tokens sent to API)
3. Enter **Output Tokens** (tokens received from API)
4. Select **AI Model** used
5. Click "Log Usage"

### Threshold Settings:
Configure warning limits:
- **Daily Limit** - Total daily budget (default: $5.00)
- **Per-Task Limit** - Max cost per task (default: $1.00)

Warnings appear at:
- 80% of threshold (orange)
- 100% of threshold (red)

### Model Pricing:
Current pricing (per 1,000 tokens):
| Model | Input | Output |
|-------|-------|--------|
| Kimi K2.5 | $0.002 | $0.008 |
| GPT-4o | $0.005 | $0.015 |
| GPT-4o-mini | $0.00015 | $0.0006 |

---

## Workflow Example

### Kevin assigns work:
1. Kevin opens Daily Log
2. Adds "Write blog post" to "Up Next"
3. Task appears in Priority Queue

### Jarvis starts work:
1. Jarvis sees task in Priority Queue
2. Moves it to "Currently Working On"
3. Begins working on task

### Task completed:
1. Jarvis finishes work
2. Marks task complete
3. Task moves to "Recently Completed" with timestamp

---

## Data Storage

All data is stored in JSON files:

- `data/daily_logs.json` - Daily task logs
- `data/projects.json` - Project data
- `data/usage.json` - API usage and cost data

**Backup:** Copy these files to backup your data.

---

## Tips

- **Use Priority Queue** for upcoming work
- **Mark tasks complete** to track progress
- **Check stats** daily to see productivity
- **Archive old projects** when done

---

## Support

For issues or feature requests, add a task to the Priority Queue with details.

---

*Last Updated: 2026-02-10*  
*Dashboard Version: 1.2*

## Changelog

### v1.2 (2026-02-10)
- Added API Usage & Cost Tracking
- Task reference numbers (REF-XXX)
- Automatic next-task workflow

### v1.1 (2026-02-10)
- Added Documentation & User Guide
- Technical documentation

### v1.0 (2026-02-10)
- Initial release
- Dashboard, Daily Log, Projects, Completed Archive
