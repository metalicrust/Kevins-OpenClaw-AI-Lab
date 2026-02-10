#!/usr/bin/env python3
"""
Agent Dashboard Web App - Feature 3: Active Projects Management
Full project management with tasks, status tracking, and progress
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

def load_json(filepath, default=None):
    """Load JSON file or return default"""
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
    """Save data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def get_or_create_today_log():
    """Get today's log or create empty one"""
    today = datetime.now().strftime("%Y-%m-%d")
    logs = load_json(DAILY_LOG_FILE, {})
    
    if today not in logs:
        logs[today] = {
            "date": today,
            "doing": [],
            "completed": [],
            "next": [],
            "notes": ""
        }
        save_json(DAILY_LOG_FILE, logs)
    
    return logs[today], today

# PROJECTS FUNCTIONS
def load_projects():
    """Load all projects"""
    return load_json(PROJECTS_FILE, [])

def save_projects(projects):
    """Save projects"""
    save_json(PROJECTS_FILE, projects)

def get_project_by_id(project_id):
    """Get single project by ID"""
    projects = load_projects()
    for i, project in enumerate(projects):
        if project.get('id') == project_id:
            return project, i
    return None, -1

@app.route('/')
def dashboard():
    """Main dashboard"""
    today_log, today = get_or_create_today_log()
    logs = load_json(DAILY_LOG_FILE, {})
    projects = load_projects()
    
    # Calculate stats
    total_completed = sum(len(log.get('completed', [])) for log in logs.values())
    active_projects = len([p for p in projects if p.get('status') != 'completed'])
    
    # Get recent projects (last 5)
    recent_projects = sorted(projects, key=lambda x: x.get('updated', ''), reverse=True)[:5]
    
    return render_template('dashboard.html',
                         today=today,
                         today_log=today_log,
                         total_completed=total_completed,
                         active_projects=active_projects,
                         recent_projects=recent_projects,
                         logs_count=len(logs))

# DAILY LOG ROUTES
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
        logs = load_json(DAILY_LOG_FILE, {})
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in logs:
            logs[today] = {"date": today, "doing": [], "completed": [], "next": [], "notes": ""}
        
        if section in logs[today]:
            logs[today][section].append(task)
            save_json(DAILY_LOG_FILE, logs)
            flash(f'Task added to {section}', 'success')
    else:
        flash('Task cannot be empty', 'error')
    
    return redirect(url_for('daily_log'))

@app.route('/daily-log/move', methods=['POST'])
def move_task():
    """Move task between sections"""
    task = request.form.get('task', '')
    from_section = request.form.get('from_section', '')
    to_section = request.form.get('to_section', '')
    
    logs = load_json(DAILY_LOG_FILE, {})
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today in logs and from_section in logs[today] and to_section in logs[today]:
        if task in logs[today][from_section]:
            logs[today][from_section].remove(task)
            logs[today][to_section].append(task)
            save_json(DAILY_LOG_FILE, logs)
            flash(f'Task moved to {to_section}', 'success')
    
    return redirect(url_for('daily_log'))

@app.route('/daily-log/delete', methods=['POST'])
def delete_task():
    """Delete a task"""
    task = request.form.get('task', '')
    section = request.form.get('section', '')
    
    logs = load_json(DAILY_LOG_FILE, {})
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today in logs and section in logs[today]:
        if task in logs[today][section]:
            logs[today][section].remove(task)
            save_json(DAILY_LOG_FILE, logs)
            flash('Task deleted', 'success')
    
    return redirect(url_for('daily_log'))

@app.route('/daily-log/history')
def log_history():
    """View past daily logs"""
    logs = load_json(DAILY_LOG_FILE, {})
    sorted_logs = dict(sorted(logs.items(), reverse=True))
    return render_template('history.html', logs=sorted_logs)

# PROJECT ROUTES
@app.route('/projects')
def projects_list():
    """List all projects"""
    projects = load_projects()
    
    # Sort by status (active first) then by updated date
    status_order = {'in_progress': 0, 'planning': 1, 'on_hold': 2, 'completed': 3}
    projects.sort(key=lambda x: (status_order.get(x.get('status', ''), 99), x.get('updated', '')), reverse=True)
    
    return render_template('projects.html', projects=projects)

@app.route('/projects/<int:project_id>')
def project_detail(project_id):
    """View project details"""
    project, idx = get_project_by_id(project_id)
    if project is None:
        flash('Project not found', 'error')
        return redirect(url_for('projects_list'))
    
    return render_template('project_detail.html', project=project)

@app.route('/projects/new', methods=['GET', 'POST'])
def project_new():
    """Create new project"""
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
    """Edit project"""
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
    """Add task to project"""
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
    """Toggle task completion"""
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

@app.route('/projects/<int:project_id>/task/<int:task_id>/delete', methods=['POST'])
def project_delete_task(project_id, task_id):
    """Delete project task"""
    project, idx = get_project_by_id(project_id)
    if project is None:
        flash('Project not found', 'error')
        return redirect(url_for('projects_list'))
    
    project['tasks'] = [t for t in project.get('tasks', []) if t.get('id') != task_id]
    project['updated'] = datetime.now().isoformat()
    
    projects = load_projects()
    projects[idx] = project
    save_projects(projects)
    flash('Task deleted', 'success')
    
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/projects/<int:project_id>/delete', methods=['POST'])
def project_delete(project_id):
    """Delete entire project"""
    projects = load_projects()
    projects = [p for p in projects if p.get('id') != project_id]
    save_projects(projects)
    flash('Project deleted', 'success')
    return redirect(url_for('projects_list'))

if __name__ == '__main__':
    print("🚀 Agent Dashboard - Feature 3: Active Projects")
    print("📱 Open http://localhost:5051")
    app.run(host='localhost', port=5051, debug=True)
