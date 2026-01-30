#!/usr/bin/env python3
"""
Flask Web Interface for Resume Builder

A web-based interface for creating professional HTML resumes.
Provides REST API and web UI for resume generation.

Usage:
    python web_app.py [--host HOST] [--port PORT] [--debug]
"""

import html
import json
import re
import logging
import os
from datetime import datetime
from pathlib import Path
from flask import Flask, request, render_template_string, jsonify, send_file, Response
from html_generator import generate_html as generate_resume_html

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
DATE_FORMATS = ['%Y', '%m/%Y', '%b %Y', '%Y-%m-%d', '%B %Y', 'Present']

def validate_email(email):
    if not email:
        return True
    if not re.match(EMAIL_PATTERN, email):
        raise ValueError(f"Invalid email format: {email}")
    return True

def validate_date(date_string):
    if not date_string:
        return True
    for fmt in DATE_FORMATS:
        try:
            datetime.strptime(date_string, fmt)
            return True
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_string}")

def sanitize_input(text, max_length=10000):
    if not text:
        return ""
    text = str(text)[:max_length]
    return html.escape(text.strip())

def escape_text(text):
    return html.escape(str(text)) if text else ""

def show_error(message):
    return jsonify({"error": message}), 400

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Builder</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600|Source+Code+Pro:400" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: "Open Sans", sans-serif; background: #f5f5f5; color: #333; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: #2c3e50; color: white; padding: 20px 0; margin-bottom: 30px; }
        header h1 { text-align: center; font-weight: 300; }
        .main-content { display: flex; gap: 30px; }
        .form-section { flex: 1; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .preview-section { flex: 1; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { color: #2c3e50; margin-bottom: 20px; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h3 { color: #34495e; margin: 15px 0 10px; font-size: 1em; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: 500; color: #555; }
        input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }
        textarea { resize: vertical; min-height: 80px; }
        input:focus, textarea:focus { outline: none; border-color: #3498db; }
        .btn { padding: 12px 25px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; transition: background 0.3s; }
        .btn-primary { background: #3498db; color: white; }
        .btn-primary:hover { background: #2980b9; }
        .btn-success { background: #27ae60; color: white; }
        .btn-success:hover { background: #219a52; }
        .btn-danger { background: #e74c3c; color: white; }
        .btn-danger:hover { background: #c0392b; }
        .btn-group { display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }
        .item-list { margin: 15px 0; }
        .item-card { background: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; margin-bottom: 10px; border-radius: 4px; position: relative; }
        .item-card h4 { color: #2c3e50; margin-bottom: 5px; }
        .item-card p { color: #666; font-size: 0.9em; }
        .item-card .remove-btn { position: absolute; top: 10px; right: 10px; background: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; font-size: 12px; }
        .preview-frame { border: 1px solid #ddd; min-height: 800px; background: white; }
        .tab-buttons { display: flex; gap: 5px; margin-bottom: 15px; }
        .tab-btn { padding: 8px 15px; background: #ecf0f1; border: none; cursor: pointer; border-radius: 4px 4px 0 0; }
        .tab-btn.active { background: #3498db; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .flash { padding: 10px 15px; margin-bottom: 20px; border-radius: 4px; }
        .flash.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .flash.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        @media (max-width: 768px) { .main-content { flex-direction: column; } }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Resume Builder</h1>
        </div>
    </header>
    <div class="container">
        <div id="flash-container"></div>
        <div class="main-content">
            <div class="form-section">
                <form id="resume-form">
                    <h2>Your Information</h2>
                    <div class="form-group">
                        <label>Full Name *</label>
                        <input type="text" name="name" value="{{ data.name or '' }}" required>
                    </div>
                    <div class="form-group">
                        <label>Professional Subtitle</label>
                        <input type="text" name="subtitle" value="{{ data.subtitle or '' }}" placeholder="e.g., Senior Software Engineer">
                    </div>
                    
                    <h3>Contact Information</h3>
                    <div class="form-group">
                        <label>Website</label>
                        <input type="url" name="website" value="{{ data.contact.website or '' }}" placeholder="https://example.com">
                    </div>
                    <div class="form-group">
                        <label>Email *</label>
                        <input type="email" name="email" value="{{ data.contact.email or '' }}" required>
                    </div>
                    <div class="form-group">
                        <label>Phone</label>
                        <input type="tel" name="phone" value="{{ data.contact.phone or '' }}">
                    </div>
                    
                    <h2>Experience</h2>
                    <div id="experience-list" class="item-list">
                        {% for exp in data.experience %}
                        <div class="item-card">
                            <button type="button" class="remove-btn" onclick="removeItem('experience', {{ loop.index0 }})">Remove</button>
                            <h4>{{ exp.title }} at {{ exp.company }}</h4>
                            <p>{{ exp.start_date }} - {{ exp.end_date }}</p>
                        </div>
                        {% endfor %}
                    </div>
                    <button type="button" class="btn btn-primary" onclick="addExperience()">+ Add Experience</button>
                    
                    <h2>Projects</h2>
                    <div id="projects-list" class="item-list">
                        {% for proj in data.projects %}
                        <div class="item-card">
                            <button type="button" class="remove-btn" onclick="removeItem('projects', {{ loop.index0 }})">Remove</button>
                            <h4>{{ proj.title }}</h4>
                            <p>{{ proj.start_date }} - {{ proj.end_date }}</p>
                        </div>
                        {% endfor %}
                    </div>
                    <button type="button" class="btn btn-primary" onclick="addProject()">+ Add Project</button>
                    
                    <h2>Education</h2>
                    <div id="education-list" class="item-list">
                        {% for edu in data.education %}
                        <div class="item-card">
                            <button type="button" class="remove-btn" onclick="removeItem('education', {{ loop.index0 }})">Remove</button>
                            <h4>{{ edu.degree }}</h4>
                            <p>{{ edu.school }} ({{ edu.start_date }} - {{ edu.end_date }})</p>
                        </div>
                        {% endfor %}
                    </div>
                    <button type="button" class="btn btn-primary" onclick="addEducation()">+ Add Education</button>
                    
                    <h2>Skills</h2>
                    <div id="skills-list" class="item-list">
                        {% for skill in data.skills %}
                        <div class="item-card">
                            <button type="button" class="remove-btn" onclick="removeItem('skills', {{ loop.index0 }})">Remove</button>
                            <h4>{{ skill.category }}</h4>
                            <p>{{ skill.skills }}</p>
                        </div>
                        {% endfor %}
                    </div>
                    <button type="button" class="btn btn-primary" onclick="addSkill()">+ Add Skill Category</button>
                    
                    <div class="btn-group">
                        <button type="button" class="btn btn-success" onclick="previewResume()">Preview</button>
                        <button type="button" class="btn btn-success" onclick="exportHTML()">Export HTML</button>
                        <button type="button" class="btn btn-primary" onclick="saveJSON()">Save JSON</button>
                        <button type="button" class="btn btn-primary" onclick="document.getElementById('load-json').click()">Load JSON</button>
                        <input type="file" id="load-json" accept=".json" style="display:none" onchange="loadJSON(this)">
                    </div>
                </form>
            </div>
            
            <div class="preview-section">
                <h2>Preview</h2>
                <div class="tab-buttons">
                    <button class="tab-btn active" onclick="showTab('preview')">HTML Preview</button>
                    <button class="tab-btn" onclick="showTab('json')">JSON Data</button>
                </div>
                <div id="preview-tab" class="tab-content active">
                    <div id="preview-frame" class="preview-frame">
                        <iframe id="preview-iframe" style="width:100%; height:800px; border:none;"></iframe>
                    </div>
                </div>
                <div id="json-tab" class="tab-content">
                    <textarea id="json-preview" style="width:100%; min-height:800px; font-family:monospace;">{{ data_json }}</textarea>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let resumeData = {{ data|tojson }};
        
        function showFlash(message, type) {
            const container = document.getElementById('flash-container');
            container.innerHTML = `<div class="flash ${type}">${message}</div>`;
            setTimeout(() => container.innerHTML = '', 5000);
        }
        
        function showTab(tab) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tab + '-tab').classList.add('active');
        }
        
        function updateData() {
            const form = document.getElementById('resume-form');
            resumeData.name = form.name.value;
            resumeData.subtitle = form.subtitle.value;
            resumeData.contact.website = form.website.value;
            resumeData.contact.email = form.email.value;
            resumeData.contact.phone = form.phone.value;
        }
        
        async function previewResume() {
            updateData();
            try {
                const response = await fetch('/api/preview', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(resumeData)
                });
                const result = await response.json();
                if (result.html) {
                    document.getElementById('preview-iframe').srcdoc = result.html;
                    showTab('preview');
                } else {
                    showFlash(result.error || 'Error generating preview', 'error');
                }
            } catch (e) {
                showFlash('Error: ' + e.message, 'error');
            }
        }
        
        async function exportHTML() {
            updateData();
            try {
                const response = await fetch('/api/export', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(resumeData)
                });
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'resume.html';
                    a.click();
                    window.URL.revokeObjectURL(url);
                } else {
                    const result = await response.json();
                    showFlash(result.error || 'Error exporting', 'error');
                }
            } catch (e) {
                showFlash('Error: ' + e.message, 'error');
            }
        }
        
        async function saveJSON() {
            updateData();
            try {
                const response = await fetch('/api/save', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(resumeData)
                });
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'resume_data.json';
                    a.click();
                    window.URL.revokeObjectURL(url);
                } else {
                    const result = await response.json();
                    showFlash(result.error || 'Error saving', 'error');
                }
            } catch (e) {
                showFlash('Error: ' + e.message, 'error');
            }
        }
        
        function loadJSON(input) {
            const file = input.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    try {
                        resumeData = JSON.parse(e.target.result);
                        location.reload();
                    } catch (err) {
                        showFlash('Invalid JSON file', 'error');
                    }
                };
                reader.readAsText(file);
            }
        }
        
        function addExperience() {
            const title = prompt('Job Title:');
            if (!title) return;
            const company = prompt('Company:');
            const start = prompt('Start Date (e.g., 2024, Jan 2024):');
            const end = prompt('End Date (e.g., Present, 2024):');
            const location = prompt('Location (optional):');
            const bullets = prompt('Bullet points (one per line):');
            resumeData.experience.push({
                title, company, location, start_date: start, end_date: end,
                bullets: bullets ? bullets.split('\\n').filter(b => b.trim()) : []
            });
            location.reload();
        }
        
        function addProject() {
            const title = prompt('Project Title:');
            if (!title) return;
            const subtitle = prompt('Subtitle/Description (optional):');
            const start = prompt('Start Date:');
            const end = prompt('End Date:');
            const bullets = prompt('Bullet points (one per line):');
            resumeData.projects.push({
                title, subtitle, start_date: start, end_date: end,
                bullets: bullets ? bullets.split('\\n').filter(b => b.trim()) : []
            });
            location.reload();
        }
        
        function addEducation() {
            const degree = prompt('Degree:');
            if (!degree) return;
            const school = prompt('School/University:');
            const start = prompt('Start Date:');
            const end = prompt('End Date:');
            const notes = prompt('Notes (optional):');
            resumeData.education.push({degree, school, start_date: start, end_date: end, notes});
            location.reload();
        }
        
        function addSkill() {
            const category = prompt('Category (e.g., Programming Languages):');
            if (!category) return;
            const skills = prompt('Skills (comma-separated):');
            resumeData.skills.push({category, skills});
            location.reload();
        }
        
        function removeItem(type, index) {
            resumeData[type].splice(index, 1);
            location.reload();
        }
        
        document.getElementById('resume-form').addEventListener('submit', function(e) {
            e.preventDefault();
            previewResume();
        });
        
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('json-preview').value = JSON.stringify(resumeData, null, 2);
        });
    </script>
</body>
</html>
'''

def generate_html(data):
    return generate_resume_html(data)

def create_default_data():
    return {
        'name': '',
        'subtitle': '',
        'contact': {'website': '', 'email': '', 'phone': ''},
        'experience': [],
        'projects': [],
        'education': [],
        'skills': []
    }

@app.route('/')
def index():
    data = request.args.get('data')
    if data:
        try:
            resume_data = json.loads(data)
        except:
            resume_data = create_default_data()
    else:
        resume_data = create_default_data()
    return render_template_string(HTML_TEMPLATE, data=resume_data, data_json=json.dumps(resume_data, indent=2))

@app.route('/api/preview', methods=['POST'])
def api_preview():
    try:
        data = request.json
        if not data:
            return show_error('No data provided')
        if not data.get('name'):
            return show_error('Name is required')
        if not data.get('contact', {}).get('email'):
            return show_error('Email is required')
        try:
            validate_email(data['contact']['email'])
            for exp in data.get('experience', []):
                validate_date(exp.get('start_date', ''))
                validate_date(exp.get('end_date', ''))
            for proj in data.get('projects', []):
                validate_date(proj.get('start_date', ''))
                validate_date(proj.get('end_date', ''))
            for edu in data.get('education', []):
                validate_date(edu.get('start_date', ''))
                validate_date(edu.get('end_date', ''))
        except ValueError as e:
            return show_error(str(e))
        html = generate_html(data)
        return jsonify({'html': html})
    except Exception as e:
        logger.error(f"Preview error: {e}")
        return show_error(str(e))

@app.route('/api/export', methods=['POST'])
def api_export():
    try:
        data = request.json
        if not data:
            return show_error('No data provided')
        if not data.get('name'):
            return show_error('Name is required')
        validate_email(data['contact'].get('email', ''))
        html = generate_html(data)
        return Response(html, mimetype='text/html', headers={'Content-Disposition': 'attachment;filename=resume.html'})
    except Exception as e:
        logger.error(f"Export error: {e}")
        return show_error(str(e))

@app.route('/api/save', methods=['POST'])
def api_save():
    try:
        data = request.json
        if not data:
            return show_error('No data provided')
        return Response(
            json.dumps(data, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=resume_data.json'}
        )
    except Exception as e:
        logger.error(f"Save error: {e}")
        return show_error(str(e))

@app.route('/api/load', methods=['POST'])
def api_load():
    try:
        if 'file' not in request.files:
            return show_error('No file provided')
        file = request.files['file']
        data = json.load(file)
        required_keys = ['name', 'subtitle', 'contact', 'experience', 'projects', 'education', 'skills']
        for key in required_keys:
            if key not in data:
                return show_error(f'Invalid resume data: missing {key}')
        logger.info(f"Loaded resume data: {data.get('name', 'Unknown')}")
        return jsonify({'data': data})
    except json.JSONDecodeError as e:
        return show_error(f'Invalid JSON: {e}')
    except Exception as e:
        logger.error(f"Load error: {e}")
        return show_error(str(e))

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Resume Builder Web Interface')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    logger.info(f"Starting Resume Builder web interface on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()
