"""Модуль для работы с магазинами и товарами."""

import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict, field

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("store_manager.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Product:
    """Класс для представления товара.
    
    Атрибуты:
        name: Название товара.
        price: Цена товара (должна быть положительной).
        category: Категория товара (опционально).
    """
    name: str
    price: float
    category: str = "Без категории"
    
    def __post_init__(self):
        """Проверяет корректность данных при инициализации."""
        if not self.name.strip():
            error_msg = "Название товара не может быть пустым"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if self.price <= 0:
            error_msg = f"Цена товара должна быть положительной: {self.price}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def to_dict(self) -> Dict[str, Any]:
        """Возвращает представление товара в виде словаря."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Создает товар из словаря."""
        return cls(**data)
    
    def __str__(self) -> str:
        """Возвращает строковое представление товара."""
        return f"{self.name} - {self.price:.2f} руб. ({self.category})"


class Store:
    """Класс для представления магазина.
    
    Атрибуты:
        name: Название магазина.
        address: Адрес магазина.
        items: Словарь товаров, где ключ - название товара, значение - экземпляр Product.
    """
    
    def __init__(self, name: str, address: str, initial_items: Optional[Dict[str, Dict[str, Any]]] = None):
        """Инициализирует магазин.
        
        Args:
            name: Название магазина.
            address: Адрес магазина.
            initial_items: Начальный ассортимент товаров.
        """
        if not name.strip():
            error_msg = "Название магазина не может быть пустым"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if not address.strip():
            error_msg = "Адрес магазина не может быть пустым"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        self.name = name.strip()
        self.address = address.strip()
        self._items: Dict[str, Product] = {}
        
        # Добавляем начальные товары, если они предоставлены
        if initial_items:
            for item_name, item_data in initial_items.items():
                try:
                    self.add_item(
                        name=item_name,
                        price=item_data.get('price'),
                        category=item_data.get('category', 'Без категории')
                    )
                except (ValueError, KeyError) as e:
                    logger.error(f"Ошибка при добавлении начального товара {item_name}: {e}")
        
        logger.info(f"Создан новый магазин: {self}")
    
    def add_item(self, name: str, price: float, category: str = "Без категории") -> Product:
        """Добавляет товар в ассортимент магазина.
        
        Args:
            name: Название товара.
            price: Цена товара.
            category: Категория товара.
            
        Returns:
            Добавленный товар.
            
        Raises:
            ValueError: Если товар с таким названием уже существует.
        """
        if name in self._items:
            error_msg = f"Товар с названием '{name}' уже существует в магазине '{self.name}'"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        product = Product(name=name, price=price, category=category)
        self._items[name] = product
        logger.info(f"Добавлен товар в магазин '{self.name}': {product}")
        return product
    
    def remove_item(self, name: str) -> bool:
        """Удаляет товар из ассортимента.
        
        Args:
            name: Название товара для удаления.
            
        Returns:
            True, если товар был удален, иначе False.
        """
        if name in self._items:
            del self._items[name]
            logger.info(f"Товар '{name}' удален из магазина '{self.name}'")
            return True
        logger.warning(f"Товар '{name}' не найден в магазине '{self.name}'")
        return False
    
    def get_item(self, name: str) -> Optional[Product]:
        """Возвращает товар по названию.
        
        Args:
            name: Название товара.
            
        Returns:
            Найденный товар или None, если не найден.
        """
        return self._items.get(name)
    
    def get_price(self, name: str) -> Optional[float]:
        """Возвращает цену товара по названию.
        
        Args:
            name: Название товара.
            
        Returns:
            Цена товара или None, если товар не найден.
        """
        product = self.get_item(name)
        if product:
            return product.price
        return None
    
    def update_price(self, name: str, new_price: float) -> bool:
        """Обновляет цену товара.
        
        Args:
            name: Название товара.
            new_price: Новая цена товара.
            
        Returns:
            True, если цена обновлена, иначе False.
            
        Raises:
            ValueError: Если новая цена некорректна.
        """
        if new_price <= 0:
            error_msg = f"Цена товара должна быть положительной: {new_price}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if name in self._items:
            old_price = self._items[name].price
            self._items[name].price = new_price
            logger.info(
                f"Цена товара '{name}' в магазине '{self.name}' обновлена: "
                f"{old_price:.2f} -> {new_price:.2f} руб."
            )
            return True
            
        logger.warning(f"Товар '{name}' не найден в магазине '{self.name}' для обновления цены")
        return False
    
    def get_items_by_category(self, category: str) -> List[Product]:
        """Возвращает список товаров по категории.
        
        Args:
            category: Название категории.
            
        Returns:
            Список товаров в указанной категории.
        """
        return [product for product in self._items.values() if product.category == category]
    
    def get_categories(self) -> List[str]:
        """Возвращает список всех категорий товаров в магазине.
        
        Returns:
            Список уникальных категорий.
        """
        return list({product.category for product in self._items.values()})
    
    def to_dict(self) -> Dict[str, Any]:
        """Возвращает представление магазина в виде словаря.
        
        Returns:
            Словарь с данными магазина и его ассортиментом.
        """
        return {
            'name': self.name,
            'address': self.address,
            'items': {name: product.to_dict() for name, product in self._items.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Store':
        """Создает магазин из словаря.
        
        Args:
            data: Словарь с данными магазина.
            
        Returns:
            Экземпляр класса Store.
        """
        store = cls(name=data['name'], address=data['address'])
        for item_name, item_data in data.get('items', {}).items():
            try:
                store._items[item_name] = Product.from_dict(item_data)
            except (ValueError, KeyError) as e:
                logger.error(f"Ошибка при загрузке товара {item_name}: {e}")
        return store
    
    def __str__(self) -> str:
        """Возвращает строковое представление магазина."""
        items_count = len(self._items)
        categories = self.get_categories()
        
        result = [
            f"=== {self.name} ===",
            f"Адрес: {self.address}",
            f"Товаров в ассортименте: {items_count}",
            f"Категории: {', '.join(categories) if categories else 'Нет категорий'}"
        ]
        
        if items_count > 0:
            result.append("\nАссортимент товаров:")
            for category in sorted(categories):
                result.append(f"\n  {category}:")
                for product in sorted(
                    self.get_items_by_category(category),
                    key=lambda p: p.name
                ):
                    result.append(f"  - {product}")
        
        return "\n".join(result)
    
    def __len__(self) -> int:
        """Возвращает количество товаров в магазине."""
        return len(self._items)
    
    def __contains__(self, item_name: str) -> bool:
        """Проверяет наличие товара в магазине."""
        return item_name in self._items
