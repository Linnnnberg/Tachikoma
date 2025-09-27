#!/usr/bin/env python3
"""
Tachikoma Multi-Agent AI System Setup Script
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tachikoma",
    version="0.1.0",
    author="Tachikoma Development Team",
    author_email="tachikoma@example.com",
    description="A dynamic, character-driven multi-agent AI system",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/tachikoma",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "ui": [
            "streamlit>=1.25.0",
            "plotly>=5.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tachikoma=tachikoma.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
