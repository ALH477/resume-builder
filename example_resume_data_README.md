# Example Resume Data JSON

This file contains an example JSON structure that demonstrates how to format resume data for the Resume Builder application.

## File: `example_resume_data.json`

The example JSON file contains a complete resume for "Asher LeRoy" with all sections populated according to the template structure.

## JSON Structure Overview

```json
{
  "name": "string",
  "subtitle": "string", 
  "summary": "string (optional)",
  "contact": {
    "website": "string",
    "email": "string", 
    "phone": "string"
  },
  "experience": [
    {
      "title": "string",
      "company": "string",
      "location": "string",
      "start_date": "string",
      "end_date": "string", 
      "bullets": ["string", "string"]
    }
  ],
  "projects": [
    {
      "title": "string",
      "subtitle": "string",
      "start_date": "string",
      "end_date": "string",
      "bullets": ["string", "string"]
    }
  ],
  "education": [
    {
      "degree": "string",
      "school": "string", 
      "location": "string",
      "start_date": "string",
      "end_date": "string",
      "notes": "string"
    }
  ],
  "skills": [
    {
      "category": "string",
      "skills": "string"
    }
  ],
  "achievements": ["string", "string"]
}
```

## Field Descriptions

### Required Fields
- **name**: Full name of the person
- **subtitle**: Professional title or tagline
- **contact**: Object containing contact information
  - **website**: Personal or professional website URL
  - **email**: Email address
  - **phone**: Phone number

### Optional Sections
- **summary**: Professional summary with optional line breaks
- **experience**: Array of work experience entries
- **projects**: Array of project entries  
- **education**: Array of education entries
- **skills**: Array of skill categories
- **achievements**: Array of achievement bullet points

### Date Format
Use consistent date formats such as:
- "2022", "2023", "2024"
- "Jan 2024", "Feb 2023"
- "Present" for current positions

### Bullet Points
- Use the "bullets" array for list items
- Each bullet should be a string
- HTML tags are escaped automatically

## Usage

1. Load this JSON file in the Resume Builder application
2. Modify the data to match your own information
3. Export as HTML or save as JSON for future editing

## Validation

The JSON structure has been tested and validated against the HTML generator. It will produce a properly formatted resume when processed through the system.

## Template Compatibility

This JSON structure is designed to work with the `template.html` file in this project, which generates a professional, print-ready resume with:
- Two-column layout (main content + sidebar)
- Timeline-style experience and project sections
- Professional typography using Courier New
- Print-optimized styling
- Font Awesome icons