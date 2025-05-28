from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="task_manager_store",
    version="1.0.0",
    author="Ваше имя",
    author_email="ваш.email@example.com",
    description="Библиотека для управления задачами и магазинами",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ваш-пользователь/task-manager-store",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'python-dateutil>=2.8.2',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'isort>=5.10.1',
            'mypy>=0.910',
            'flake8>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'task-manager=task_manager_store.main:main',
        ],
    },
)
