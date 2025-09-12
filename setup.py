#!/usr/bin/env python3
"""
🚀 Site Builder - Setup Script
"""

from setuptools import setup, find_packages
import os

# خواندن README
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Site Builder - ابزار استخراج و ساخت سایت"

# خواندن requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="pey-builder",
    version="1.0.0",
    author="Peysan Web",
    author_email="info@peysunweb.ir",
    description="ابزار کامل استخراج و ساخت سایت - PEY Builder",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/iman-noroozi/sitebuilder",
    project_urls={
        "Bug Reports": "https://github.com/iman-noroozi/sitebuilder/issues",
        "Source": "https://github.com/iman-noroozi/sitebuilder",
        "Documentation": "https://github.com/iman-noroozi/sitebuilder#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: Persian",
    ],
    python_requires=">=3.9",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-django>=4.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-django>=4.0.0",
            "pytest-cov>=4.0.0",
            "coverage>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sitebuilder-cli=sitebuilder_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml", "*.json"],
    },
    keywords=[
        "website-extractor",
        "template-extractor", 
        "site-builder",
        "web-scraping",
        "html-css-extractor",
        "django",
        "python",
        "nodejs",
        "grapesjs",
        "drag-drop",
        "persian",
        "rtl",
        "peysan-web"
    ],
    zip_safe=False,
)
