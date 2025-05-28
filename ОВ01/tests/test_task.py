"""Модуль для тестирования функциональности работы с задачами."""

import unittest
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import os

# Добавляем родительскую директорию в путь для импорта
import sys
sys.path.append(str(Path(__file__).parent.parent))

from task_manager_store.task import Task, TaskManager

class TestTask(unittest.TestCase):
    """Тесты для класса Task."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.task = Task("Тестовая задача", self.tomorrow)
    
    def test_task_creation(self):
        """Тест создания задачи."""
        self.assertEqual(self.task.description, "Тестовая задача")
        self.assertEqual(self.task.due_date, self.tomorrow)
        self.assertFalse(self.task.status)
    
    def test_mark_as_done(self):
        """Тест отметки задачи как выполненной."""
        self.task.mark_as_done()
        self.assertTrue(self.task.status)
    
    def test_invalid_due_date(self):
        """Тест создания задачи с неверной датой."""
        with self.assertRaises(ValueError):
            Task("Неверная дата", "2023-13-45")
    
    def test_empty_description(self):
        """Тест создания задачи с пустым описанием."""
        with self.assertRaises(ValueError):
            Task("", self.tomorrow)


class TestTaskManager(unittest.TestCase):
    """Тесты для класса TaskManager."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.manager = TaskManager()
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Добавляем тестовые задачи
        self.manager.add_task("Задача 1", self.today)
        self.manager.add_task("Задача 2", self.tomorrow)
        self.manager.add_task("Задача 3", self.yesterday)
        self.manager.mark_task_completed("Задача 3")
    
    def test_add_task(self):
        """Тест добавления задачи."""
        initial_count = len(self.manager.tasks)
        self.manager.add_task("Новая задача", self.tomorrow)
        self.assertEqual(len(self.manager.tasks), initial_count + 1)
    
    def test_mark_completed(self):
        """Тест отметки задачи как выполненной."""
        self.assertTrue(self.manager.mark_task_completed("Задача 1"))
        self.assertFalse(self.manager.mark_task_completed("Несуществующая задача"))
    
    def test_get_current_tasks(self):
        """Тест получения текущих задач."""
        current_tasks = self.manager.get_current_tasks()
        self.assertEqual(len(current_tasks), 2)  # Задача 1 и Задача 2
        self.assertTrue(all(not task.status for task in current_tasks))
    
    def test_get_completed_tasks(self):
        """Тест получения выполненных задач."""
        completed_tasks = self.manager.get_completed_tasks()
        self.assertEqual(len(completed_tasks), 1)  # Только Задача 3
        self.assertTrue(all(task.status for task in completed_tasks))
    
    def test_remove_task(self):
        """Тест удаления задачи."""
        initial_count = len(self.manager.tasks)
        self.assertTrue(self.manager.remove_task("Задача 1"))
        self.assertEqual(len(self.manager.tasks), initial_count - 1)
        self.assertFalse(self.manager.remove_task("Несуществующая задача"))
    
    def test_serialization(self):
        """Тест сериализации и десериализации."""
        # Сохраняем текущие задачи
        tasks_data = self.manager.to_dict()
        
        # Создаем новый менеджер и загружаем задачи
        new_manager = TaskManager.from_dict(tasks_data)
        
        # Проверяем, что задачи загрузились корректно
        self.assertEqual(len(self.manager.tasks), len(new_manager.tasks))
        
        # Проверяем, что первая задача загрузилась корректно
        if self.manager.tasks and new_manager.tasks:
            original = self.manager.tasks[0]
            loaded = new_manager.tasks[0]
            self.assertEqual(original.description, loaded.description)
            self.assertEqual(original.due_date, loaded.due_date)
            self.assertEqual(original.status, loaded.status)


if __name__ == "__main__":
    # Создаем временную директорию для логов
    test_log_dir = Path("test_logs")
    test_log_dir.mkdir(exist_ok=True)
    
    # Настраиваем логирование для тестов
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(test_log_dir / "test_task.log"),
            logging.StreamHandler()
        ]
    )
    
    try:
        unittest.main()
    finally:
        # Удаляем временную директорию после выполнения тестов
        shutil.rmtree(test_log_dir, ignore_errors=True)
