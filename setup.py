"""Setup script for Gravity Framework."""

from setuptools import setup, find_packages  # type: ignore
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="gravity-framework",
    version="0.1.0",
    description="A Python framework for discovering, installing, connecting, and orchestrating microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gravity Framework Team",
    author_email="team@gravityframework.dev",
    url="https://github.com/GravtyWaves/GravityFrameWork",
    project_urls={
        "Documentation": "https://gravity-framework.readthedocs.io",
        "Source": "https://github.com/GravtyWaves/GravityFrameWork",
        "Tracker": "https://github.com/GravtyWaves/GravityFrameWork/issues",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.23.2",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "black>=23.12.1",
            "isort>=5.13.2",
            "mypy>=1.8.0",
            "ruff>=0.1.9",
            "pre-commit>=3.6.0",
            "bandit>=1.7.6",
            "safety>=3.0.1",
        ],
        "docs": [
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.5.3",
            "mkdocstrings[python]>=0.24.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gravity=gravity_framework.cli.main:app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    keywords="microservices orchestration framework service-discovery deployment docker kubernetes",
    license="MIT",
    zip_safe=False,
)
