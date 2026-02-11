#!/usr/bin/env python3
"""
Agent Dashboard Web App - Jarvis Work Tracking
Tracks what I'm doing for Kevin: my tasks, projects I'm working on, completed work
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
PROJECTS_FILE = os.path.join(DATA_DIR, 'projects.json')
USAGE_FILE = os.path.join(DATA_DIR, 'usage.json')

# Model pricing (per 1K tokens)
MODEL_PRICING = {
    'moonshot/kimi-k2.5': {'input': 0.002, 'output': 0.008},
    'openai/gpt-4o': {'input': 0.005, 'output': 0.015},
    'openai/gpt-4o-mini': {'input': 0.00015, 'output': 0.0006},
    'default': {'input': 0.002, 'output': 0.008}
}

def load_json(filepath, default=None):
    if default is None:
        default = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_daily_logs():
    return load_json(DAILY_LOG_FILE, {})

def save_daily_logs(logs):
    save_json(DAILY_LOG_FILE, logs)

def load_projects():
    return load_json(PROJECTS_FILE, [])

def save_projects(projects):
    save_json(PROJECTS_FILE, projects)

def load_usage():
    return load_json(USAGE_FILE, {'tasks': {}, 'daily_totals': {}, 'thresholds': {'daily': 5.0, 'task': 1.0}})

def save_usage(usage):
    save_json(USAGE_FILE, usage)

def estimate_cost(tokens_in, tokens_out, model='default'):
    """Estimate cost based on token usage and model"""
    pricing = MODEL_PRICING.get(model, MODEL_PRICING['default'])
    cost_in = (tokens_in / 1000) * pricing['input']
    cost_out = (tokens_out / 1000) * pricing['output']
    return round(cost_in + cost_out, 4)

def log_task_usage(task_ref, tokens_in, tokens_out, model='default'):
    """Log API usage for a specific task"""
    usage = load_usage()
    cost = estimate_cost(tokens_in, tokens_out, model)
    today = datetime.now().strftime("%Y-%m-%d")
    
    if task_ref not in usage['tasks']:
        usage['tasks'][task_ref] = []
    
    usage['tasks'][task_ref].append({
        'timestamp': datetime.now().isoformat(),
        'tokens_in': tokens_in,
        'tokens_out': tokens_out,
        'model': model,
        'cost': cost
    })
    
    # Update daily totals
    if today not in usage['daily_totals']:
        usage['daily_totals'][today] = {'tokens': 0, 'cost': 0}
    
    usage['daily_totals'][today]['tokens'] += tokens_in + tokens_out
    usage['daily_totals'][today]['cost'] += cost
    
    save_usage(usage)
    return cost

def get_task_usage_summary(task_ref):
    """Get usage summary for a task"""
    usage = load_usage()
    task_data = usage['tasks'].get(task_ref, [])
    total_tokens = sum(u['tokens_in'] + u['tokens_out'] for u in task_data)
    total_cost = sum(u['cost'] for u in task_data)
    models_used = list(set(u['model'] for u in task_data))
    return {
        'total_tokens': total_tokens,
        'total_cost': round(total_cost, 4),
        'calls': len(task_data),
        'models': models_used
    }

def check_thresholds():
    """Check if usage crosses thresholds and return warnings"""
    usage = load_usage()
    today = datetime.now().strftime("%Y-%m-%d")
    thresholds = usage.get('thresholds', {'daily': 5.0, 'task': 1.0})
    warnings = []
    
    # Check daily threshold
    daily_cost = usage['daily_totals'].get(today, {}).get('cost', 0)
    if daily_cost >= thresholds['daily']:
        warnings.append(f"Daily cost threshold crossed: ${daily_cost:.4f} (limit: ${thresholds['daily']})")
    elif daily_cost >= thresholds['daily'] * 0.8:
        warnings.append(f"Daily cost at 80% threshold: ${daily_cost:.4f}")
    
    # Check task thresholds
    for task_ref, calls in usage['tasks'].items():
        task_cost = sum(c['cost'] for c in calls)
        if task_cost >= thresholds['task']:
            warnings.append(f"Task {task_ref} cost threshold crossed: ${task_cost:.4f}")
    
    return warnings

def get_or_create_today_log():
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

def get_project_by_id(project_id):
    projects = load_projects()
    for i, project in enumerate(projects):
        if project.get('id') == project_id:
            return project, i
    return None, -1

# DASHBOARD
@app.route('/')
def dashboard():
    today_log, today = get_or_create_today_log()
    logs = load_daily_logs()
    projects = load_projects()
    
    total_completed = sum(len(log.get('completed', [])) for log in logs.values())
    active_projects = len([p for p in projects if p.get('status') != 'completed'])
    recent_projects = sorted(projects, key=lambda x: x.get('updated', ''), reverse=True)[:5]
    
    return render_template('dashboard.html',
                         today=today,
                         today_log=today_log,
                         total_completed=total_completed,
                         active_projects=active_projects,
                         recent_projects=recent_projects,
                         logs_count=len(logs))

# DAILY LOG
@app.route('/daily-log')
def daily_log():
    today_log, today = get_or_create_today_log()
    return render_template('daily-log.html', log=today_log, today=today)

@app.route('/daily-log/add', methods=['POST'])
def add_task():
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
        flash('Task cannot be empty', 'error')
    
    return redirect(url_for('daily_log'))

@app.route('/daily-log/move', methods=['POST'])
def move_task():
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
    logs = load_daily_logs()
    sorted_logs = dict(sorted(logs.items(), reverse=True))
    return render_template('history.html', logs=sorted_logs)

# PROJECTS
@app.route('/projects')
def projects_list():
    projects = load_projects()
    status_order = {'in_progress': 0, 'planning': 1, 'on_hold': 2, 'completed': 3}
    projects.sort(key=lambda x: (status_order.get(x.get('status', ''), 99), x.get('updated', '')), reverse=True)
    return render_template('projects.html', projects=projects)

@app.route('/projects/<int:project_id>')
def project_detail(project_id):
    project, idx = get_project_by_id(project_id)
    if project is None:
        flash('Project not found', 'error')
        return redirect(url_for('projects_list'))
    return render_template('project_detail.html', project=project)

@app.route('/projects/new', methods=['GET', 'POST'])
def project_new():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        goal = request.form.get('goal', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'medium')
        
        if not name:
            flash('Project name is required', 'error')
            return redirect(url_for('project_new'))
        
        projects = load_projects()
        new_id = max([p.get('id', 0) for p in projects], default=0) + 1
        
        new_project = {
            'id': new_id,
            'name': name,
            'goal': goal,
            'description': description,
            'status': 'planning',
            'priority': priority,
            'tasks': [],
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat()
        }
        
        projects.append(new_project)
        save_projects(projects)
        flash(f'Project "{name}" created', 'success')
        return redirect(url_for('project_detail', project_id=new_id))
    
    return render_template('project_new.html')

@app.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
def project_edit(project_id):
    project, idx = get_project_by_id(project_id)
    if project is None:
        flash('Project not found', 'error')
        return redirect(url_for('projects_list'))
    
    if request.method == 'POST':
        project['name'] = request.form.get('name', project['name']).strip()
        project['goal'] = request.form.get('goal', project.get('goal', '')).strip()
        project['description'] = request.form.get('description', project.get('description', '')).strip()
        project['status'] = request.form.get('status', project.get('status', 'planning'))
        project['priority'] = request.form.get('priority', project.get('priority', 'medium'))
        project['updated'] = datetime.now().isoformat()
        
        projects = load_projects()
        projects[idx] = project
        save_projects(projects)
        flash('Project updated', 'success')
        return redirect(url_for('project_detail', project_id=project_id))
    
    return render_template('project_edit.html', project=project)

@app.route('/projects/<int:project_id>/task/add', methods=['POST'])
def project_add_task(project_id):
    project, idx = get_project_by_id(project_id)
    if project is None:
        flash('Project not found', 'error')
        return redirect(url_for('projects_list'))
    
    task_text = request.form.get('task', '').strip()
    if task_text:
        if 'tasks' not in project:
            project['tasks'] = []
        
        task_id = max([t.get('id', 0) for t in project['tasks']], default=0) + 1
        new_task = {
            'id': task_id,
            'text': task_text,
            'completed': False,
            'created': datetime.now().isoformat()
        }
        
        project['tasks'].append(new_task)
        project['updated'] = datetime.now().isoformat()
        
        projects = load_projects()
        projects[idx] = project
        save_projects(projects)
        flash('Task added', 'success')
    
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/projects/<int:project_id>/task/<int:task_id>/toggle', methods=['POST'])
def project_toggle_task(project_id, task_id):
    project, idx = get_project_by_id(project_id)
    if project is None:
        flash('Project not found', 'error')
        return redirect(url_for('projects_list'))
    
    for task in project.get('tasks', []):
        if task.get('id') == task_id:
            task['completed'] = not task.get('completed', False)
            project['updated'] = datetime.now().isoformat()
            break
    
    projects = load_projects()
    projects[idx] = project
    save_projects(projects)
    flash('Task updated', 'success')
    
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/projects/<int:project_id>/delete', methods=['POST'])
def project_delete(project_id):
    projects = load_projects()
    projects = [p for p in projects if p.get('id') != project_id]
    save_projects(projects)
    flash('Project deleted', 'success')
    return redirect(url_for('projects_list'))

# COMPLETED ARCHIVE
@app.route('/completed')
def completed_archive():
    logs = load_daily_logs()
    
    all_completed = []
    for date, log in logs.items():
        for task in log.get('completed', []):
            all_completed.append({
                'date': date,
                'task': task,
                'day_of_week': datetime.strptime(date, '%Y-%m-%d').strftime('%A')
            })
    
    all_completed.sort(key=lambda x: x['date'], reverse=True)
    
    total_tasks = len(all_completed)
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    this_week = [t for t in all_completed if datetime.strptime(t['date'], '%Y-%m-%d') >= week_start]
    month_start = today.replace(day=1)
    this_month = [t for t in all_completed if datetime.strptime(t['date'], '%Y-%m-%d') >= month_start]
    
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
                         this_week_tasks=this_week[:10],
                         today=today.strftime('%Y-%m-%d'))

@app.route('/completed/search')
def search_completed():
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

# API USAGE & COST TRACKING
@app.route('/usage')
def usage_dashboard():
    """Display API usage and cost dashboard"""
    usage = load_usage()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Get today's stats
    today_stats = usage['daily_totals'].get(today, {'tokens': 0, 'cost': 0})
    
    # Get all daily totals sorted by date
    daily_history = []
    for date, stats in sorted(usage['daily_totals'].items(), reverse=True)[:30]:
        daily_history.append({
            'date': date,
            'tokens': stats['tokens'],
            'cost': round(stats['cost'], 4)
        })
    
    # Get task summaries
    task_summaries = []
    for task_ref, calls in usage['tasks'].items():
        summary = get_task_usage_summary(task_ref)
        task_summaries.append({
            'ref': task_ref,
            **summary
        })
    task_summaries.sort(key=lambda x: x['total_cost'], reverse=True)
    
    # Check thresholds
    warnings = check_thresholds()
    thresholds = usage.get('thresholds', {'daily': 5.0, 'task': 1.0})
    
    return render_template('usage.html',
                         today_stats=today_stats,
                         daily_history=daily_history,
                         task_summaries=task_summaries,
                         warnings=warnings,
                         thresholds=thresholds,
                         model_pricing=MODEL_PRICING)

@app.route('/usage/log', methods=['POST'])
def log_usage():
    """Log API usage for a task"""
    task_ref = request.form.get('task_ref')
    tokens_in = int(request.form.get('tokens_in', 0))
    tokens_out = int(request.form.get('tokens_out', 0))
    model = request.form.get('model', 'default')
    
    cost = log_task_usage(task_ref, tokens_in, tokens_out, model)
    flash(f'Logged usage for {task_ref}: ${cost:.4f}', 'success')
    return redirect(url_for('usage_dashboard'))

@app.route('/usage/thresholds', methods=['POST'])
def update_thresholds():
    """Update usage thresholds"""
    usage = load_usage()
    usage['thresholds'] = {
        'daily': float(request.form.get('daily_threshold', 5.0)),
        'task': float(request.form.get('task_threshold', 1.0))
    }
    save_usage(usage)
    flash('Thresholds updated', 'success')
    return redirect(url_for('usage_dashboard'))

if __name__ == '__main__':
    print("🚀 Agent Dashboard - All Features")
    print("📱 Open http://localhost:5051")
    app.run(host='localhost', port=5051, debug=True)
