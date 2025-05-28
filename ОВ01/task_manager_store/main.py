"""
Главный модуль приложения для управления задачами и магазинами.

Этот модуль демонстрирует использование классов Task, TaskManager и Store.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any

# Импортируем наши классы
from .task import Task, TaskManager
from .store import Store, Product

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_demo_tasks() -> TaskManager:
    """Настраивает демонстрационные задачи.
    
    Returns:
        TaskManager с демонстрационными задачами.
    """
    logger.info("Настройка демонстрационных задач...")
    
    # Создаем менеджер задач
    task_manager = TaskManager()
    
    # Добавляем демонстрационные задачи
    tasks = [
        ("Купить молоко", (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")),
        ("Сделать ДЗ по ОВ01", (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")),
        ("Позвонить маме", (datetime.now() + timedelta(days=0)).strftime("%Y-%m-%d")),
        ("Записаться на курсы", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")),
        ("Сходить в спортзал", (datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d")),
    ]
    
    for desc, due_date in tasks:
        task_manager.add_task(description=desc, due_date=due_date)
    
    # Отмечаем некоторые задачи как выполненные
    task_manager.mark_task_completed("Позвонить маме")
    task_manager.mark_task_completed("Сходить в спортзал")
    
    return task_manager

def setup_demo_stores() -> Dict[str, Store]:
    """Настраивает демонстрационные магазины.
    
    Returns:
        Словарь с демонстрационными магазинами.
    """
    logger.info("Настройка демонстрационных магазинов...")
    
    # Создаем демонстрационные магазины
    stores = {}
    
    # 1. Продуктовый магазин
    stores["grocery"] = Store(
        name="Продукты у дома",
        address="ул. Ленина, 1",
        initial_items={
            "Хлеб": {"price": 50.0, "category": "Хлебобулочные изделия"},
            "Молоко": {"price": 70.5, "category": "Молочные продукты"},
            "Яйца": {"price": 120.0, "category": "Молочные продукты"},
            "Яблоки": {"price": 150.0, "category": "Фрукты и овощи"},
        }
    )
    
    # 2. Книжный магазин
    stores["bookstore"] = Store(
        name="Книжный мир",
        address="пр. Мира, 15",
        initial_items={
            "Война и мир": {"price": 1500.0, "category": "Классика"},
            "1984": {"price": 800.0, "category": "Антиутопия"},
            "Мастер и Маргарита": {"price": 1200.0, "category": "Классика"},
            "Python для чайников": {"price": 2000.0, "category": "Программирование"},
        }
    )
    
    # 3. Магазин электроники
    stores["electronics"] = Store(
        name="ТехноСила",
        address="ул. Гагарина, 42",
        initial_items={
            "Смартфон X": {"price": 25000.0, "category": "Смартфоны"},
            "Ноутбук Y": {"price": 60000.0, "category": "Ноутбуки"},
            "Наушники Z": {"price": 5000.0, "category": "Аксессуары"},
            "Планшет W": {"price": 35000.0, "category": "Планшеты"},
        }
    )
    
    return stores

def demo_task_manager():
    """Демонстрация работы с задачами."""
    print("\n" + "="*50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ С ЗАДАЧАМИ".center(50))
    print("="*50)
    
    # Создаем менеджер задач с демонстрационными данными
    task_manager = setup_demo_tasks()
    
    # Выводим текущие задачи
    print("\nТекущие задачи:")
    for i, task in enumerate(task_manager.get_current_tasks(), 1):
        print(f"{i}. {task}")
    
    # Выводим выполненные задачи
    completed = task_manager.get_completed_tasks()
    if completed:
        print("\nВыполненные задачи:")
        for i, task in enumerate(completed, 1):
            print(f"{i}. {task}")
    
    # Добавляем новую задачу
    print("\nДобавляем новую задачу...")
    task_manager.add_task("Записаться к врачу", (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"))
    
    # Отмечаем задачу как выполненную
    print("\nОтмечаем задачу как выполненную...")
    task_manager.mark_task_completed("Купить молоко")
    
    # Выводим обновленный список задач
    print("\nОбновленный список задач:")
    print(task_manager)

def demo_store_operations():
    """Демонстрация работы с магазинами."""
    print("\n" + "="*50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ С МАГАЗИНАМИ".center(50))
    print("="*50)
    
    # Создаем демонстрационные магазины
    stores = setup_demo_stores()
    
    # Выводим информацию о магазинах
    for store in stores.values():
        print("\n" + "-"*50)
        print(store)
    
    # Выбираем продуктовый магазин для демонстрации операций
    grocery = stores["grocery"]
    
    # Демонстрация добавления товара
    print("\nДобавляем новый товар в продуктовый магазин...")
    try:
        grocery.add_item("Сыр", 350.0, "Молочные продукты")
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    # Демонстрация обновления цены
    print("\nОбновляем цену товара...")
    grocery.update_price("Яблоки", 180.0)
    
    # Демонстрация удаления товара
    print("\nУдаляем товар...")
    grocery.remove_item("Яйца")
    
    # Выводим обновленную информацию о магазине
    print("\nОбновленная информация о магазине:")
    print(grocery)
    
    # Демонстрация поиска по категории
    print("\nТовары категории 'Молочные продукты':")
    for product in grocery.get_items_by_category("Молочные продукты"):
        print(f"- {product}")

def main():
    """Главная функция приложения."""
    try:
        # Демонстрация работы с задачами
        demo_task_manager()
        
        # Демонстрация работы с магазинами
        demo_store_operations()
        
        print("\n" + "="*50)
        print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА".center(50))
        print("="*50)
        
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}", exc_info=True)
        print(f"\nПроизошла ошибка: {e}")

if __name__ == "__main__":
    main()
