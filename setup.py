#!/usr/bin/env python3
"""
Package setup and installation configuration for not-warrior.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from __init__.py
version = {}
with open(Path(__file__).parent / "not_warrior" / "__init__.py") as f:
    exec(f.read(), version)

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "Notion-Taskwarrior Synchronization Service"

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    requirements = [
        "click>=8.0.0",
        "requests>=2.28.0",
        "python-dateutil>=2.8.0",
        "pydantic>=1.10.0",
        "PyYAML>=6.0",
        "python-dotenv>=0.19.0"
    ]

setup(
    name="not-warrior",
    version=version["__version__"],
    author="Your Name",
    author_email="your.email@example.com",
    description="Notion-Taskwarrior Synchronization Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/not-warrior",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
            "pre-commit>=2.20.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.8.0",
            "responses>=0.21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "not-warrior=not_warrior.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "not_warrior": [
            "config/*.yml",
            "config/*.yaml",
        ],
    },
    keywords="notion taskwarrior sync productivity task management",
    project_urls={
        "Bug Reports": "https://github.com/your-username/not-warrior/issues",
        "Source": "https://github.com/your-username/not-warrior",
        "Documentation": "https://github.com/your-username/not-warrior/blob/main/README.md",
    },
)