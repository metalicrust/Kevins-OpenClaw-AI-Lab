#!/usr/bin/env python3
"""
Agent Dashboard Web App - Feature 4: Completed Tasks Archive
Tracks agent work with archive, statistics, and search
"""

import json
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'agent-dashboard-secret-key'

# Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

DAILY_LOG_FILE = os.path.join(DATA_DIR, 'daily_logs.json')

def load_daily_logs():
    """Load all daily logs"""
    if os.path.exists(DAILY_LOG_FILE):
        try:
            with open(DAILY_LOG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_daily_logs(logs):
    """Save daily logs"""
    with open(DAILY_LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def get_or_create_today_log():
    """Get today's log or create empty one"""
    today = datetime.now().strftime("%Y-%m-%d")
    logs = load_daily_logs()
    
    if today not in logs:
        logs[today] = {
            "date": today,
            "doing": [],
            "completed": [],
            "next": [],
            "notes": ""
        }
        save_daily_logs(logs)
    
    return logs[today], today

@app.route('/')
def dashboard():
    """Main dashboard"""
    today_log, today = get_or_create_today_log()
    logs = load_daily_logs()
    
    # Calculate stats
    total_completed = sum(len(log.get('completed', [])) for log in logs.values())
    
    return render_template('dashboard.html',
                         today=today,
                         today_log=today_log,
                         total_completed=total_completed,
                         logs_count=len(logs))

@app.route('/daily-log')
def daily_log():
    """Daily log view"""
    today_log, today = get_or_create_today_log()
    return render_template('daily-log.html', log=today_log, today=today)

@app.route('/daily-log/add', methods=['POST'])
def add_task():
    """Add a new task"""
    section = request.form.get('section', 'doing')
    task = request.form.get('task', '').strip()
    
    if task:
        logs = load_daily_logs()
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in logs:
            logs[today] = {"date": today, "doing": [], "completed": [], "next": [], "notes": ""}
        
        if section in logs[today]:
            logs[today][section].append(task)
            save_daily_logs(logs)
            flash(f'Task added to {section}', 'success')
        else:
            flash('Invalid section', 'error')
    else:
        flash('Task cannot be empty', 'error')
    
    return redirect(url_for('daily_log'))

@app.route('/daily-log/move', methods=['POST'])
def move_task():
    """Move task between sections"""
    task = request.form.get('task', '')
    from_section = request.form.get('from_section', '')
    to_section = request.form.get('to_section', '')
    
    logs = load_daily_logs()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today in logs and from_section in logs[today] and to_section in logs[today]:
        if task in logs[today][from_section]:
            logs[today][from_section].remove(task)
            logs[today][to_section].append(task)
            save_daily_logs(logs)
            flash(f'Task moved to {to_section}', 'success')
    
    return redirect(url_for('daily_log'))

@app.route('/daily-log/delete', methods=['POST'])
def delete_task():
    """Delete a task"""
    task = request.form.get('task', '')
    section = request.form.get('section', '')
    
    logs = load_daily_logs()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today in logs and section in logs[today]:
        if task in logs[today][section]:
            logs[today][section].remove(task)
            save_daily_logs(logs)
            flash('Task deleted', 'success')
    
    return redirect(url_for('daily_log'))

@app.route('/daily-log/history')
def log_history():
    """View past daily logs"""
    logs = load_daily_logs()
    # Sort by date descending
    sorted_logs = dict(sorted(logs.items(), reverse=True))
    return render_template('history.html', logs=sorted_logs)

@app.route('/completed')
def completed_archive():
    """View all completed tasks archive"""
    logs = load_daily_logs()
    
    # Gather all completed tasks with dates
    all_completed = []
    for date, log in logs.items():
        for task in log.get('completed', []):
            all_completed.append({
                'date': date,
                'task': task,
                'day_of_week': datetime.strptime(date, '%Y-%m-%d').strftime('%A')
            })
    
    # Sort by date descending
    all_completed.sort(key=lambda x: x['date'], reverse=True)
    
    # Calculate statistics
    total_tasks = len(all_completed)
    
    # This week
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    this_week = [t for t in all_completed if datetime.strptime(t['date'], '%Y-%m-%d') >= week_start]
    
    # This month
    month_start = today.replace(day=1)
    this_month = [t for t in all_completed if datetime.strptime(t['date'], '%Y-%m-%d') >= month_start]
    
    # Group by date for display
    grouped = {}
    for task in all_completed:
        date = task['date']
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(task)
    
    return render_template('completed.html',
                         completed_tasks=all_completed,
                         grouped_tasks=grouped,
                         total=total_tasks,
                         this_week_count=len(this_week),
                         this_month_count=len(this_month),
                         this_week_tasks=this_week[:10],  # Last 10 for preview
                         today=today.strftime('%Y-%m-%d'))

@app.route('/completed/search')
def search_completed():
    """Search completed tasks"""
    query = request.args.get('q', '').lower()
    logs = load_daily_logs()
    
    results = []
    for date, log in logs.items():
        for task in log.get('completed', []):
            if query in task.lower():
                results.append({
                    'date': date,
                    'task': task,
                    'day_of_week': datetime.strptime(date, '%Y-%m-%d').strftime('%A')
                })
    
    results.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('completed_search.html',
                         results=results,
                         query=query,
                         count=len(results))

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    logs = load_daily_logs()
    
    # Daily completion counts for last 30 days
    today = datetime.now()
    daily_stats = []
    
    for i in range(30):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        count = len(logs.get(date, {}).get('completed', []))
        daily_stats.append({'date': date, 'count': count})
    
    return {'daily_stats': daily_stats}

if __name__ == '__main__':
    print("🚀 Agent Dashboard - Feature 4: Completed Tasks Archive")
    print("📱 Open http://localhost:5051")
    app.run(host='localhost', port=5051, debug=True)
