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

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk
import os
import json
import sys
import html
import re
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
DATE_FORMATS = ["%Y", "%m/%Y", "%b %Y", "%Y-%m-%d", "%B %Y", "Present"]

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
    raise ValueError(f"Invalid date format: {date_string}. Use formats like 2024, Present, Jan 2024")

def sanitize_input(text, max_length=10000):
    if not text:
        return ""
    text = str(text)[:max_length]
    return html.escape(text.strip())

def escape_text(text):
    return html.escape(str(text)) if text else ""

def show_error(parent, message):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        flags=0,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        text=message
    )
    dialog.run()
    dialog.destroy()

def show_info(parent, message):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=message
    )
    dialog.run()
    dialog.destroy()

class ResumeBuilder(Gtk.Window):
    def __init__(self):
        super().__init__(title="Resume Builder")
        self.set_default_size(900, 700)
        self.set_border_width(10)
        self.set_property("name", "Resume Builder")
        self.set_property("accessible-name", "Resume Builder Application")
        
        logger.info("Initializing Resume Builder application")
        
        self.resume_data = {
            "name": "",
            "subtitle": "",
            "contact": {
                "website": "",
                "email": "",
                "phone": ""
            },
            "experience": [],
            "projects": [],
            "education": [],
            "skills": []
        }
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(main_box)
        
        left_scroll = Gtk.ScrolledWindow()
        left_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        left_scroll.set_size_request(450, -1)
        
        self.form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        left_scroll.add(self.form_box)
        main_box.pack_start(left_scroll, False, False, 0)
        
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.pack_start(right_box, True, True, 0)
        
        self.build_header_section()
        self.build_contact_section()
        self.build_experience_section()
        self.build_projects_section()
        self.build_education_section()
        self.build_skills_section()
        
        preview_label = Gtk.Label()
        preview_label.set_markup("<b>Preview</b>")
        preview_label.set_halign(Gtk.Align.START)
        right_box.pack_start(preview_label, False, False, 0)
        
        preview_scroll = Gtk.ScrolledWindow()
        preview_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        self.preview_view = Gtk.TextView()
        self.preview_view.set_editable(False)
        self.preview_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.preview_buffer = self.preview_view.get_buffer()
        preview_scroll.add(self.preview_view)
        right_box.pack_start(preview_scroll, True, True, 0)
        
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        right_box.pack_start(button_box, False, False, 0)
        
        self.preview_btn = Gtk.Button(label="Update Preview")
        self.preview_btn.set_tooltip_text("Update the resume preview (Ctrl+P)")
        self.preview_btn.connect("clicked", self.on_preview_clicked)
        button_box.pack_start(self.preview_btn, True, True, 0)
        
        self.export_btn = Gtk.Button(label="Export HTML")
        self.export_btn.set_tooltip_text("Export resume as HTML file (Ctrl+E)")
        self.export_btn.connect("clicked", self.on_export_clicked)
        button_box.pack_start(self.export_btn, True, True, 0)
        
        self.save_btn = Gtk.Button(label="Save JSON")
        self.save_btn.set_tooltip_text("Save resume data as JSON (Ctrl+S)")
        self.save_btn.connect("clicked", self.on_save_json)
        button_box.pack_start(self.save_btn, True, True, 0)
        
        self.load_btn = Gtk.Button(label="Load JSON")
        self.load_btn.set_tooltip_text("Load resume data from JSON (Ctrl+O)")
        self.load_btn.connect("clicked", self.on_load_json)
        button_box.pack_start(self.load_btn, True, True, 0)
        
        self.setup_keyboard_shortcuts()
        
    def setup_keyboard_shortcuts(self):
        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)
        
        self.save_btn.add_accelerator("clicked", accel_group, Gdk.KEY_s, Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)
        self.load_btn.add_accelerator("clicked", accel_group, Gdk.KEY_o, Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)
        self.export_btn.add_accelerator("clicked", accel_group, Gdk.KEY_e, Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)
        self.preview_btn.add_accelerator("clicked", accel_group, Gdk.KEY_p, Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)
    
    def create_section_header(self, title):
        label = Gtk.Label()
        label.set_markup(f"<b>{title}</b>")
        label.set_halign(Gtk.Align.START)
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.form_box.pack_start(label, False, False, 5)
        self.form_box.pack_start(separator, False, False, 0)
    
    def create_entry_row(self, label_text, placeholder=""):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        label = Gtk.Label(label=label_text, xalign=0)
        label.set_size_request(100, -1)
        entry = Gtk.Entry()
        entry.set_placeholder_text(placeholder)
        entry.set_property("accessible-name", label_text.strip(":"))
        box.pack_start(label, False, False, 0)
        box.pack_start(entry, True, True, 0)
        self.form_box.pack_start(box, False, False, 0)
        return entry
    
    def build_header_section(self):
        self.create_section_header("Header")
        self.name_entry = self.create_entry_row("Name:", "John Doe")
        self.name_entry.set_tooltip_text("Enter your full name")
        self.subtitle_entry = self.create_entry_row("Subtitle:", "Your professional tagline")
        self.subtitle_entry.set_tooltip_text("Enter your professional title or tagline")
    
    def build_contact_section(self):
        self.create_section_header("Contact")
        self.website_entry = self.create_entry_row("Website:", "https://example.com")
        self.website_entry.set_tooltip_text("Enter your personal website URL")
        self.email_entry = self.create_entry_row("Email:", "you@example.com")
        self.email_entry.set_tooltip_text("Enter your email address")
        self.phone_entry = self.create_entry_row("Phone:", "555-555-5555")
        self.phone_entry.set_tooltip_text("Enter your phone number")
    
    def build_experience_section(self):
        self.create_section_header("Experience")
        
        exp_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        add_exp_btn = Gtk.Button(label="Add Experience")
        add_exp_btn.set_tooltip_text("Add a new work experience entry")
        add_exp_btn.connect("clicked", self.on_add_experience)
        exp_btn_box.pack_start(add_exp_btn, True, True, 0)
        self.form_box.pack_start(exp_btn_box, False, False, 0)
        
        self.experience_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.form_box.pack_start(self.experience_box, False, False, 0)
    
    def build_projects_section(self):
        self.create_section_header("Projects")
        
        proj_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        add_proj_btn = Gtk.Button(label="Add Project")
        add_proj_btn.set_tooltip_text("Add a new project entry")
        add_proj_btn.connect("clicked", self.on_add_project)
        proj_btn_box.pack_start(add_proj_btn, True, True, 0)
        self.form_box.pack_start(proj_btn_box, False, False, 0)
        
        self.projects_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.form_box.pack_start(self.projects_box, False, False, 0)
    
    def build_education_section(self):
        self.create_section_header("Education")
        
        edu_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        add_edu_btn = Gtk.Button(label="Add Education")
        add_edu_btn.set_tooltip_text("Add a new education entry")
        add_edu_btn.connect("clicked", self.on_add_education)
        edu_btn_box.pack_start(add_edu_btn, True, True, 0)
        self.form_box.pack_start(edu_btn_box, False, False, 0)
        
        self.education_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.form_box.pack_start(self.education_box, False, False, 0)
    
    def build_skills_section(self):
        self.create_section_header("Skills")
        
        skill_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        add_skill_btn = Gtk.Button(label="Add Skill Category")
        add_skill_btn.set_tooltip_text("Add a new skill category")
        add_skill_btn.connect("clicked", self.on_add_skill)
        skill_btn_box.pack_start(add_skill_btn, True, True, 0)
        self.form_box.pack_start(skill_btn_box, False, False, 0)
        
        self.skills_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.form_box.pack_start(self.skills_box, False, False, 0)
    
    def on_add_experience(self, button):
        dialog = ExperienceDialog(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            try:
                exp_data = dialog.get_data()
                validate_date(exp_data["start_date"])
                validate_date(exp_data["end_date"])
                self.resume_data["experience"].append(exp_data)
                self.add_experience_item(exp_data)
                logger.info(f"Added experience: {exp_data["title"]} at {exp_data["company"]}")
            except ValueError as e:
                show_error(self, str(e))
        
        dialog.destroy()
    
    def add_experience_item(self, exp_data):
        frame = Gtk.Frame()
        frame.set_property("name", f"Experience: {exp_data["title"]}")
        frame_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        frame_box.set_margin_top(5)
        frame_box.set_margin_bottom(5)
        frame_box.set_margin_start(5)
        frame_box.set_margin_end(5)
        
        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{escape_text(exp_data["title"])}</b> at {escape_text(exp_data["company"])}")
        title_label.set_halign(Gtk.Align.START)
        frame_box.pack_start(title_label, False, False, 0)
        
        date_label = Gtk.Label(label=f"{escape_text(exp_data["start_date"])} - {escape_text(exp_data["end_date"])}")
        date_label.set_halign(Gtk.Align.START)
        frame_box.pack_start(date_label, False, False, 0)
        
        remove_btn = Gtk.Button(label="Remove")
        remove_btn.set_tooltip_text("Remove this experience entry")
        remove_btn.connect("clicked", lambda b: self.remove_item(frame, self.resume_data["experience"], exp_data))
        frame_box.pack_start(remove_btn, False, False, 0)
        
        frame.add(frame_box)
        self.experience_box.pack_start(frame, False, False, 0)
        self.experience_box.show_all()
    
    def on_add_project(self, button):
        dialog = ProjectDialog(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            try:
                proj_data = dialog.get_data()
                validate_date(proj_data["start_date"])
                validate_date(proj_data["end_date"])
                self.resume_data["projects"].append(proj_data)
                self.add_project_item(proj_data)
                logger.info(f"Added project: {proj_data["title"]}")
            except ValueError as e:
                show_error(self, str(e))
        
        dialog.destroy()
    
    def add_project_item(self, proj_data):
        frame = Gtk.Frame()
        frame.set_property("name", f"Project: {proj_data["title"]}")
        frame_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        frame_box.set_margin_top(5)
        frame_box.set_margin_bottom(5)
        frame_box.set_margin_start(5)
        frame_box.set_margin_end(5)
        
        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{escape_text(proj_data["title"])}</b>")
        title_label.set_halign(Gtk.Align.START)
        frame_box.pack_start(title_label, False, False, 0)
        
        date_label = Gtk.Label(label=f"{escape_text(proj_data["start_date"])} - {escape_text(proj_data["end_date"])}")
        date_label.set_halign(Gtk.Align.START)
        frame_box.pack_start(date_label, False, False, 0)
        
        remove_btn = Gtk.Button(label="Remove")
        remove_btn.set_tooltip_text("Remove this project entry")
        remove_btn.connect("clicked", lambda b: self.remove_item(frame, self.resume_data["projects"], proj_data))
        frame_box.pack_start(remove_btn, False, False, 0)
        
        frame.add(frame_box)
        self.projects_box.pack_start(frame, False, False, 0)
        self.projects_box.show_all()
    
    def on_add_education(self, button):
        dialog = EducationDialog(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            try:
                edu_data = dialog.get_data()
                validate_date(edu_data["start_date"])
                validate_date(edu_data["end_date"])
                self.resume_data["education"].append(edu_data)
                self.add_education_item(edu_data)
                logger.info(f"Added education: {edu_data["degree"]} at {edu_data["school"]}")
            except ValueError as e:
                show_error(self, str(e))
        
        dialog.destroy()
    
    def add_education_item(self, edu_data):
        frame = Gtk.Frame()
        frame.set_property("name", f"Education: {edu_data["degree"]}")
        frame_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        frame_box.set_margin_top(5)
        frame_box.set_margin_bottom(5)
        frame_box.set_margin_start(5)
        frame_box.set_margin_end(5)
        
        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{escape_text(edu_data["degree"])}</b>")
        title_label.set_halign(Gtk.Align.START)
        frame_box.pack_start(title_label, False, False, 0)
        
        school_label = Gtk.Label(label=f"{escape_text(edu_data["school"])}")
        school_label.set_halign(Gtk.Align.START)
        frame_box.pack_start(school_label, False, False, 0)
        
        remove_btn = Gtk.Button(label="Remove")
        remove_btn.set_tooltip_text("Remove this education entry")
        remove_btn.connect("clicked", lambda b: self.remove_item(frame, self.resume_data["education"], edu_data))
        frame_box.pack_start(remove_btn, False, False, 0)
        
        frame.add(frame_box)
        self.education_box.pack_start(frame, False, False, 0)
        self.education_box.show_all()
    
    def on_add_skill(self, button):
        dialog = SkillDialog(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            skill_data = dialog.get_data()
            self.resume_data["skills"].append(skill_data)
            self.add_skill_item(skill_data)
            logger.info(f"Added skill category: {skill_data["category"]}")
        
        dialog.destroy()
    
    def add_skill_item(self, skill_data):
        frame = Gtk.Frame()
        frame.set_property("name", f"Skills: {skill_data["category"]}")
        frame_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        frame_box.set_margin_top(5)
        frame_box.set_margin_bottom(5)
        frame_box.set_margin_start(5)
        frame_box.set_margin_end(5)
        
        cat_label = Gtk.Label()
        cat_label.set_markup(f"<b>{escape_text(skill_data["category"])}</b>")
        cat_label.set_halign(Gtk.Align.START)
        frame_box.pack_start(cat_label, False, False, 0)
        
        skills_label = Gtk.Label(label=escape_text(skill_data["skills"]))
        skills_label.set_halign(Gtk.Align.START)
        skills_label.set_line_wrap(True)
        frame_box.pack_start(skills_label, False, False, 0)
        
        remove_btn = Gtk.Button(label="Remove")
        remove_btn.set_tooltip_text("Remove this skill category")
        remove_btn.connect("clicked", lambda b: self.remove_item(frame, self.resume_data["skills"], skill_data))
        frame_box.pack_start(remove_btn, False, False, 0)
        
        frame.add(frame_box)
        self.skills_box.pack_start(frame, False, False, 0)
        self.skills_box.show_all()
    
    def remove_item(self, widget, data_list, item):
        data_list.remove(item)
        widget.destroy()
        logger.info("Removed item from resume data")
    
    def collect_form_data(self):
        self.resume_data["name"] = sanitize_input(self.name_entry.get_text())
        self.resume_data["subtitle"] = sanitize_input(self.subtitle_entry.get_text())
        self.resume_data["contact"]["website"] = sanitize_input(self.website_entry.get_text())
        self.resume_data["contact"]["email"] = sanitize_input(self.email_entry.get_text())
        self.resume_data["contact"]["phone"] = sanitize_input(self.phone_entry.get_text())
        
        try:
            validate_email(self.resume_data["contact"]["email"])
        except ValueError as e:
            logger.warning(f"Email validation warning: {e}")
    
    def on_preview_clicked(self, button):
        try:
            self.collect_form_data()
            html_content = self.generate_html()
            self.preview_buffer.set_text(html_content[:2000] + "\n\n... (preview truncated)")
            logger.info("Updated resume preview")
        except Exception as e:
            logger.error(f"Error generating preview: {e}")
            show_error(self, f"Error generating preview: {e}")
    
    def on_export_clicked(self, button):
        self.collect_form_data()
        
        dialog = Gtk.FileChooserDialog(
            title="Save Resume HTML",
            parent=self,
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE, Gtk.ResponseType.OK
        )
        dialog.set_current_name("resume.html")
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            try:
                path = Path(filename)
                if path.suffix != ".html":
                    path = path.with_suffix(".html")
                html_content = self.generate_html()
                with open(path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                logger.info(f"Exported resume to {path}")
                show_info(self, "Resume exported successfully!")
            except Exception as e:
                logger.error(f"Error exporting resume: {e}")
                show_error(self, f"Error exporting resume: {e}")
        
        dialog.destroy()
    
    def on_save_json(self, button):
        self.collect_form_data()
        
        dialog = Gtk.FileChooserDialog(
            title="Save Resume Data",
            parent=self,
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE, Gtk.ResponseType.OK
        )
        dialog.set_current_name("resume_data.json")
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            try:
                path = Path(filename)
                if path.suffix != ".json":
                    path = path.with_suffix(".json")
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(self.resume_data, f, indent=2, ensure_ascii=False)
                logger.info(f"Saved resume data to {path}")
            except Exception as e:
                logger.error(f"Error saving resume data: {e}")
                show_error(self, f"Error saving resume data: {e}")
        
        dialog.destroy()
    
    def on_load_json(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Load Resume Data",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        dialog.set_filter(Gtk.FileFilter().add_pattern("*.json"))
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    required_keys = ["name", "subtitle", "contact", "experience", "projects", "education", "skills"]
                    for key in required_keys:
                        if key not in data:
                            raise ValueError(f"Invalid resume data: missing {key}")
                    self.resume_data = data
                    self.populate_form()
                    logger.info(f"Loaded resume data from {filename}")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON file: {e}")
                show_error(self, f"Invalid JSON file: {e}")
            except Exception as e:
                logger.error(f"Error loading resume data: {e}")
                show_error(self, f"Error loading resume data: {e}")
        
        dialog.destroy()
    
    def populate_form(self):
        self.name_entry.set_text(self.resume_data.get("name", ""))
        self.subtitle_entry.set_text(self.resume_data.get("subtitle", ""))
        self.website_entry.set_text(self.resume_data["contact"].get("website", ""))
        self.email_entry.set_text(self.resume_data["contact"].get("email", ""))
        self.phone_entry.set_text(self.resume_data["contact"].get("phone", ""))
        
        for child in self.experience_box.get_children():
            child.destroy()
        for child in self.projects_box.get_children():
            child.destroy()
        for child in self.education_box.get_children():
            child.destroy()
        for child in self.skills_box.get_children():
            child.destroy()
        
        for exp in self.resume_data.get("experience", []):
            self.add_experience_item(exp)
        for proj in self.resume_data.get("projects", []):
            self.add_project_item(proj)
        for edu in self.resume_data.get("education", []):
            self.add_education_item(edu)
        for skill in self.resume_data.get("skills", []):
            self.add_skill_item(skill)
    
    def generate_html(self):
        exp_html = ""
        for exp in self.resume_data.get("experience", []):
            bullets = "".join([f"<li>{escape_text(item)}</li>" for item in exp.get("bullets", [])])
            exp_html += f"""
            <section class="blocks">
                <div class="date"><span>{escape_text(exp["end_date"])}</span><span>{escape_text(exp["start_date"])}</span></div>
                <div class="decorator"></div>
                <div class="details">
                    <header><h3>{escape_text(exp["title"])}</h3><span class="place">{escape_text(exp["company"])}</span><span class="location">{escape_text(exp.get("location", ""))}</span></header>
                    <div>
                        <ul>
                            {bullets}
                        </ul>
                    </div>
                </div>
            </section>"""
        
        proj_html = ""
        for proj in self.resume_data.get("projects", []):
            bullets = "".join([f"<li>{escape_text(item)}</li>" for item in proj.get("bullets", [])])
            proj_html += f"""
            <section class="blocks">
                <div class="date"><span>{escape_text(proj["end_date"])}</span><span>{escape_text(proj["start_date"])}</span></div>
                <div class="decorator"></div>
                <div class="details">
                    <header><h3>{escape_text(proj["title"])}</h3><span class="place">{escape_text(proj.get("subtitle", ""))}</span></header>
                    <div>
                        <ul>
                            {bullets}
                        </ul>
                    </div>
                </div>
            </section>"""
        
        edu_html = ""
        for edu in self.resume_data.get("education", []):
            edu_html += f"""
            <section class="blocks">
                <div class="date"><span>{escape_text(edu["end_date"])}</span><span>{escape_text(edu["start_date"])}</span></div>
                <div class="decorator"></div>
                <div class="details">
                    <header><h3>{escape_text(edu["degree"])}</h3><span class="place">{escape_text(edu["school"])}</span><span class="location">{escape_text(edu.get("location", ""))}</span></header>
                    <div>{escape_text(edu.get("notes", ""))}</div>
                </div>
            </section>"""
        
        skills_html = ""
        for skill in self.resume_data.get("skills", []):
            skills_html += f"<ul><li><strong>{escape_text(skill["category"])}:</strong></li><li>{escape_text(skill["skills"])}</li></ul>\n"
        
        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{name} Resume</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600|Source+Code+Pro:400" rel="stylesheet">
    <style>
        html {{ line-height: 1.15; -webkit-text-size-adjust: 100%; }}
        body {{ margin: 0; }}
        main {{ display: block; }}
        h1 {{ font-size: 2em; margin: 0.67em 0; }}
        hr {{ box-sizing: content-box; height: 0; overflow: visible; }}
        pre {{ font-family: monospace, monospace; font-size: 1em; }}
        a {{ background-color: transparent; }}
        abbr[title] {{ border-bottom: none; text-decoration: underline; text-decoration: underline dotted; }}
        b, strong {{ font-weight: bolder; }}
        code, kbd, samp {{ font-family: monospace, monospace; font-size: 1em; }}
        small {{ font-size: 80%; }}
        sub, sup {{ font-size: 75%; line-height: 0; position: relative; vertical-align: baseline; }}
        sub {{ bottom: -0.25em; }}
        sup {{ top: -0.5em; }}
        img {{ border-style: none; }}
        button, input, optgroup, select, textarea {{ font-family: inherit; font-size: 100%; line-height: 1.15; margin: 0; }}
        button, input {{ overflow: visible; }}
        button, select {{ text-transform: none; }}
        button, [type="button"], [type="reset"], [type="submit"] {{ -webkit-appearance: button; }}
        button::-moz-focus-inner, [type="button"]::-moz-focus-inner, [type="reset"]::-moz-focus-inner, [type="submit"]::-moz-focus-inner {{ border-style: none; padding: 0; }}
        button:-moz-focusring, [type="button"]:-moz-focusring, [type="reset"]:-moz-focusring, [type="submit"]:-moz-focusring {{ outline: 1px dotted ButtonText; }}
        fieldset {{ padding: 0.35em 0.75em 0.625em; }}
        legend {{ box-sizing: border-box; color: inherit; display: table; max-width: 100%; padding: 0; white-space: normal; }}
        progress {{ vertical-align: baseline; }}
        textarea {{ overflow: auto; }}
        [type="checkbox"], [type="radio"] {{ box-sizing: border-box; padding: 0; }}
        [type="number"]::-webkit-inner-spin-button, [type="number"]::-webkit-outer-spin-button {{ height: auto; }}
        [type="search"] {{ -webkit-appearance: textfield; outline-offset: -2px; }}
        [type="search"]::-webkit-search-decoration {{ -webkit-appearance: none; }}
        ::-webkit-file-upload-button {{ -webkit-appearance: button; font: inherit; }}
        details {{ display: block; }}
        summary {{ display: list-item; }}
        template {{ display: none; }}
        [hidden] {{ display: none; }}
        .fa {{ font-family: "Font Awesome 6 Free"; font-weight: 900; }}
        .fas, .far, .fab, .fa-solid, .fa-regular, .fa-brands, .fa {{ -moz-osx-font-smoothing: grayscale; -webkit-font-smoothing: antialiased; display: inline-block; font-style: normal; font-variant: normal; line-height: 1; text-rendering: auto; }}
        .fa-suitcase:before {{ content: "\\f0b1"; }}
        .fa-folder-open:before {{ content: "\\f07c"; }}
        .fa-graduation-cap:before {{ content: "\\f19d"; }}
        .fa-envelope:before {{ content: "\\f0e0"; }}
        .fa-phone:before {{ content: "\\f095"; }}
        .fa-code:before {{ content: "\\f121"; }}
        @page {{ size: letter portrait; margin: 0; }}
        * {{ box-sizing: border-box; }}
        :root {{
            --page-width: 8.5in;
            --page-height: 11in;
            --main-width: 6.4in;
            --sidebar-width: calc(var(--page-width) - var(--main-width));
            --decorator-horizontal-margin: 0.2in;
            --sidebar-horizontal-padding: 0.2in;
            --decorator-outer-offset-top: 10px;
            --decorator-outer-offset-left: -5.5px;
            --decorator-border-width: 1px;
            --decorator-outer-dim: 9px;
            --decorator-border: 1px solid #ccc;
            --row-blocks-padding-top: 5pt;
            --date-block-width: 0.6in;
            --main-blocks-title-icon-offset-left: -19pt;
        }}
        body {{
            width: var(--page-width);
            height: var(--page-height);
            margin: 0;
            font-family: "Open Sans", sans-serif;
            font-weight: 300;
            line-height: 1.3;
            color: #444;
            hyphens: auto;
        }}
        h1, h2, h3 {{ margin: 0; color: #000; }}
        li {{ list-style-type: none; }}
        #main {{
            float: left;
            width: var(--main-width);
            padding: 0.25in 0.25in 0 0.25in;
            font-size: 7pt;
        }}
        #sidebar {{
            float: right;
            position: relative;
            width: var(--sidebar-width);
            height: 100%;
            padding: 0.6in var(--sidebar-horizontal-padding);
            background-color: #f2f2f2;
            font-size: 8.5pt;
        }}
        #title, h1, h2 {{ text-transform: uppercase; }}
        #title {{
            position: relative;
            left: 0.55in;
            margin-bottom: 0.3in;
            line-height: 1.2;
        }}
        #title h1 {{ font-weight: 300; font-size: 18pt; line-height: 1.5; }}
        #title h1 strong {{ margin: auto 2pt auto 4pt; font-weight: 600; }}
        .subtitle {{ font-size: 8pt; }}
        .main-block {{ margin-top: 0.1in; }}
        #main h2 {{
            position: relative;
            top: var(--row-blocks-padding-top);
            left: calc((var(--date-block-width) + var(--decorator-horizontal-margin)));
            font-weight: 400;
            font-size: 11pt;
            color: #555;
        }}
        #main h2 > i {{
            position: absolute;
            left: var(--main-blocks-title-icon-offset-left);
            z-index: 1;
            color: #444;
        }}
        #main h2::after {{
            height: calc(var(--row-blocks-padding-top) * 2);
            position: relative;
            top: calc(-1 * var(--row-blocks-padding-top));
            left: calc(-1 * var(--decorator-horizontal-margin));
            display: block;
            border-left: var(--decorator-border);
            z-index: 0;
            line-height: 0;
            font-size: 0;
            content: " ";
        }}
        #main h2 > .fa-graduation-cap {{ left: calc(var(--main-blocks-title-icon-offset-left) - 2pt); top: 2pt; }}
        #main h2 > .fa-suitcase {{ top: 1pt; }}
        #main h2 > .fa-folder-open {{ top: 1.5pt; }}
        .blocks {{ display: flex; flex-flow: row nowrap; }}
        .blocks > div {{ padding-top: var(--row-blocks-padding-top); }}
        .date {{
            flex: 0 0 var(--date-block-width);
            padding-top: calc(var(--row-blocks-padding-top) + 2.5pt);
            padding-right: var(--decorator-horizontal-margin);
            font-size: 7pt;
            text-align: right;
            line-height: 1;
        }}
        .date span {{ display: block; }}
        .date span:nth-child(2)::before {{
            position: relative;
            top: 1pt;
            right: 5.5pt;
            display: block;
            height: 10pt;
            content: "|";
        }}
        .decorator {{
            flex: 0 0 0;
            position: relative;
            width: 2pt;
            min-height: 100%;
            border-left: var(--decorator-border);
        }}
        .decorator::before {{
            position: absolute;
            top: var(--decorator-outer-offset-top);
            left: var(--decorator-outer-offset-left);
            content: " ";
            display: block;
            width: var(--decorator-outer-dim);
            height: var(--decorator-outer-dim);
            border-radius: calc(var(--decorator-outer-dim) / 2);
            background-color: #fff;
        }}
        .decorator::after {{
            position: absolute;
            top: calc(var(--decorator-outer-offset-top) + var(--decorator-border-width));
            left: calc(var(--decorator-outer-offset-left) + var(--decorator-border-width));
            content: " ";
            display: block;
            width: calc(var(--decorator-outer-dim) - (var(--decorator-border-width) * 2));
            height: calc(var(--decorator-outer-dim) - (var(--decorator-border-width) * 2));
            border-radius: calc((var(--decorator-outer-dim) - (var(--decorator-border-width) * 2)) / 2);
            background-color: #555;
        }}
        .blocks:last-child .decorator {{ margin-bottom: 0.25in; }}
        .details {{
            flex: 1 0 0;
            padding-left: var(--decorator-horizontal-margin);
            padding-top: calc(var(--row-blocks-padding-top) - 0.5pt);
        }}
        .details header {{ color: #000; }}
        .details h3 {{ font-size: 9pt; }}
        .main-block:not(.concise) .details div {{ margin: 0.18in 0 0.1in 0; }}
        .main-block:not(.concise) .blocks:last-child .details div {{ margin-bottom: 0; }}
        .main-block.concise .details div:not(.concise) {{ padding: 0.05in 0 0.07in 0; }}
        .details .place {{ float: left; font-size: 7.5pt; }}
        .details .location {{ float: right; }}
        .details div {{ clear: both; }}
        .details .location::before {{
            display: inline-block;
            position: relative;
            right: 3pt;
            top: 0.25pt;
            font-family: "Font Awesome 6 Free";
            font-weight: normal;
            font-style: normal;
            text-decoration: inherit;
            content: "\\f041";
        }}
        #main ul {{ padding-left: 0.07in; margin: 0.08in 0; }}
        #main li {{ margin: 0 0 0.025in 0; }}
        #main li::before {{ position: relative; margin-left: -4.25pt; content: "• "; }}
        .details .concise ul {{ margin: 0; -webkit-columns: 2; -moz-columns: 2; columns: 2; }}
        .details .concise li {{ margin: 0; margin-left: 0; }}
        #sidebar h1 {{ font-weight: 400; font-size: 11pt; }}
        .side-block {{ margin-top: 0.5in; }}
        #contact ul {{ margin-top: 0.05in; padding-left: 0; font-family: "Source Code Pro"; font-weight: 400; line-height: 1.75; }}
        #contact li > i {{ width: 9pt; text-align: right; }}
        #skills {{ line-height: 1.5; }}
        #skills ul {{ margin: 0.05in 0 0.15in; padding: 0; }}
        #disclaimer {{
            position: absolute;
            bottom: var(--sidebar-horizontal-padding);
            right: var(--sidebar-horizontal-padding);
            font-size: 7.5pt;
            font-style: italic;
            line-height: 1.1;
            text-align: right;
            color: #777;
        }}
        #disclaimer code {{ color: #666; font-family: "Source Code Pro"; font-weight: 400; font-style: normal; }}
    </style>
</head>
<body lang="en">
    <section id="main">
        <header id="title">
            <h1>{name}</h1>
            <span class="subtitle">{subtitle}</span>
        </header>
        <section class="main-block">
            <h2><i class="fa fa-suitcase"></i> Experience</h2>
            {experience}
        </section>
        <section class="main-block">
            <h2><i class="fa fa-folder-open"></i> Projects</h2>
            {projects}
        </section>
        <section class="main-block concise">
            <h2><i class="fa fa-graduation-cap"></i> Education & Certifications</h2>
            {education}
        </section>
    </section>
    <aside id="sidebar">
        <div class="side-block" id="contact">
            <h1>Contact Info</h1>
            <ul>
                <a href="{website}">{website_display}</a>
                <li><i class="fa fa-envelope"></i> <a href="mailto:{email}">{email}</a></li>
                <li><i class="fa fa-phone"></i> {phone}</li>
            </ul>
        </div>
        <div class="side-block" id="skills">
            <h1>Skills</h1>
            {skills}
        </div>
        <div class="side-block" id="disclaimer">
            Built with Resume Builder
        </div>
    </aside>
</body>
</html>"""
        
        website = self.resume_data["contact"].get("website", "")
        website_display = website.replace("https://", "").replace("http://", "")
        
        return html_template.format(
            name=escape_text(self.resume_data.get("name", "Your Name")),
            subtitle=escape_text(self.resume_data.get("subtitle", "Your Subtitle")),
            experience=exp_html,
            projects=proj_html,
            education=edu_html,
            skills=skills_html,
            website=escape_text(website),
            website_display=escape_text(website_display),
            email=escape_text(self.resume_data["contact"].get("email", "")),
            phone=escape_text(self.resume_data["contact"].get("phone", ""))
        )


class ExperienceDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Add Experience", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        self.set_default_size(500, 400)
        
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        
        self.title_entry = self.add_entry(box, "Job Title:")
        self.company_entry = self.add_entry(box, "Company:")
        self.location_entry = self.add_entry(box, "Location:")
        self.start_date_entry = self.add_entry(box, "Start Date:")
        self.end_date_entry = self.add_entry(box, "End Date:")
        
        label = Gtk.Label(label="Bullet Points (one per line):", xalign=0)
        box.pack_start(label, False, False, 0)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_size_request(-1, 150)
        
        self.bullets_view = Gtk.TextView()
        self.bullets_view.set_wrap_mode(Gtk.WrapMode.WORD)
        scroll.add(self.bullets_view)
        box.pack_start(scroll, True, True, 0)
        
        self.show_all()
    
    def add_entry(self, box, label_text):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        label = Gtk.Label(label=label_text, xalign=0)
        label.set_size_request(100, -1)
        entry = Gtk.Entry()
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(entry, True, True, 0)
        box.pack_start(hbox, False, False, 0)
        return entry
    
    def get_data(self):
        buffer = self.bullets_view.get_buffer()
        start, end = buffer.get_bounds()
        bullets_text = buffer.get_text(start, end, True)
        bullets = [sanitize_input(line.strip()) for line in bullets_text.split("\n") if line.strip()]
        
        return {
            "title": sanitize_input(self.title_entry.get_text()),
            "company": sanitize_input(self.company_entry.get_text()),
            "location": sanitize_input(self.location_entry.get_text()),
            "start_date": sanitize_input(self.start_date_entry.get_text()),
            "end_date": sanitize_input(self.end_date_entry.get_text()),
            "bullets": bullets
        }


class ProjectDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Add Project", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        self.set_default_size(500, 400)
        
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        
        self.title_entry = self.add_entry(box, "Project Title:")
        self.subtitle_entry = self.add_entry(box, "Subtitle:")
        self.start_date_entry = self.add_entry(box, "Start Date:")
        self.end_date_entry = self.add_entry(box, "End Date:")
        
        label = Gtk.Label(label="Bullet Points (one per line):", xalign=0)
        box.pack_start(label, False, False, 0)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_size_request(-1, 150)
        
        self.bullets_view = Gtk.TextView()
        self.bullets_view.set_wrap_mode(Gtk.WrapMode.WORD)
        scroll.add(self.bullets_view)
        box.pack_start(scroll, True, True, 0)
        
        self.show_all()
    
    def add_entry(self, box, label_text):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        label = Gtk.Label(label=label_text, xalign=0)
        label.set_size_request(100, -1)
        entry = Gtk.Entry()
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(entry, True, True, 0)
        box.pack_start(hbox, False, False, 0)
        return entry
    
    def get_data(self):
        buffer = self.bullets_view.get_buffer()
        start, end = buffer.get_bounds()
        bullets_text = buffer.get_text(start, end, True)
        bullets = [sanitize_input(line.strip()) for line in bullets_text.split("\n") if line.strip()]
        
        return {
            "title": sanitize_input(self.title_entry.get_text()),
            "subtitle": sanitize_input(self.subtitle_entry.get_text()),
            "start_date": sanitize_input(self.start_date_entry.get_text()),
            "end_date": sanitize_input(self.end_date_entry.get_text()),
            "bullets": bullets
        }


class EducationDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Add Education", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        self.set_default_size(400, 300)
        
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        
        self.degree_entry = self.add_entry(box, "Degree:")
        self.school_entry = self.add_entry(box, "School:")
        self.location_entry = self.add_entry(box, "Location:")
        self.start_date_entry = self.add_entry(box, "Start Date:")
        self.end_date_entry = self.add_entry(box, "End Date:")
        self.notes_entry = self.add_entry(box, "Notes:")
        
        self.show_all()
    
    def add_entry(self, box, label_text):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        label = Gtk.Label(label=label_text, xalign=0)
        label.set_size_request(100, -1)
        entry = Gtk.Entry()
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(entry, True, True, 0)
        box.pack_start(hbox, False, False, 0)
        return entry
    
    def get_data(self):
        return {
            "degree": sanitize_input(self.degree_entry.get_text()),
            "school": sanitize_input(self.school_entry.get_text()),
            "location": sanitize_input(self.location_entry.get_text()),
            "start_date": sanitize_input(self.start_date_entry.get_text()),
            "end_date": sanitize_input(self.end_date_entry.get_text()),
            "notes": sanitize_input(self.notes_entry.get_text())
        }


class SkillDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Add Skill Category", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        self.set_default_size(400, 200)
        
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        
        self.category_entry = self.add_entry(box, "Category:")
        self.skills_entry = self.add_entry(box, "Skills:")
        
        self.show_all()
    
    def add_entry(self, box, label_text):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        label = Gtk.Label(label=label_text, xalign=0)
        label.set_size_request(100, -1)
        entry = Gtk.Entry()
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(entry, True, True, 0)
        box.pack_start(hbox, False, False, 0)
        return entry
    
    def get_data(self):
        return {
            "category": sanitize_input(self.category_entry.get_text()),
            "skills": sanitize_input(self.skills_entry.get_text())
        }


def main():
    """Main entry point for the application."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Resume Builder - Create professional HTML resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  resume_builder.py                  # Launch GTK desktop interface
  resume_builder.py --web            # Launch web interface
  resume_builder.py --web --port 8080  # Web interface on port 8080
  resume_builder.py --help           # Show this help message
        """
    )
    parser.add_argument("--web", action="store_true", help="Run web interface instead of GTK")
    parser.add_argument("--host", default="0.0.0.0", help="Host for web server (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5000, help="Port for web server (default: 5000)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for web server")
    
    args = parser.parse_args()
    
    if args.web:
        logger.info(f"Starting Resume Builder web interface on {args.host}:{args.port}")
        try:
            from web_app import app
            app.run(host=args.host, port=args.port, debug=args.debug)
        except ImportError as e:
            logger.error(f"Flask not installed. Install with: pip install flask")
            print(f"Error: Flask is required for web mode. Install with: pip install flask")
            sys.exit(1)
    else:
        logger.info("Starting Resume Builder GTK interface")
        try:
            win = ResumeBuilder()
            win.connect("destroy", Gtk.main_quit)
            win.show_all()
            Gtk.main()
        except NameError:
            print("Error: GTK3 is not available. Use --web for web interface or install GTK3.")
            print("On Ubuntu/Debian: sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0")
            print("On Fedora: sudo dnf install python3-gobject gtk3")
            print("On Arch: sudo pacman -S python-gobject gtk3")
            sys.exit(1)


if __name__ == "__main__":
    main()
