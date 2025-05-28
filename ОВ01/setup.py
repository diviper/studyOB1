"""Настройка пакета для установки."""

from setuptools import setup, find_packages
from pathlib import Path

# Чтение README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Чтение зависимостей из requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="task_manager_store",
    version="1.0.0",
    author="Чурэн Дмитрий Сергеевич",
    author_email="churendmitriy@gmail.com",
    description="Библиотека для управления задачами и магазинами",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diviper/studyOB1",
    packages=find_packages(exclude=["tests*"]),
    package_data={
        "task_manager_store": ["py.typed"],
    },
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.10.0",
            "black>=22.0.0",
            "isort>=5.10.1",
            "mypy>=0.910",
            "flake8>=4.0.0",
            "flake8-docstrings>=1.6.0",
            "flake8-import-order>=0.18.1",
            "pre-commit>=2.17.0",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    keywords="task manager store inventory",
    project_urls={
        "Bug Reports": "https://github.com/diviper/studyOB1/issues",
        "Source": "https://github.com/diviper/studyOB1",
    },
    entry_points={
        "console_scripts": [
            "task-manager=task_manager_store.main:main",
        ],
    },
)
