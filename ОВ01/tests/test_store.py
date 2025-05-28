"""Модуль для тестирования функциональности работы с магазинами."""

import unittest
import shutil
from pathlib import Path
import sys
from datetime import datetime

# Добавляем родительскую директорию в путь для импорта
sys.path.append(str(Path(__file__).parent.parent))

from task_manager_store.store import Store, Product

class TestProduct(unittest.TestCase):
    """Тесты для класса Product."""
    
    def test_product_creation(self):
        """Тест создания товара."""
        product = Product("Тестовый товар", 100.0, "Тестовая категория")
        self.assertEqual(product.name, "Тестовый товар")
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.category, "Тестовая категория")
    
    def test_invalid_price(self):
        """Тест создания товара с недопустимой ценой."""
        with self.assertRaises(ValueError):
            Product("Товар с отрицательной ценой", -10.0, "Категория")
        
        with self.assertRaises(ValueError):
            Product("Бесплатный товар", 0.0, "Категория")
    
    def test_empty_name(self):
        """Тест создания товара с пустым названием."""
        with self.assertRaises(ValueError):
            Product("", 100.0, "Категория")


class TestStore(unittest.TestCase):
    """Тесты для класса Store."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        # Создаем тестовый магазин
        self.store = Store("Тестовый магазин", "ул. Тестовая, 123")
        
        # Добавляем тестовые товары
        self.store.add_item("Товар 1", 100.0, "Категория 1")
        self.store.add_item("Товар 2", 200.0, "Категория 1")
        self.store.add_item("Товар 3", 300.0, "Категория 2")
    
    def test_store_creation(self):
        """Тест создания магазина."""
        self.assertEqual(self.store.name, "Тестовый магазин")
        self.assertEqual(self.store.address, "ул. Тестовая, 123")
        self.assertEqual(len(self.store), 3)
    
    def test_add_item(self):
        """Тест добавления товара."""
        initial_count = len(self.store)
        self.store.add_item("Новый товар", 150.0, "Новая категория")
        self.assertEqual(len(self.store), initial_count + 1)
        
        # Проверяем, что нельзя добавить товар с существующим именем
        with self.assertRaises(ValueError):
            self.store.add_item("Новый товар", 200.0, "Другая категория")
    
    def test_remove_item(self):
        """Тест удаления товара."""
        initial_count = len(self.store)
        self.assertTrue(self.store.remove_item("Товар 1"))
        self.assertEqual(len(self.store), initial_count - 1)
        self.assertFalse(self.store.remove_item("Несуществующий товар"))
    
    def test_get_price(self):
        """Тест получения цены товара."""
        self.assertEqual(self.store.get_price("Товар 1"), 100.0)
        self.assertIsNone(self.store.get_price("Несуществующий товар"))
    
    def test_update_price(self):
        """Тест обновления цены товара."""
        self.assertTrue(self.store.update_price("Товар 1", 150.0))
        self.assertEqual(self.store.get_price("Товар 1"), 150.0)
        
        # Проверяем, что нельзя установить недопустимую цену
        with self.assertRaises(ValueError):
            self.store.update_price("Товар 1", -10.0)
        
        # Проверяем, что нельзя обновить цену несуществующего товара
        self.assertFalse(self.store.update_price("Несуществующий товар", 100.0))
    
    def test_get_items_by_category(self):
        """Тест получения товаров по категории."""
        category1_items = self.store.get_items_by_category("Категория 1")
        self.assertEqual(len(category1_items), 2)
        self.assertTrue(all(item.category == "Категория 1" for item in category1_items))
        
        # Проверяем пустую категорию
        self.assertEqual(len(self.store.get_items_by_category("Несуществующая категория")), 0)
    
    def test_get_categories(self):
        """Тест получения списка категорий."""
        categories = self.store.get_categories()
        self.assertEqual(len(categories), 2)
        self.assertIn("Категория 1", categories)
        self.assertIn("Категория 2", categories)
    
    def test_serialization(self):
        """Тест сериализации и десериализации."""
        # Сериализуем магазин
        store_data = self.store.to_dict()
        
        # Создаем новый магазин из данных
        new_store = Store.from_dict(store_data)
        
        # Проверяем, что данные загрузились корректно
        self.assertEqual(self.store.name, new_store.name)
        self.assertEqual(self.store.address, new_store.address)
        self.assertEqual(len(self.store), len(new_store))
        
        # Проверяем, что товары загрузились корректно
        if len(self.store) > 0 and len(new_store) > 0:
            item_name = next(iter(self.store._items))
            self.assertIn(item_name, new_store._items)
            self.assertEqual(self.store._items[item_name].name, new_store._items[item_name].name)
            self.assertEqual(self.store._items[item_name].price, new_store._items[item_name].price)
            self.assertEqual(self.store._items[item_name].category, new_store._items[item_name].category)


class TestStoreInitialization(unittest.TestCase):
    """Тесты инициализации магазина с начальными данными."""
    
    def test_initialization_with_items(self):
        """Тест инициализации с начальным ассортиментом."""
        initial_items = {
            "Товар A": {"price": 100.0, "category": "Категория A"},
            "Товар B": {"price": 200.0, "category": "Категория B"}
        }
        
        store = Store("Магазин с начальными товарами", "Адрес", initial_items)
        self.assertEqual(len(store), 2)
        self.assertEqual(store.get_price("Товар A"), 100.0)
        self.assertEqual(store.get_price("Товар B"), 200.0)
    
    def test_invalid_initial_items(self):
        """Тест обработки недопустимых начальных данных."""
        initial_items = {
            "Товар A": {"price": -100.0, "category": "Категория A"},  # Неверная цена
            "Товар B": {"price": 200.0}  # Отсутствует категория
        }
        
        # Магазин должен быть создан, но только с валидными товарами
        store = Store("Магазин с невалидными товарами", "Адрес", initial_items)
        # Проверяем, что невалидные товары не были добавлены
        self.assertEqual(len(store), 0)


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
            logging.FileHandler(test_log_dir / "test_store.log"),
            logging.StreamHandler()
        ]
    )
    
    try:
        unittest.main()
    finally:
        # Удаляем временную директорию после выполнения тестов
        shutil.rmtree(test_log_dir, ignore_errors=True)
