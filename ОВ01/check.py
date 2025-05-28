"""Скрипт для проверки работоспособности приложения."""

import sys
from pathlib import Path

# Добавляем родительскую директорию в путь для импорта
sys.path.append(str(Path(__file__).parent))

# Импортируем необходимые модули
from task_manager_store.task import Task, TaskManager
from task_manager_store.store import Store, Product

def test_task_manager():
    """Тестирование работы с задачами."""
    print("\n=== Тестирование менеджера задач ===")
    
    # Создаем менеджер задач
    manager = TaskManager()
    
    # Добавляем задачи
    manager.add_task("Купить молоко", "2025-06-01")
    manager.add_task("Позвонить маме", "2025-05-30")
    
    # Выводим текущие задачи
    print("\nТекущие задачи:")
    for task in manager.get_current_tasks():
        print(f"- {task}")
    
    # Отмечаем задачу как выполненную
    manager.mark_task_completed("Позвонить маме")
    
    # Выводим выполненные задачи
    print("\nВыполненные задачи:")
    for task in manager.get_completed_tasks():
        print(f"- {task}")
    
    print("\n✅ Тестирование менеджера задач завершено успешно!")

def test_store():
    """Тестирование работы с магазином."""
    print("\n=== Тестирование магазина ===")
    
    # Создаем магазин
    store = Store("Продуктовый", "ул. Примерная, 1")
    
    # Добавляем товары
    store.add_item("Молоко", 70.50, "Молочные продукты")
    store.add_item("Хлеб", 50.00, "Хлебобулочные изделия")
    store.add_item("Яблоки", 150.00, "Фрукты и овощи")
    
    # Выводим информацию о магазине
    print(f"\nМагазин: {store.name}")
    print(f"Адрес: {store.address}")
    print(f"Количество товаров: {len(store)}")
    
    # Выводим товары по категориям
    print("\nТовары по категориям:")
    for category in store.get_categories():
        print(f"\n{category}:")
        for item in store.get_items_by_category(category):
            print(f"- {item.name}: {item.price} руб.")
    
    # Обновляем цену товара
    store.update_price("Яблоки", 180.00)
    print("\nОбновленная цена на яблоки:", store.get_price("Яблоки"), "руб.")
    
    print("\n✅ Тестирование магазина завершено успешно!")

if __name__ == "__main__":
    print("=== Начало тестирования приложения ===\n")
    
    try:
        test_task_manager()
        test_store()
        print("\n=== Все тесты успешно пройдены! ===")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        raise
