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

import pytest
import json
from pathlib import Path
from html_generator import (
    escape_text,
    generate_experience_html,
    generate_projects_html,
    generate_education_html,
    generate_skills_html,
    generate_html
)


class TestHTMLGenerator:
    """Test HTML generation functions."""

    def test_escape_text_basic(self):
        """Test basic HTML escaping."""
        assert escape_text("<script>alert('xss')</script>") == "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"
        assert escape_text("Hello & World") == "Hello &amp; World"
        assert escape_text('Test "quotes"') == 'Test &quot;quotes&quot;'

    def test_escape_text_empty(self):
        """Test escaping of empty strings."""
        assert escape_text("") == ""
        assert escape_text(None) == ""

    def test_generate_experience_html(self):
        """Test experience section HTML generation."""
        experiences = [
            {
                'title': 'Software Engineer',
                'company': 'Tech Corp',
                'location': 'San Francisco',
                'start_date': '2020',
                'end_date': 'Present',
                'bullets': ['Developed web apps', 'Led team of 5']
            }
        ]
        html = generate_experience_html(experiences)
        assert 'Software Engineer' in html
        assert 'Tech Corp' in html
        assert 'San Francisco' in html
        assert 'Developed web apps' in html
        assert 'Led team of 5' in html

    def test_generate_projects_html(self):
        """Test projects section HTML generation."""
        projects = [
            {
                'title': 'Open Source Project',
                'subtitle': 'CLI tool for data processing',
                'start_date': '2023',
                'end_date': '2024',
                'bullets': ['Python implementation', '1000+ GitHub stars']
            }
        ]
        html = generate_projects_html(projects)
        assert 'Open Source Project' in html
        assert 'CLI tool for data processing' in html

    def test_generate_education_html(self):
        """Test education section HTML generation."""
        education = [
            {
                'degree': 'BS Computer Science',
                'school': 'University of Tech',
                'location': 'Boston',
                'start_date': '2016',
                'end_date': '2020',
                'notes': 'Summa Cum Laude'
            }
        ]
        html = generate_education_html(education)
        assert 'BS Computer Science' in html
        assert 'University of Tech' in html
        assert 'Summa Cum Laude' in html

    def test_generate_skills_html(self):
        """Test skills section HTML generation."""
        skills = [
            {'category': 'Programming', 'skills': 'Python, JavaScript, C++'},
            {'category': 'Tools', 'skills': 'Git, Docker, Kubernetes'}
        ]
        html = generate_skills_html(skills)
        assert 'Programming' in html
        assert 'Python' in html
        assert 'JavaScript' in html
        assert 'Tools' in html

    def test_generate_full_html(self):
        """Test complete HTML generation."""
        data = {
            'name': 'John Doe',
            'subtitle': 'Senior Software Engineer',
            'contact': {
                'website': 'https://johndoe.com',
                'email': 'john@example.com',
                'phone': '555-123-4567'
            },
            'experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Tech Corp',
                    'location': 'San Francisco',
                    'start_date': '2020',
                    'end_date': 'Present',
                    'bullets': ['Developed web apps']
                }
            ],
            'projects': [],
            'education': [],
            'skills': []
        }
        html = generate_html(data)
        assert 'John Doe' in html
        assert 'Senior Software Engineer' in html
        assert 'john@example.com' in html
        assert 'Software Engineer' in html
        assert '<!DOCTYPE html>' in html
        assert '</html>' in html

    def test_html_escaping_in_html_generation(self):
        """Test that user input is properly escaped in HTML output."""
        data = {
            'name': '<script>alert("xss")</script>',
            'subtitle': '& malicious input',
            'contact': {
                'website': 'https://example.com',
                'email': 'test@example.com',
                'phone': '555-1234'
            },
            'experience': [
                {
                    'title': 'Job with <script>',
                    'company': 'Company & Co',
                    'location': 'City',
                    'start_date': '2020',
                    'end_date': 'Present',
                    'bullets': ['<img src=x onerror=alert(1)>']
                }
            ],
            'projects': [],
            'education': [],
            'skills': []
        }
        html = generate_html(data)
        assert '&lt;script&gt;' in html
        assert '&amp;' in html
        assert '<script>' not in html


class TestValidation:
    """Test input validation functions."""

    def test_email_validation(self):
        """Test email validation."""
        from resume_builder import validate_email

        valid_emails = [
            'test@example.com',
            'user.name@example.co.uk',
            'test+tag@example.org'
        ]
        for email in valid_emails:
            assert validate_email(email) is True

        invalid_emails = [
            'invalid',
            'test@',
            '@example.com',
            'test..name@example.com'
        ]
        for email in invalid_emails:
            with pytest.raises(ValueError):
                validate_email(email)

    def test_email_validation_empty(self):
        """Test that empty email is allowed (optional field)."""
        from resume_builder import validate_email
        assert validate_email('') is True
        assert validate_email(None) is True

    def test_date_validation(self):
        """Test date validation."""
        from resume_builder import validate_date

        valid_dates = [
            '2024',
            '01/2024',
            'Jan 2024',
            '2024-01-15',
            'January 2024',
            'Present'
        ]
        for date in valid_dates:
            assert validate_date(date) is True

        invalid_dates = [
            'invalid date',
            '2024-13-01',
            'Not a date'
        ]
        for date in invalid_dates:
            with pytest.raises(ValueError):
                validate_date(date)

    def test_date_validation_empty(self):
        """Test that empty date is allowed (optional field)."""
        from resume_builder import validate_date
        assert validate_date('') is True
        assert validate_date(None) is True


class TestInputSanitization:
    """Test input sanitization functions."""

    def test_sanitize_input(self):
        """Test input sanitization."""
        from resume_builder import sanitize_input

        # Test HTML escaping
        assert '<script>' not in sanitize_input('<script>alert(1)</script>')
        assert '&lt;script&gt;' in sanitize_input('<script>alert(1)</script>')

        # Test max length
        long_text = 'a' * 20000
        sanitized = sanitize_input(long_text)
        assert len(sanitized) == 10000

        # Test whitespace trimming
        assert sanitize_input('  text  ') == 'text'

    def test_sanitize_input_none(self):
        """Test sanitization of None values."""
        from resume_builder import sanitize_input
        assert sanitize_input(None) == ''


class TestDataStructure:
    """Test resume data structure validation."""

    def test_valid_resume_data(self):
        """Test that valid resume data structure is accepted."""
        data = {
            'name': 'Test User',
            'subtitle': 'Developer',
            'contact': {
                'website': 'https://example.com',
                'email': 'test@example.com',
                'phone': '555-1234'
            },
            'experience': [],
            'projects': [],
            'education': [],
            'skills': []
        }
        # This should not raise any errors
        html = generate_html(data)
        assert html is not None

    def test_missing_optional_fields(self):
        """Test that missing optional fields are handled gracefully."""
        data = {
            'name': 'Test User',
            'subtitle': '',
            'contact': {
                'website': '',
                'email': '',
                'phone': ''
            },
            'experience': [],
            'projects': [],
            'education': [],
            'skills': []
        }
        html = generate_html(data)
        assert html is not None


class TestTemplateFile:
    """Test that template file exists and is readable."""

    def test_template_file_exists(self):
        """Test that the HTML template file exists."""
        template_path = Path(__file__).parent / 'templates' / 'resume_template.html'
        assert template_path.exists()

    def test_template_file_readable(self):
        """Test that the HTML template file is readable."""
        template_path = Path(__file__).parent / 'templates' / 'resume_template.html'
        content = template_path.read_text(encoding='utf-8')
        assert '<!DOCTYPE html>' in content
        assert '{name}' in content
        assert '{experience}' in content
        assert '</html>' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
