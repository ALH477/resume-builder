# Resume Template Formatting Documentation

## Overview

This document describes the complete page formatting structure extracted from `template.html` in the resume builder project. This formatting is used to generate professional, print-ready HTML resumes.

---

## Table of Contents

1. [Page Dimensions](#page-dimensions)
2. [CSS Variables](#css-variables)
3. [Layout Architecture](#layout-architecture)
4. [Typography System](#typography-system)
5. [Component Specifications](#component-specifications)
6. [Icons](#icons)
7. [Spacing System](#spacing-system)
8. [Print Styling](#print-styling)
9. [HTML Structure](#html-structure)

---

## Page Dimensions

### Standard Paper Size
- **Size**: Letter (8.5" × 11")
- **Orientation**: Portrait
- **Margin**: 0 (full-bleed layout)

```
┌──────────────────────────────────────────────────────────────┐
│                       8.5 inches (page-width)                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                                                        │  │
│  │                    Content Area                        │  │
│  │                         11                             │  │
│  │                         in                             │  │
│  │                         c                              │  │
│  │                         h                              │  │
│  │                         .                              │  │
│  │                         (                               │  │
│  │                         p                                │  │
│  │                         a                                │  │
│  │                         c                                │  │
│  │                         e                                │  │
│  │                         -                                │  │
│  │                         h                                │  │
│  │                         e                                │  │
│  │                         i                                │  │
│  │                         g                                │  │
│  │                         h                                │  │
│  │                         t                                │  │
│  │                          )                             │  │
│  └────────────────────────────────────────────────────────┘  │
│                        11 inches (page-height)               │
└──────────────────────────────────────────────────────────────┘
```

---

## CSS Variables

The template uses 13 CSS variables defined in `:root` for consistent styling and easy customization:

| Variable | Value | Description |
|----------|-------|-------------|
| `--page-width` | `8.5in` | Total page width |
| `--page-height` | `11in` | Total page height |
| `--main-width` | `6.4in` | Main content column width |
| `--sidebar-width` | `calc(8.5in - 6.4in)` | Sidebar width (2.1in) |
| `--decorator-horizontal-margin` | `0.2in` | Horizontal spacing for decorators |
| `--sidebar-horizontal-padding` | `0.2in` | Sidebar side padding |
| `--decorator-outer-offset-top` | `10px` | Vertical offset for decorator circles |
| `--decorator-outer-offset-left` | `-5.5px` | Horizontal offset for decorator circles |
| `--decorator-border-width` | `1px` | Decorator border width |
| `--decorator-outer-dim` | `9px` | Outer decorator circle diameter |
| `--decorator-border` | `1px solid #ccc` | Decorator border style |
| `--row-blocks-padding-top` | `5pt` | Top padding for timeline blocks |
| `--date-block-width` | `0.6in` | Date column width |
| `--main-blocks-title-icon-offset-left` | `-19pt` | Icon positioning offset |

---

## Layout Architecture

### Flexbox Layout System

The layout uses a two-column flexbox design:

```html
<body>
  <section id="main">          <!-- 6.4in content column -->
    <header id="title">...</header>
    <section class="main-block">...</section>
  </section>
  <aside id="sidebar">          <!-- 2.1in sidebar -->
    <div class="side-block">...</div>
  </aside>
</body>
```

### Main Section (#main)

- **Flex**: `1 1 6.4in` (grows to fill space, minimum 6.4in)
- **Padding**: `0.25in 0.25in 0 0.25in` (left, top, right, bottom)
- **Font Size**: `7pt`
- **Content Flow**:
  1. Header (#title)
  2. Experience section (.main-block)
  3. Projects section (.main-block)
  4. Education section (.main-block)

### Sidebar Section (#sidebar)

- **Flex**: `0 0 2.1in` (fixed width, doesn't grow)
- **Height**: `100%` (full page height)
- **Padding**: `0.6in var(--sidebar-horizontal-padding)` (0.6in top/bottom, 0.2in sides)
- **Background Color**: `#f2f2f2` (light gray)
- **Font Size**: `8.5pt`
- **Display**: `flex` with `flex-direction: column` and `justify-content: space-between`
- **Content Flow** (bottom-aligned due to justify-content):
  1. Contact Info section
  2. Skills section
  3. Achievements section
  4. Footer section
  5. Disclaimer (bottom)

---

## Typography System

### Base Font Settings

| Property | Value | Applies To |
|----------|-------|------------|
| Font Family | `"Courier New", monospace` | Body text |
| Font Weight | `400` (normal) | Body text |
| Line Height | `1.3` | Body text |
| Color | `#444` (dark gray) | Body text |
| Hyphens | `auto` | Body text |

### Font Sizes by Context

| Context | Font Size | Weight | Color |
|---------|-----------|--------|-------|
| h1 (Name) | `18pt` | `400` | `#000` |
| h2 (Section Headers) | `11pt` | `400` | `#555` |
| h3 (Job Title) | `9pt` | `600` (bold) | `#000` |
| Subtitle | `8pt` | `400` | `#333` |
| Summary | `8pt` | `400` | `#333` |
| Place (Company) | `7.5pt` | `400` | inherited |
| Location | `5pt` | `400` | inherited |
| Date | `7pt` | `400` | inherited |
| Main Body | `7pt` | `400` | `#444` |
| Sidebar Body | `8.5pt` | `400` | inherited |

### Line Heights by Section

| Section | Line Height |
|---------|-------------|
| Base | `1.3` |
| Title | `1.2` |
| Subtitle/Summary | `1.2` |
| Contact | `1.75` |
| Skills | `1.5` |
| Achievements | `1.5` |
| Disclaimer | `1.1` |

---

## Component Specifications

### Header (#title)

```
┌─────────────────────────────────────────────────────────────┐
│  #title (relative, left: 0.55in, margin-bottom: 0.3in)     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ h1 (18pt, line-height: 1.5, uppercase)             │   │
│  │ "Asher LeRoy"                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ .subtitle (8pt, #333)                               │   │
│  │ "Cybersecurity Innovator | Founder | ...           │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ .summary (8pt, #333, line-height: 1.2)             │   │
│  │ Self-taught...<br>Architected...<br>alongside...   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**HTML Structure:**
```html
<header id="title">
    <h1>{name}</h1>
    <span class="subtitle">{subtitle}</span>
    <div class="summary">{summary with <br> tags}</div>
</header>
```

### Timeline Block (.blocks)

Each experience, project, or education item uses this reusable structure:

```
┌──────────────────────────────────────────────────────────────────────┐
│ .blocks (flex row, nowrap)                                            │
│ ┌──────┬──────────┬────────────────────────────────────────────────┐ │
│ │ date │decorator │ .details                                       │ │
│ │0.6in │  2pt     │ flex: 1 0 0                                  │ │
│ │      │          │ padding-left: 0.2in                          │ │
│ │      │          │ padding-top: 4.5pt (5pt - 0.5pt)             │ │
│ │      │          │                                              │ │
│ │ span │  ○●      │ ┌────────────────────────────────────────┐ │ │
│ │(left│  (9px)   │ │ header                                   │ │ │
│ │ date)│          │ │ ┌───┬────────┬─────────────────────┐  │ │ │
│ │      │          │ │h3 │ place  │ location              │  │ │ │
│ │ span │          │ │   │7.5pt   │ 5pt with 📍            │  │ │ │
│ │(right│          │ │   │        │                         │  │ │ │
│ │ date)│          │ │   │        │                         │  │ │ │
│ └──────┴──────────┤ │   │        │                         │  │ │ │
│ │ date separator │ │   │        │                         │  │ │ │
│ │ (vertical \|)  │ │   │        │                         │  │ │ │
│ └──────┴──────────┤ │   │        │                         │  │ │ │
│ │      │          │ │   │        │                         │  │ │ │
│ │      │          │ │   │        │ ul/li (7pt)             │  │ │ │
│ │      │          │ │   │        │ • Achievement           │  │ │ │
│ │      │          │ │   │        │ • Achievement           │  │ │ │
│ │      │          │ │   │        │ • Achievement           │  │ │ │
│ │      │          │ └───┴────────┴─────────────────────┘  │ │ │
│ │      │          │                                         │ │ │
│ │      │          │ div (margin: 0.18in 0 0.1in 0)        │ │ │
│ └──────┴──────────┴─────────────────────────────────────────┘ │
```

**HTML Structure:**
```html
<section class="blocks">
    <div class="date">
        <span>{start_date}</span>
        <span>{end_date}</span>
    </div>
    <div class="decorator"></div>
    <div class="details">
        <header>
            <h3>{title}</h3>
            <span class="place">{company}</span>
            <span class="location">{location}</span>
        </header>
        <div>
            <ul>
                <li>{bullet point 1}</li>
                <li>{bullet point 2}</li>
            </ul>
        </div>
    </div>
</section>
```

### Decorator Component

The decorator creates a timeline visualization with circles:

```
 decorator (2pt width, border-left: 1px solid #ccc)
 ┌──
 │  before (9px circle, white #fff, centered on line)
 │  ●
 │
 │  after (7px circle, dark #555, centered on line)
 │  ●
 │
 │  (continue for all timeline items...)
```

**CSS Implementation:**
```css
.decorator::before {
    /* 9px white circle */
}
.decorator::after {
    /* 7px dark circle */
}
```

### Details Section

The details section contains job/project information:

```
┌───────────────────────────────────────────────────────────────┐
│ .details                                                      │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ header (color: #000)                                    │   │
│ │ ┌───┬────────────────────┬───────────────────────────┐  │   │
│ │ │h3 │ .place             │ .location                 │  │   │
│ │ │9pt│ 7.5pt, left-float  │ 5pt, right-float with 📍  │  │   │
│ │ │   │                      │                           │  │   │
│ │ └───┴────────────────────┴───────────────────────────┘  │   │
│ └─────────────────────────────────────────────────────────┘   │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ div (margin: 0.18in 0 0.1in 0)                         │   │
│ │ ul (padding-left: 0.07in, margin: 0.08in 0)            │   │
│ │ li (margin: 0 0 0.025in 0)                             │   │
│ │ li::before (content: '• ', margin-left: -4.25pt)       │   │
│ └─────────────────────────────────────────────────────────┘   │
```

---

## Icons

### Font Awesome Setup

```css
.fa {
    font-family: "Font Awesome 6 Free";
    font-weight: 900;
}
```

### Used Icons

| Class | Unicode | Usage | Position |
|-------|---------|-------|----------|
| `fa-suitcase` | `\f0b1` | Experience section h2 icon | top: 1pt |
| `fa-folder-open` | `\f07c` | Projects section h2 icon | top: 1.5pt |
| `fa-graduation-cap` | `\f19d` | Education section h2 icon | top: 2pt, left: -21pt |
| `fa-envelope` | `\f0e0` | Contact email icon | inline |
| `fa-phone` | `\f095` | Contact phone icon | inline |
| `fa-globe` | `\f0ac` | Contact website icon | inline |
| `fa-location-dot` | `\f3c5` | Location marker | before location span |

### Icon Positioning in Headers

```css
#main h2 > .fa-graduation-cap {
    left: calc(var(--main-blocks-title-icon-offset-left) - 2pt);
    top: 2pt;
}
#main h2 > .fa-suitcase {
    top: 1pt;
}
#main h2 > .fa-folder-open {
    top: 1.5pt;
}
```

---

## Spacing System

### Page & Section Spacing

| Element | Property | Value |
|---------|----------|-------|
| @page margin | margin | 0 |
| body margin | margin | 0 |
| #main padding | padding | 0.25in 0.25in 0 0.25in |
| #sidebar padding | padding | 0.6in 0.2in |
| .main-block margin-top | margin-top | 0.1in |
| .side-block margin-top | margin-top | 0.5in |

### Timeline Block Spacing

| Component | Property | Value |
|-----------|----------|-------|
| .blocks padding-top | padding-top | 5pt |
| .date padding-top | padding-top | 7.5pt (5pt + 2.5pt) |
| .details padding-left | padding-left | 0.2in |
| .details padding-top | padding-top | 4.5pt (5pt - 0.5pt) |
| decorator horizontal margin | - | 0.2in |
| decorator vertical offset | top | 10px |

### List Spacing

| Element | Property | Value |
|---------|----------|-------|
| ul padding-left | padding-left | 0.07in |
| ul margin | margin | 0.08in 0 |
| li margin | margin | 0 0 0.025in 0 |
| li::before margin-left | margin-left | -4.25pt |
| details div margin | margin | 0.18in 0 0.1in 0 |
| details div margin (last) | margin-bottom | 0 |

### Typography Spacing

| Element | Property | Value |
|---------|----------|-------|
| h1 strong margin | margin | auto 2pt auto 4pt |
| location pseudo right | right | 3pt |
| location pseudo top | top | 0.25pt |
| date separator right | right | 5.5pt |
| date separator top | top | 1pt |

---

## Print Styling

### Print Media Query

```css
@media print {
    /* Override body margins for printing */
    body {
        margin: 0;
        padding: 0;
    }
    
    /* Make sidebar white (not light gray) */
    #sidebar {
        background-color: white !important;
    }
    
    /* Make all links black without underlines */
    a {
        color: black !important;
        text-decoration: none !important;
    }
    
    /* Make decorators black and white */
    .decorator,
    .decorator::before,
    .decorator::after {
        border-color: black !important;
        background-color: white !important;
    }
    
    /* Hide disclaimer (footer) */
    #disclaimer {
        display: none;
    }
    
    /* Prevent section breaks inside blocks */
    .main-block {
        page-break-inside: avoid;
    }
}
```

### Print Output Characteristics

- **Color**: Black and white only (no gray backgrounds)
- **Borders**: Solid black lines (no gray #ccc)
- **Sidebar**: White background (not light gray #f2f2f2)
- **Links**: No underlines (print optimization)
- **Footer**: Hidden (disclaimer removed)
- **Page breaks**: Avoided inside content blocks

---

## HTML Structure

### Root Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>...</head>
<body lang="en">
    <section id="main">...</section>
    <aside id="sidebar">...</aside>
</body>
</html>
```

### Main Section

```html
<section id="main">
    <header id="title">
        <h1>{name}</h1>
        <span class="subtitle">{subtitle}</span>
        <div class="summary">{summary}</div>
    </header>
    
    <section class="main-block">
        <h2><i class="fa fa-suitcase"></i> Experience</h2>
        {experience blocks...}
    </section>
    
    <section class="main-block">
        <h2><i class="fa fa-folder-open"></i> Projects</h2>
        {project blocks...}
    </section>
    
    <section class="main-block concise">
        <h2><i class="fa fa-graduation-cap"></i> Education</h2>
        {education blocks...}
    </section>
</section>
```

### Sidebar Section

```html
<aside id="sidebar">
    <div class="side-block" id="contact">
        <h1>Contact Info</h1>
        <ul>
            <li><i class="fa fa-globe"></i> <a href="{website}">{website_display}</a></li>
            <li><i class="fa fa-envelope"></i> <a href="mailto:{email}">{email}</a></li>
            <li><i class="fa fa-phone"></i> {phone}</li>
        </ul>
    </div>
    
    <div class="side-block" id="skills">
        <h1>Skills</h1>
        {skills list...}
    </div>
    
    <div class="side-block" id="achievements">
        <h1>Achievements</h1>
        {achievements list...}
    </div>
    
    <div class="side-block">
        <ul>
            <li>Built with HTML/CSS, delivered via Nginx</li>
        </ul>
    </div>
    
    <div class="side-block" id="disclaimer">
        Built with Resume Builder
    </div>
</aside>
```

---

## Customization Guide

### Changing Page Size

To change from Letter to A4:

```css
:root {
    --page-width: 8.27in;  /* A4 width */
    --page-height: 11.69in; /* A4 height */
}

@page {
    size: A4 portrait;
}
```

### Modifying Colors

Update CSS variables:

```css
:root {
    --decorator-border: 1px solid #999;  /* Darker gray */
    --sidebar-background: #e0e0e0;  /* Lighter gray */
}
```

### Adjusting Spacing

Modify padding/margin values:

```css
#main {
    padding: 0.5in;  /* More padding */
}

.main-block {
    margin-top: 0.2in;  /* More section spacing */
}
```

### Changing Fonts

Update font family variables:

```css
body {
    font-family: "Helvetica Neue", sans-serif;
}
```

---

## Template Files Reference

| File | Purpose |
|------|---------|
| `template.html` | Main HTML template with embedded CSS |
| `templates/resume_template.html` | Template for the web interface |
| `resume-builder.py` | Main application with GTK and web interfaces |
| `html_generator.py` | HTML generation functions |
| `web_app.py` | Flask web application |

---

**Last Updated**: February 9, 2026  
**Version**: 1.0.0  
**Source**: `/home/asher/Downloads/resume/template.html`
