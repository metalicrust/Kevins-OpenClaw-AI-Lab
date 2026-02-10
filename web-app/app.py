#!/usr/bin/env python3
"""
Agent Dashboard Web App
Tracks agent work, daily logs, active projects, completed tasks
"""

import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

# Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# File paths
DAILY_LOG_FILE = os.path.join(DATA_DIR, 'daily-log.json')
PROJECTS_FILE = os.path.join(DATA_DIR, 'projects.json')
COMPLETED_FILE = os.path.join(DATA_DIR, 'completed.json')

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

@app.route('/')
def dashboard():
    """Main dashboard view"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Load data
    daily_logs = load_json(DAILY_LOG_FILE, {})
    projects = load_json(PROJECTS_FILE, [])
    completed = load_json(COMPLETED_FILE, [])
    
    # Get today's log or create empty
    today_log = daily_logs.get(today, {
        "date": today,
        "doing": [],
        "completed": [],
        "next": []
    })
    
    return render_template('dashboard.html', 
                         today=today,
                         today_log=today_log,
                         projects=projects,
                         completed_count=len(completed))

@app.route('/daily-log')
def daily_log():
    """Daily log view"""
    today = datetime.now().strftime("%Y-%m-%d")
    daily_logs = load_json(DAILY_LOG_FILE, {})
    today_log = daily_logs.get(today, {
        "date": today,
        "doing": [],
        "completed": [],
        "next": []
    })
    return render_template('daily-log.html', log=today_log)

@app.route('/api/log', methods=['POST'])
def update_log():
    """Update daily log via API"""
    data = request.json
    today = datetime.now().strftime("%Y-%m-%d")
    
    daily_logs = load_json(DAILY_LOG_FILE, {})
    if today not in daily_logs:
        daily_logs[today] = {
            "date": today,
            "doing": [],
            "completed": [],
            "next": []
        }
    
    # Update fields
    if 'doing' in data:
        daily_logs[today]['doing'] = data['doing']
    if 'completed' in data:
        daily_logs[today]['completed'] = data['completed']
    if 'next' in data:
        daily_logs[today]['next'] = data['next']
    
    save_json(DAILY_LOG_FILE, daily_logs)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("🚀 Agent Dashboard starting...")
    print("📱 Open http://localhost:5051")
    app.run(host='localhost', port=5051, debug=True)
