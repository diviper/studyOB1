import datetime

class Task:
    """Класс для представления задачи."""
    def __init__(self, description, due_date):
        """Инициализирует задачу.

        Args:
            description (str): Описание задачи.
            due_date (str): Срок выполнения задачи (например, 'YYYY-MM-DD').
        """
        self.description = description
        self.due_date = due_date
        self.status = False  # False - не выполнено, True - выполнено

    def mark_as_done(self):
        """Отмечает задачу как выполненную."""
        self.status = True

    def __str__(self):
        status_str = "Выполнено" if self.status else "Не выполнено"
        return f"Задача: {self.description}, Срок: {self.due_date}, Статус: {status_str}"

# Список для хранения задач
tasks = []

def add_task(description, due_date):
    """Добавляет новую задачу в список.

    Args:
        description (str): Описание задачи.
        due_date (str): Срок выполнения.
    """
    new_task = Task(description, due_date)
    tasks.append(new_task)
    print(f"Задача '{description}' добавлена.")

def mark_task_completed(description):
    """Отмечает задачу как выполненную по её описанию.

    Args:
        description (str): Описание задачи для отметки.
    """
    found = False
    for task in tasks:
        if task.description == description:
            task.mark_as_done()
            print(f"Задача '{description}' отмечена как выполненная.")
            found = True
            break
    if not found:
        print(f"Задача '{description}' не найдена.")

def show_current_tasks():
    """Выводит список текущих (не выполненных) задач."""
    current_tasks = [task for task in tasks if not task.status]
    if not current_tasks:
        print("\nНет текущих невыполненных задач.")
        return

    print("\nТекущие задачи:")
    for task in current_tasks:
        print(task)

class Store:
    """Класс для представления магазина."""
    def __init__(self, name, address):
        """Инициализирует магазин.

        Args:
            name (str): Название магазина.
            address (str): Адрес магазина.
        """
        self.name = name
        self.address = address
        self.items = {}  # Словарь для товаров: {'название_товара': цена}

    def add_item(self, item_name, price):
        """Добавляет товар в ассортимент магазина.

        Args:
            item_name (str): Название товара.
            price (float): Цена товара.
        """
        if item_name in self.items:
            print(f"Товар '{item_name}' уже есть в магазине '{self.name}'.")
        else:
            self.items[item_name] = price
            print(f"Товар '{item_name}' (цена: {price}) добавлен в магазин '{self.name}'.")

    def remove_item(self, item_name):
        """Удаляет товар из ассортимента магазина.

        Args:
            item_name (str): Название товара для удаления.
        """
        if item_name in self.items:
            del self.items[item_name]
            print(f"Товар '{item_name}' удален из магазина '{self.name}'.")
        else:
            print(f"Товар '{item_name}' не найден в магазине '{self.name}'.")

    def get_price(self, item_name):
        """Возвращает цену товара по его названию.

        Args:
            item_name (str): Название товара.

        Returns:
            float or None: Цена товара, если он есть, иначе None.
        """
        price = self.items.get(item_name)
        if price is not None:
            print(f"Цена товара '{item_name}' в магазине '{self.name}': {price}")
            return price
        else:
            print(f"Товар '{item_name}' не найден в магазине '{self.name}'.")
            return None

    def update_price(self, item_name, new_price):
        """Обновляет цену существующего товара.

        Args:
            item_name (str): Название товара.
            new_price (float): Новая цена товара.
        """
        if item_name in self.items:
            self.items[item_name] = new_price
            print(f"Цена товара '{item_name}' в магазине '{self.name}' обновлена на {new_price}.")
        else:
            print(f"Товар '{item_name}' не найден в магазине '{self.name}' для обновления цены.")

    def __str__(self):
        return f"Магазин: {self.name}, Адрес: {self.address}, Ассортимент: {len(self.items)} товаров."

if __name__ == "__main__":
    # --- Тестирование менеджера задач ---
    print("--- Менеджер задач ---")
    add_task("Купить молоко", "2024-05-30")
    add_task("Сделать ДЗ по ОВ01", "2024-05-29")
    add_task("Позвонить маме", "2024-05-28")

    show_current_tasks()

    mark_task_completed("Позвонить маме")
    mark_task_completed("Выучить Python за ночь") # Такой задачи нет

    show_current_tasks()

    add_task("Погулять с собакой", "2024-05-28")
    mark_task_completed("Купить молоко")
    show_current_tasks()

    # --- Тестирование магазинов ---
    print("\n--- Сеть магазинов ---")

    # 1. Создание нескольких объектов класса Store
    store1 = Store("Продукты у дома", "ул. Ленина, 1")
    store2 = Store("Книжный мир", "пр. Мира, 15")
    store3 = Store("ТехноСила", "ул. Гагарина, 42")

    # Добавление товаров в магазины
    print("\n--- Добавление товаров ---")
    store1.add_item("Хлеб", 50.0)
    store1.add_item("Молоко", 70.5)
    store1.add_item("Яйца", 120.0)

    store2.add_item("Война и мир", 1500.0)
    store2.add_item("1984", 800.0)
    store2.add_item("Мастер и Маргарита", 1200.0)

    store3.add_item("Смартфон X", 25000.0)
    store3.add_item("Ноутбук Y", 60000.0)
    store3.add_item("Наушники Z", 5000.0)
    store3.add_item("Смартфон X", 26000.0) # Попытка добавить существующий

    print(f"\n{store1}")
    print(f"{store2}")
    print(f"{store3}")

    # 3. Тестирование методов одного из магазинов (например, store1)
    print(f"\n--- Тестирование методов магазина '{store1.name}' ---")

    # Добавление нового товара
    store1.add_item("Сыр", 250.75)

    # Обновление цены товара
    store1.update_price("Молоко", 75.0)
    store1.update_price("Кефир", 80.0) # Попытка обновить цену несуществующего товара

    # Запрос цены товара
    store1.get_price("Хлеб")
    store1.get_price("Сыр")
    store1.get_price("Колбаса") # Попытка получить цену несуществующего товара

    # Удаление товара
    store1.remove_item("Яйца")
    store1.remove_item("Масло") # Попытка удалить несуществующий товар

    # Проверка ассортимента после изменений
    print("\nАссортимент магазина '" + store1.name + "' после всех операций:")
    for item, price in store1.items.items():
        print(f"- {item}: {price}")

    print("\n--- Тестирование магазина '" + store3.name + "' ---")
    store3.get_price("Смартфон X")
    store3.update_price("Смартфон X", 24500.0)
    store3.get_price("Смартфон X")
    store3.remove_item("Наушники Z")
    print(store3.items)
