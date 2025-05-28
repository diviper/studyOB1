"""
Модуль с классом администратора.

Содержит класс Admin, который расширяет базовый класс User
дополнительными правами и возможностями управления пользователями.
"""

from dataclasses import field
from typing import List, Optional, Dict, Any, Set
from datetime import datetime
import logging

from .user import User
from ..models import UserRole
from ..utils import log_activity, logger


class Admin(User):
    """Класс, представляющий администратора системы.
    
    Наследует все атрибуты и методы класса User и добавляет
    функциональность управления пользователями.
    """
    
    def __init__(self, user_id: int, name: str, email: Optional[str] = None, 
                 password: Optional[str] = None) -> None:
        """Инициализирует администратора.
        
        Args:
            user_id: Уникальный идентификатор администратора
            name: Имя администратора
            email: Электронная почта (опционально)
            password: Пароль (опционально)
        """
        super().__init__(user_id=user_id, name=name, email=email, access_level='admin')
        if password:
            self.set_password(password)
        
        # Добавляем администратору роль по умолчанию
        admin_role = UserRole(
            name='admin',
            permissions=['manage_users', 'manage_roles', 'view_reports'],
            description='Полный доступ к системе'
        )
        self.add_role(admin_role)
        
        self._users: Dict[int, User] = {}
        log_activity(user_id, "Администратор инициализирован")
    
    @property
    def users(self) -> List[User]:
        """Возвращает список всех пользователей."""
        return list(self._users.values())
    
    def add_user(self, user: User) -> bool:
        """Добавляет пользователя в систему.
        
        Args:
            user: Объект пользователя для добавления
            
        Returns:
            bool: True если пользователь добавлен, иначе False
        """
        if not isinstance(user, User):
            logger.error("Можно добавлять только объекты класса User")
            return False
            
        if user.user_id == self.user_id:
            logger.error("Нельзя добавить самого себя как пользователя")
            return False
            
        if user.user_id in self._users:
            logger.warning(f"Пользователь с ID {user.user_id} уже существует")
            return False
            
        self._users[user.user_id] = user
        log_activity(self.user_id, f"Добавлен пользователь {user.user_id}")
        return True
    
    def remove_user(self, user_id: int) -> bool:
        """Удаляет пользователя из системы.
        
        Args:
            user_id: ID пользователя для удаления
            
        Returns:
            bool: True если пользователь удален, иначе False
        """
        if not isinstance(user_id, int) or user_id <= 0:
            logger.error("ID пользователя должен быть положительным целым числом")
            return False
            
        if user_id not in self._users:
            logger.warning(f"Пользователь с ID {user_id} не найден")
            return False
            
        user = self._users.pop(user_id)
        log_activity(self.user_id, f"Удален пользователь {user_id}: {user.name}")
        return True
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Возвращает пользователя по ID.
        
        Args:
            user_id: ID искомого пользователя
            
        Returns:
            Optional[User]: Найденный пользователь или None
        """
        if not isinstance(user_id, int) or user_id <= 0:
            logger.error("ID пользователя должен быть положительным целым числом")
            return None
            
        return self._users.get(user_id)
    
    def list_users(self) -> List[Dict[str, Any]]:
        """Возвращает список всех пользователей в виде словарей.
        
        Returns:
            List[Dict[str, Any]]: Список словарей с данными пользователей
        """
        return [user.to_dict() for user in self._users.values()]
    
    def search_users(self, **criteria: Any) -> List[User]:
        """Ищет пользователей по заданным критериям.
        
        Args:
            **criteria: Критерии поиска (атрибуты пользователя)
            
        Returns:
            List[User]: Список найденных пользователей
        """
        if not criteria:
            return []
            
        result = []
        for user in self._users.values():
            match = True
            for key, value in criteria.items():
                if hasattr(user, key):
                    if getattr(user, key) != value:
                        match = False
                        break
                elif hasattr(user.profile, key):
                    if getattr(user.profile, key) != value:
                        match = False
                        break
                else:
                    match = False
                    break
                    
            if match:
                result.append(user)
                
        return result
    
    def update_user_role(self, user_id: int, role: UserRole) -> bool:
        """Обновляет роль пользователя.
        
        Args:
            user_id: ID пользователя
            role: Новая роль
            
        Returns:
            bool: True если роль обновлена, иначе False
        """
        user = self.get_user(user_id)
        if not user:
            return False
            
        # Удаляем существующую роль с таким же именем, если есть
        user.roles = [r for r in user.roles if r.name != role.name]
        user.add_role(role)
        user.updated_at = datetime.utcnow()
        
        log_activity(
            self.user_id, 
            f"Обновлена роль пользователя {user_id}",
            {"role": role.name, "permissions": role.permissions}
        )
        return True
    
    def __str__(self) -> str:
        """Возвращает строковое представление администратора."""
        return f"Администратор {self.name} (ID: {self.user_id}), пользователей: {len(self._users)}"
    
    def __repr__(self) -> str:
        """Возвращает формальное строковое представление объекта."""
        return f"Admin(user_id={self.user_id}, name='{self.name}')"
