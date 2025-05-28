"""Модуль для работы с задачами."""

import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("task_manager.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Task:
    """Класс для представления задачи.
    
    Атрибуты:
        description (str): Описание задачи.
        due_date (str): Срок выполнения в формате 'YYYY-MM-DD'.
        status (bool): Статус выполнения (False - не выполнено, True - выполнено).
    """
    
    def __init__(self, description: str, due_date: str):
        """Инициализирует задачу.
        
        Args:
            description: Описание задачи.
            due_date: Срок выполнения в формате 'YYYY-MM-DD'.
            
        Raises:
            ValueError: Если описание пустое или дата имеет неверный формат.
        """
        if not description.strip():
            error_msg = "Описание задачи не может быть пустым"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        try:
            # Проверяем, что дата соответствует формату YYYY-MM-DD
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError as e:
            error_msg = f"Неверный формат даты: {due_date}. Используйте формат 'YYYY-MM-DD'"
            logger.error(error_msg)
            raise ValueError(error_msg) from e
            
        self.description = description.strip()
        self.due_date = due_date
        self.status = False
        logger.info(f"Создана новая задача: {self}")
    
    def mark_as_done(self) -> None:
        """Отмечает задачу как выполненную."""
        if not self.status:
            self.status = True
            logger.info(f"Задача отмечена как выполненная: {self}")
        else:
            logger.warning(f"Попытка отметить уже выполненную задачу: {self}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Возвращает представление задачи в виде словаря.
        
        Returns:
            Словарь с данными задачи.
        """
        return {
            'description': self.description,
            'due_date': self.due_date,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Создает задачу из словаря.
        
        Args:
            data: Словарь с данными задачи.
            
        Returns:
            Экземпляр класса Task.
        """
        task = cls(data['description'], data['due_date'])
        task.status = data.get('status', False)
        return task
    
    def __str__(self) -> str:
        """Возвращает строковое представление задачи."""
        status_str = "✅ Выполнено" if self.status else "❌ Не выполнено"
        due_date = datetime.strptime(self.due_date, '%Y-%m-%d').strftime('%d.%m.%Y')
        return f"{self.description} (до {due_date}) - {status_str}"
    
    def __repr__(self) -> str:
        """Возвращает формальное строковое представление объекта."""
        return f"Task(description='{self.description}', due_date='{self.due_date}', status={self.status})"


class TaskManager:
    """Класс для управления списком задач."""
    
    def __init__(self):
        """Инициализирует менеджер задач с пустым списком."""
        self.tasks: List[Task] = []
    
    def add_task(self, description: str, due_date: str) -> Task:
        """Добавляет новую задачу.
        
        Args:
            description: Описание задачи.
            due_date: Срок выполнения в формате 'YYYY-MM-DD'.
            
        Returns:
            Созданная задача.
            
        Raises:
            ValueError: Если не удалось создать задачу.
        """
        try:
            task = Task(description, due_date)
            self.tasks.append(task)
            logger.info(f"Задача добавлена: {task}")
            return task
        except ValueError as e:
            logger.error(f"Ошибка при добавлении задачи: {e}")
            raise
    
    def get_task(self, description: str) -> Optional[Task]:
        """Находит задачу по описанию.
        
        Args:
            description: Описание искомой задачи.
            
        Returns:
            Найденная задача или None, если не найдена.
        """
        for task in self.tasks:
            if task.description.lower() == description.lower():
                return task
        return None
    
    def mark_task_completed(self, description: str) -> bool:
        """Отмечает задачу как выполненную.
        
        Args:
            description: Описание задачи для отметки.
            
        Returns:
            True, если задача найдена и отмечена, иначе False.
        """
        task = self.get_task(description)
        if task:
            task.mark_as_done()
            return True
        logger.warning(f"Задача не найдена: {description}")
        return False
    
    def get_current_tasks(self) -> List[Task]:
        """Возвращает список невыполненных задач.
        
        Returns:
            Список невыполненных задач.
        """
        return [task for task in self.tasks if not task.status]
    
    def get_completed_tasks(self) -> List[Task]:
        """Возвращает список выполненных задач.
        
        Returns:
            Список выполненных задач.
        """
        return [task for task in self.tasks if task.status]
    
    def remove_task(self, description: str) -> bool:
        """Удаляет задачу.
        
        Args:
            description: Описание задачи для удаления.
            
        Returns:
            True, если задача найдена и удалена, иначе False.
        """
        task = self.get_task(description)
        if task:
            self.tasks.remove(task)
            logger.info(f"Задача удалена: {task}")
            return True
        return False
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """Возвращает список всех задач в виде словарей.
        
        Returns:
            Список словарей с данными задач.
        """
        return [task.to_dict() for task in self.tasks]
    
    @classmethod
    def from_dict(cls, data: List[Dict[str, Any]]) -> 'TaskManager':
        """Создает менеджер задач из списка словарей.
        
        Args:
            data: Список словарей с данными задач.
            
        Returns:
            Экземпляр класса TaskManager.
        """
        manager = cls()
        for task_data in data:
            try:
                manager.tasks.append(Task.from_dict(task_data))
            except (KeyError, ValueError) as e:
                logger.error(f"Ошибка при загрузке задачи: {e}")
        return manager
    
    def __str__(self) -> str:
        """Возвращает строковое представление менеджера задач."""
        if not self.tasks:
            return "Нет задач"
        
        current_tasks = self.get_current_tasks()
        completed_tasks = self.get_completed_tasks()
        
        result = ["=== Управление задачами ==="]
        
        if current_tasks:
            result.append("\nТекущие задачи:")
            for i, task in enumerate(current_tasks, 1):
                result.append(f"{i}. {task}")
        else:
            result.append("\nНет текущих задач.")
            
        if completed_tasks:
            result.append("\nВыполненные задачи:")
            for i, task in enumerate(completed_tasks, 1):
                result.append(f"{i}. {task}")
        
        return "\n".join(result)
    
    def __len__(self) -> int:
        """Возвращает количество задач."""
        return len(self.tasks)
