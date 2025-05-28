"""Конфигурация тестового окружения."""

import pytest
from pathlib import Path
import shutil
import logging

# Настройка логирования для тестов
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tests/test.log"),
        logging.StreamHandler()
    ]
)

# Фикстуры для тестов
@pytest.fixture
def temp_dir():
    """Создает временную директорию для тестов и удаляет её после завершения."""
    temp_path = Path("temp_test_dir")
    temp_path.mkdir(exist_ok=True)
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def sample_store():
    """Создает тестовый магазин с демонстрационными данными."""
    from task_manager_store.store import Store
    store = Store("Тестовый магазин", "ул. Тестовая, 1")
    store.add_item("Товар 1", 100.0, "Категория 1")
    store.add_item("Товар 2", 200.0, "Категория 1")
    store.add_item("Товар 3", 300.0, "Категория 2")
    return store

@pytest.fixture
def task_manager():
    """Создает менеджер задач с демонстрационными данными."""
    from task_manager_store.task import TaskManager
    from datetime import datetime, timedelta
    
    manager = TaskManager()
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    manager.add_task("Задача 1", today)
    manager.add_task("Задача 2", tomorrow)
    manager.mark_task_completed("Задача 1")
    
    return manager
