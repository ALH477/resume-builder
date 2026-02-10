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
from html_generator import generate_html as generate_resume_html, escape_text

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
        
        if self.resume_data["contact"]["email"]:
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
        return generate_resume_html(self.resume_data)


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
        
        data = {
            "title": sanitize_input(self.title_entry.get_text()),
            "company": sanitize_input(self.company_entry.get_text()),
            "location": sanitize_input(self.location_entry.get_text()),
            "start_date": sanitize_input(self.start_date_entry.get_text()),
            "end_date": sanitize_input(self.end_date_entry.get_text()),
            "bullets": bullets
        }
        
        if not data["title"]:
            raise ValueError("Job title is required")
        if not data["company"]:
            raise ValueError("Company is required")
        
        validate_date(data["start_date"])
        validate_date(data["end_date"])
        
        return data


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
        
        data = {
            "title": sanitize_input(self.title_entry.get_text()),
            "subtitle": sanitize_input(self.subtitle_entry.get_text()),
            "start_date": sanitize_input(self.start_date_entry.get_text()),
            "end_date": sanitize_input(self.end_date_entry.get_text()),
            "bullets": bullets
        }
        
        if not data["title"]:
            raise ValueError("Project title is required")
        
        validate_date(data["start_date"])
        validate_date(data["end_date"])
        
        return data


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
        data = {
            "degree": sanitize_input(self.degree_entry.get_text()),
            "school": sanitize_input(self.school_entry.get_text()),
            "location": sanitize_input(self.location_entry.get_text()),
            "start_date": sanitize_input(self.start_date_entry.get_text()),
            "end_date": sanitize_input(self.end_date_entry.get_text()),
            "notes": sanitize_input(self.notes_entry.get_text())
        }
        
        if not data["degree"]:
            raise ValueError("Degree is required")
        if not data["school"]:
            raise ValueError("School is required")
        
        validate_date(data["start_date"])
        validate_date(data["end_date"])
        
        return data


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
        data = {
            "category": sanitize_input(self.category_entry.get_text()),
            "skills": sanitize_input(self.skills_entry.get_text())
        }
        
        if not data["category"]:
            raise ValueError("Skill category is required")
        if not data["skills"]:
            raise ValueError("Skills are required")
        
        return data


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
