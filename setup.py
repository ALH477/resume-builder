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

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="resume-builder-gtk",
    version="1.1.0",
    author="ALH477",
    description="A GTK3 and web-based resume builder that generates professional HTML resumes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ALH477/resume-builder",
    py_modules=["resume_builder", "web_app"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Office/Business",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyGObject>=3.36.0; platform_system!='Windows'",
    ],
    extras_require={
        "web": ["flask>=2.0.0"],
        "docker": ["flask>=2.0.0"],
    },
    entry_points={
        "console_scripts": [
            "resume-builder=resume_builder:main",
        ],
    },
    license="Apache-2.0",
)
