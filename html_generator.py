#!/usr/bin/env python3
# Copyright 2025 Resume Builder Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import html
from pathlib import Path
from typing import Dict, List, Any


def escape_text(text: str | None) -> str:
    """Escape HTML special characters in text."""
    return html.escape(str(text)) if text else ''


def generate_experience_html(experiences: List[Dict[str, Any]]) -> str:
    """Generate HTML for experience section."""
    exp_html = ""
    for exp in experiences:
        bullets = "".join([f"<li>{escape_text(item)}</li>" for item in exp.get('bullets', [])])
        exp_html += f'''
        <section class="blocks">
            <div class="date"><span>{escape_text(exp['end_date'])}</span><span>{escape_text(exp['start_date'])}</span></div>
            <div class="decorator"></div>
            <div class="details">
                <header><h3>{escape_text(exp['title'])}</h3><span class="place">{escape_text(exp['company'])}</span><span class="location">{escape_text(exp.get('location', ''))}</span></header>
                <div><ul>{bullets}</ul></div>
            </div>
        </section>'''
    return exp_html


def generate_projects_html(projects: List[Dict[str, Any]]) -> str:
    """Generate HTML for projects section."""
    proj_html = ""
    for proj in projects:
        bullets = "".join([f"<li>{escape_text(item)}</li>" for item in proj.get('bullets', [])])
        proj_html += f'''
        <section class="blocks">
            <div class="date"><span>{escape_text(proj['end_date'])}</span><span>{escape_text(proj['start_date'])}</span></div>
            <div class="decorator"></div>
            <div class="details">
                <header><h3>{escape_text(proj['title'])}</h3><span class="place">{escape_text(proj.get('subtitle', ''))}</span></header>
                <div><ul>{bullets}</ul></div>
            </div>
        </section>'''
    return proj_html


def generate_education_html(education: List[Dict[str, Any]]) -> str:
    """Generate HTML for education section."""
    edu_html = ""
    for edu in education:
        edu_html += f'''
        <section class="blocks">
            <div class="date"><span>{escape_text(edu['end_date'])}</span><span>{escape_text(edu['start_date'])}</span></div>
            <div class="decorator"></div>
            <div class="details">
                <header><h3>{escape_text(edu['degree'])}</h3><span class="place">{escape_text(edu['school'])}</span><span class="location">{escape_text(edu.get('location', ''))}</span></header>
                <div>{escape_text(edu.get('notes', ''))}</div>
            </div>
        </section>'''
    return edu_html


def generate_skills_html(skills: List[Dict[str, Any]]) -> str:
    """Generate HTML for skills section."""
    skills_html = ""
    for skill in skills:
        skills_html += f'<ul><li><strong>{escape_text(skill["category"])}:</strong></li><li>{escape_text(skill["skills"])}</li></ul>'
    return skills_html


def generate_html(data: Dict[str, Any]) -> str:
    """
    Generate complete HTML resume from data dictionary.
    
    Args:
        data: Dictionary containing resume data with keys:
            - name, subtitle
            - contact: dict with website, email, phone
            - experience, projects, education: lists
            - skills: list of dicts
    
    Returns:
        Complete HTML document as string
    """
    # Load template with multiple fallback paths
    possible_paths = [
        Path(__file__).parent / 'templates' / 'resume_template.html',
        Path(__file__).parent / 'resume_template.html',
        Path('.') / 'templates' / 'resume_template.html',
        Path('.') / 'resume_template.html',
        Path(__file__).parent / '..' / 'templates' / 'resume_template.html',
    ]
    
    html_template = None
    for template_path in possible_paths:
        try:
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    html_template = f.read()
                    break
        except (FileNotFoundError, PermissionError):
            continue
    
    if html_template is None:
        # Fallback: return basic HTML if template not found
        return '<html><body><p>Resume template not found</p></body></html>'
    
    # Generate sections
    exp_html = generate_experience_html(data.get('experience', []))
    proj_html = generate_projects_html(data.get('projects', []))
    edu_html = generate_education_html(data.get('education', []))
    skills_html = generate_skills_html(data.get('skills', []))
    
    # Process website
    website = data.get('contact', {}).get('website', '')
    website_display = website.replace('https://', '').replace('http://', '')
    
    # Format template
    return html_template.format(
        name=escape_text(data.get('name', 'Your Name')),
        subtitle=escape_text(data.get('subtitle', '')),
        experience=exp_html,
        projects=proj_html,
        education=edu_html,
        skills=skills_html,
        website=escape_text(website),
        website_display=escape_text(website_display),
        email=escape_text(data.get('contact', {}).get('email', '')),
        phone=escape_text(data.get('contact', {}).get('phone', ''))
    )
