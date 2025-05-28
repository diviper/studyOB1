# Менеджер задач и магазинов

Проект представляет собой набор классов для управления задачами и магазинами на языке Python.

## 🚀 Возможности

### 📋 Управление задачами
- Создание, редактирование и удаление задач
- Отметка задач как выполненных
- Просмотр текущих и выполненных задач
- Фильтрация задач по статусу

### 🏪 Управление магазинами
- Создание и настройка магазинов
- Управление ассортиментом товаров
- Работа с категориями товаров
- Обновление цен и информации о товарах

## 📦 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/diviper/studyOB1.git
   cd studyOB1
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Быстрый старт

### Запуск демонстрации
```bash
python -m task_manager_store.main
```

### Пример использования

```python
from task_manager_store.task import TaskManager
from task_manager_store.store import Store
from datetime import datetime, timedelta

# Работа с задачами
task_manager = TaskManager()
task_manager.add_task("Купить молоко", (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
task_manager.mark_task_completed("Купить молоко")

# Работа с магазином
store = Store("Продуктовый", "ул. Ленина, 1")
store.add_item("Яблоки", 150.0, "Фрукты")
store.update_price("Яблоки", 180.0)
```

## 📁 Структура проекта

```
studyOB1/
├── task_manager_store/     # Основной пакет
│   ├── __init__.py
│   ├── task.py           # Классы для работы с задачами
│   ├── store.py          # Классы для работы с магазинами
│   └── main.py           # Демонстрационный скрипт
├── .gitignore           # Игнорируемые файлы
├── README.md            # Этот файл
├── requirements.txt     # Зависимости
└── setup.py            # Установочный файл
```

## 📝 Требования
- Python 3.7+
- Зависимости из requirements.txt

## 🤝 Вклад
1. Форкните репозиторий
2. Создайте ветку с новой функцией (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия
Распространяется по лицензии MIT. См. файл `LICENSE` для получения дополнительной информации.

## 📬 Контакты
Ваше имя - [@ваш_твиттер](https://twitter.com/ваш_твиттер) - ваш.email@example.com

Ссылка на проект: [https://github.com/diviper/studyOB1](https://github.com/diviper/studyOB1)
