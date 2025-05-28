.PHONY: help install test lint format check-format type-check docs clean

# Определение переменных
PYTHON = python
PIP = pip
PYTEST = pytest
FLAKE8 = flake8
BLACK = black
ISORT = isort
MYPY = mypy
SPHINX_BUILD = sphinx-build

# Список всех Python-файлов
PYTHON_FILES = $(shell find . -name '*.py' -not -path '*/venv/*' -not -path '*/build/*' -not -path '*/dist/*' -not -path '*/__pycache__/*' -not -path '*/.*')

# Цель по умолчанию
help:
	@echo "Доступные команды:"
	@echo "  make install     - Установка зависимостей"
	@echo "  make dev         - Установка зависимостей для разработки"
	@echo "  make test        - Запуск тестов"
	@echo "  make test-cov    - Запуск тестов с покрытием"
	@echo "  make lint        - Проверка кода с помощью flake8"
	@echo "  make format      - Форматирование кода с помощью black и isort"
	@echo "  make check-format - Проверка форматирования кода"
	@echo "  make type-check  - Проверка типов с помощью mypy"
	@echo "  make docs        - Сборка документации"
	@echo "  make clean       - Очистка временных файлов"

# Установка зависимостей
install:
	$(PIP) install -e .


# Установка зависимостей для разработки
dev:
	$(PIP) install -e ".[dev]"

# Запуск тестов
test:
	$(PYTEST) tests/ -v

# Запуск тестов с покрытием
test-cov:
	$(PYTEST) --cov=user_management --cov-report=term-missing tests/

# Проверка кода
lint:
	$(FLAKE8) user_management/ tests/

# Форматирование кода
format:
	$(BLACK) $(PYTHON_FILES)
	$(ISORT) $(PYTHON_FILES)

# Проверка форматирования кода
check-format:
	$(BLACK) --check $(PYTHON_FILES) || (echo "Ошибка форматирования. Запустите 'make format' для автоматического исправления."; exit 1)
	$(ISORT) --check-only $(PYTHON_FILES) || (echo "Ошибка сортировки импортов. Запустите 'make format' для автоматического исправления."; exit 1)

# Проверка типов
type-check:
	$(MYPY) user_management/ tests/

# Сборка документации
docs:
	$(SPHINX_BUILD) -b html docs/source/ docs/build/html

# Очистка временных файлов
clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	find . -type d -name '.hypothesis' -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/ .mypy_cache/ .pytest_cache/ .hypothesis/
	cd docs && make clean

# Проверка перед коммитом
pre-commit: check-format lint type-check test
