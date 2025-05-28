"""
Модуль для тестирования функциональности управления пользователями.
"""

import os
import sys
import unittest

# Добавляем родительскую директорию в путь для импорта модулей
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from user_management import Admin, User  # noqa: E402


class TestUser(unittest.TestCase):
    """Тесты для класса User."""

    def setUp(self) -> None:
        """Подготовка тестовых данных."""
        self.user_id = 1
        self.user_name = "Тестовый Пользователь"
        self.user = User(self.user_id, self.user_name)

    def test_user_creation(self) -> None:
        """Проверка создания пользователя."""
        self.assertEqual(self.user.user_id, self.user_id)
        self.assertEqual(self.user.name, self.user_name)
        self.assertEqual(self.user.access_level, 'user')
        expected = f"Пользователь {self.user_name} (ID: {self.user_id})"
        self.assertIn(expected, str(self.user))

    def test_name_setter(self) -> None:
        """Проверка изменения имени пользователя."""
        new_name = "Новое Имя"
        self.user.name = new_name
        self.assertEqual(self.user.name, new_name)

    def test_invalid_name_setter(self) -> None:
        """Проверка обработки недопустимых имен пользователя."""
        with self.assertRaises(ValueError):
            self.user.name = ""  # Пустое имя
        with self.assertRaises(ValueError):
            self.user.name = "   "  # Имя из пробелов
        with self.assertRaises(ValueError):
            self.user.name = 123  # Не строка

    def test_invalid_user_creation(self) -> None:
        """Проверка создания пользователя с недопустимыми параметрами."""
        with self.assertRaises(ValueError):
            User(0, "Нулевой ID")  # ID должен быть положительным
        with self.assertRaises(ValueError):
            User(-1, "Отрицательный ID")
        with self.assertRaises(ValueError):
            User(1, "")  # Пустое имя

    def test_repr(self) -> None:
        """Проверка строкового представления объекта."""
        self.assertEqual(
            repr(self.user),
            f"User(user_id={self.user_id}, name='{self.user_name}')"
        )


class TestAdmin(unittest.TestCase):
    """Тесты для класса Admin."""

    def setUp(self) -> None:
        """Подготовка тестовых данных."""
        self.admin_id = 1
        self.admin_name = "Администратор"
        self.admin = Admin(self.admin_id, self.admin_name)
        
        # Создаем тестовых пользователей
        self.user1 = User(2, "Пользователь 1")
        self.user2 = User(3, "Пользователь 2")

    def test_admin_creation(self) -> None:
        """Проверка создания администратора."""
        self.assertEqual(self.admin.user_id, self.admin_id)
        self.assertEqual(self.admin.name, self.admin_name)
        self.assertEqual(self.admin.access_level, 'admin')
        self.assertEqual(str(self.admin), f"Администратор {self.admin_name} (ID: {self.admin_id}), пользователей: 0")

    def test_add_user(self) -> None:
        """Проверка добавления пользователя."""
        # Добавляем пользователя
        self.assertTrue(self.admin.add_user(self.user1))
        self.assertIn(self.user1, self.admin.users)
        
        # Пытаемся добавить того же пользователя снова
        self.assertFalse(self.admin.add_user(self.user1))
        
        # Пытаемся добавить пользователя с тем же ID
        user_same_id = User(self.user1.user_id, "Другой пользователь")
        self.assertFalse(self.admin.add_user(user_same_id))
        
        # Пытаемся добавить самого администратора
        self.assertFalse(self.admin.add_user(self.admin))

    def test_remove_user(self) -> None:
        """Проверка удаления пользователя."""
        # Добавляем пользователя
        self.admin.add_user(self.user1)
        self.admin.add_user(self.user2)
        
        # Удаляем пользователя
        self.assertTrue(self.admin.remove_user(self.user1.user_id))
        self.assertNotIn(self.user1, self.admin.users)
        
        # Пытаемся удалить несуществующего пользователя
        self.assertFalse(self.admin.remove_user(999))
        
        # Пытаемся удалить с некорректным ID
        self.assertFalse(self.admin.remove_user("не число"))  # type: ignore

    def test_get_user(self) -> None:
        """Проверка поиска пользователя по ID."""
        # Добавляем пользователя
        self.admin.add_user(self.user1)
        
        # Ищем существующего пользователя
        found_user = self.admin.get_user(self.user1.user_id)
        self.assertEqual(found_user, self.user1)
        
        # Ищем несуществующего пользователя
        self.assertIsNone(self.admin.get_user(999))

    def test_list_users(self) -> None:
        """Проверка вывода списка пользователей."""
        # Проверяем пустой список
        self.assertEqual(len(self.admin.users), 0)
        
        # Добавляем пользователей и проверяем список
        self.admin.add_user(self.user1)
        self.admin.add_user(self.user2)
        
        self.assertEqual(len(self.admin.users), 2)
        self.assertIn(self.user1, self.admin.users)
        self.assertIn(self.user2, self.admin.users)

    def test_repr(self) -> None:
        """Проверка строкового представления объекта."""
        self.assertEqual(
            repr(self.admin),
            f"Admin(user_id={self.admin_id}, name='{self.admin_name}')"
        )


if __name__ == '__main__':
    unittest.main()
