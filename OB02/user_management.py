from __future__ import annotations
from typing import List, Optional

class User:
    """
    Класс для представления пользователя системы.
    Инкапсулирует данные пользователя: ID, имя и уровень доступа.
    
    Атрибуты:
        _user_id (int): Уникальный идентификатор пользователя
        _name (str): Имя пользователя
        _access_level (str): Уровень доступа пользователя (по умолчанию 'user')
    """
    
    def __init__(self, user_id: int, name: str) -> None:
        """
        Инициализация пользователя.
        
        Args:
            user_id: Уникальный идентификатор пользователя (положительное целое число)
            name: Имя пользователя (непустая строка)
            
        Raises:
            ValueError: Если user_id не является положительным числом
                     или имя пустое
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("ID пользователя должен быть положительным целым числом")
            
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Имя пользователя должно быть непустой строкой")
            
        self._user_id = user_id
        self._name = name.strip()
        self._access_level = 'user'
    
    @property
    def user_id(self) -> int:
        """int: Возвращает ID пользователя (только чтение)."""
        return self._user_id
    
    @property
    def name(self) -> str:
        """str: Возвращает имя пользователя."""
        return self._name
    
    @name.setter
    def name(self, new_name: str) -> None:
        """
        Устанавливает новое имя пользователя.
        
        Args:
            new_name: Новое имя пользователя
            
        Raises:
            ValueError: Если новое имя пустое или не является строкой
        """
        if not isinstance(new_name, str) or not new_name.strip():
            raise ValueError("Имя пользователя должно быть непустой строкой")
        self._name = new_name.strip()
    
    @property
    def access_level(self) -> str:
        """str: Возвращает уровень доступа пользователя (только чтение)."""
        return self._access_level
    
    def __str__(self) -> str:
        """
        Возвращает строковое представление пользователя.
        
        Returns:
            str: Строка с информацией о пользователе
        """
        return f"Пользователь ID: {self._user_id}, Имя: {self._name}, Уровень доступа: {self._access_level}"
    
    def __repr__(self) -> str:
        """
        Возвращает формальное строковое представление объекта.
        
        Returns:
            str: Формальное строковое представление
        """
        return f"{self.__class__.__name__}(user_id={self._user_id}, name='{self._name}')"


class Admin(User):
    """
    Класс администратора, наследуется от User.
    
    Имеет расширенные права доступа (уровень 'admin') и может управлять пользователями:
    добавлять новых пользователей, удалять существующих и просматривать список всех пользователей.
    
    Атрибуты:
        _users (List[User]): Список пользователей в системе
    """
    
    def __init__(self, user_id: int, name: str) -> None:
        """
        Инициализация администратора.
        
        Args:
            user_id: Уникальный идентификатор администратора (положительное целое число)
            name: Имя администратора (непустая строка)
        """
        super().__init__(user_id, name)
        self._access_level = 'admin'
        self._users: List[User] = []  # Список пользователей системы
    
    @property
    def users(self) -> List[User]:
        """
        Возвращает копию списка пользователей.
        
        Returns:
            List[User]: Копия списка пользователей
        """
        return self._users.copy()
    
    def add_user(self, user: User) -> bool:
        """
        Добавляет пользователя в систему.
        
        Args:
            user: Объект пользователя для добавления
            
        Returns:
            bool: True, если пользователь успешно добавлен, иначе False
            
        Raises:
            TypeError: Если переданный объект не является экземпляром класса User
        """
        if not isinstance(user, User):
            raise TypeError(f"Ожидается объект класса User, получен {type(user).__name__}")
        
        if user.user_id == self.user_id:
            print("Ошибка: Нельзя добавить самого себя как пользователя")
            return False
            
        if any(u.user_id == user.user_id for u in self._users):
            print(f"Ошибка: Пользователь с ID {user.user_id} уже существует")
            return False
        
        self._users.append(user)
        print(f"Пользователь {user.name} (ID: {user.user_id}) успешно добавлен")
        return True
    
    def remove_user(self, user_id: int) -> bool:
        """
        Удаляет пользователя из системы по ID.
        
        Args:
            user_id: ID пользователя для удаления
            
        Returns:
            bool: True, если пользователь успешно удален, иначе False
        """
        if not isinstance(user_id, int):
            print("Ошибка: ID пользователя должен быть целым числом")
            return False
            
        for i, user in enumerate(self._users):
            if user.user_id == user_id:
                removed_user = self._users.pop(i)
                print(f"Пользователь {removed_user.name} (ID: {user_id}) успешно удален")
                return True
        
        print(f"Ошибка: Пользователь с ID {user_id} не найден")
        return False
    
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Находит пользователя по ID.
        
        Args:
            user_id: ID искомого пользователя
            
        Returns:
            Optional[User]: Найденный пользователь или None, если не найден
        """
        return next((user for user in self._users if user.user_id == user_id), None)
    
    def list_users(self) -> None:
        """
        Выводит список всех пользователей в системе с их основными данными.
        
        Выводит количество пользователей и их список с порядковыми номерами.
        """
        if not self._users:
            print("В системе пока нет пользователей")
            return
        
        print("\nСписок пользователей (всего: {}):".format(len(self._users)))
        for i, user in enumerate(self._users, 1):
            print(f"{i}. {user}")
    
    def __str__(self) -> str:
        """
        Возвращает строковое представление администратора.
        
        Returns:
            str: Строка с информацией об администраторе
        """
        return f"Администратор ID: {self._user_id}, Имя: {self._name}, Уровень доступа: {self._access_level}"
    
    def __repr__(self) -> str:
        """
        Возвращает формальное строковое представление объекта.
        
        Returns:
            str: Формальное строковое представление
        """
        return f"{self.__class__.__name__}(user_id={self.user_id}, name='{self.name}')"
