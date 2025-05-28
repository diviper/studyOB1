#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Демонстрация работы системы управления пользователями.

Этот скрипт демонстрирует основные возможности классов User и Admin,
включая создание, добавление, удаление и изменение пользователей.
"""

import sys
import io
from typing import NoReturn

# Настройка вывода для корректного отображения кириллицы
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from user_management import User, Admin


def print_header(title: str) -> None:
    """Печатает заголовок с рамкой.
    
    Args:
        title: Текст заголовка
    """
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)


def demo_user_creation() -> tuple[Admin, list[User]]:
    """Демонстрирует создание пользователей и администратора.
    
    Returns:
        tuple: Кортеж из объекта администратора и списка пользователей
    """
    print_header("СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ")
    
    # Создаем администратора
    try:
        admin = Admin(1, "Алексей Админов")
        print(f"Создан администратор: {admin}")
    except ValueError as e:
        print(f"Ошибка при создании администратора: {e}")
        raise
    
    # Создаем обычных пользователей
    users = []
    user_data = [
        (2, "Иван Иванов"),
        (3, "Мария Петрова"),
        (4, "Сергей Сидоров")
    ]
    
    for uid, name in user_data:
        try:
            user = User(uid, name)
            users.append(user)
            print(f"Создан пользователь: {user}")
        except ValueError as e:
            print(f"Ошибка при создании пользователя {name}: {e}")
    
    return admin, users


def demo_user_management(admin: Admin, users: list[User]) -> None:
    """Демонстрирует управление пользователями.
    
    Args:
        admin: Объект администратора
        users: Список пользователей для добавления
    """
    print_header("УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ")
    
    # Добавляем пользователей в систему
    print("\nДобавление пользователей:")
    for user in users:
        admin.add_user(user)
    
    # Пытаемся добавить пользователя с существующим ID
    print("\nПопытка добавить пользователя с существующим ID:")
    admin.add_user(User(2, "Дубликат Иванова"))
    
    # Пытаемся добавить самого администратора как пользователя
    print("\nПопытка добавить самого администратора как пользователя:")
    admin.add_user(admin)
    
    # Выводим список пользователей
    print("\nТекущий список пользователей:")
    admin.list_users()
    
    # Ищем пользователя по ID
    print("\nПоиск пользователя по ID:")
    user = admin.get_user(3)
    if user:
        print(f"Найден пользователь: {user}")
    else:
        print("Пользователь не найден")
    
    # Удаляем пользователя
    print("\nУдаление пользователя:")
    admin.remove_user(2)  # Удаляем Ивана Иванова
    
    # Пытаемся удалить несуществующего пользователя
    print("\nПопытка удалить несуществующего пользователя:")
    admin.remove_user(999)
    
    # Пытаемся удалить с некорректным ID
    print("\nПопытка удалить пользователя с некорректным ID:")
    admin.remove_user("не число")  # type: ignore
    
    # Выводим обновленный список пользователей
    print("\nОбновленный список пользователей:")
    admin.list_users()


def demo_user_modification() -> None:
    """Демонстрирует изменение данных пользователя."""
    print_header("ИЗМЕНЕНИЕ ДАННЫХ ПОЛЬЗОВАТЕЛЯ")
    
    # Создаем пользователя
    try:
        user = User(10, "Анна Смирнова")
        print(f"Создан пользователь: {user}")
        
        # Изменяем имя пользователя
        print("\nИзменение имени пользователя:")
        print(f"Имя до изменения: {user.name}")
        user.name = "Анна Новикова"
        print(f"Имя после изменения: {user.name}")
        
        # Пытаемся установить некорректное имя
        print("\nПопытка установить пустое имя:")
        try:
            user.name = ""
        except ValueError as e:
            print(f"Ошибка: {e}")
            
        # Показываем, что имя не изменилось
        print(f"Текущее имя: {user.name}")
        
    except ValueError as e:
        print(f"Ошибка при работе с пользователем: {e}")


def main() -> None:
    """Основная функция для демонстрации работы системы."""
    try:
        # Демонстрация создания пользователей
        admin, users = demo_user_creation()
        
        # Демонстрация управления пользователями
        demo_user_management(admin, users)
        
        # Демонстрация изменения данных пользователя
        demo_user_modification()
        
        print("\n" + "=" * 60)
        print("Демонстрация завершена успешно!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
