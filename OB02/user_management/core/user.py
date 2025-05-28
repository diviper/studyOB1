"""
Модуль с базовым классом пользователя.

Содержит класс User, который представляет базовую сущность пользователя в системе.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
import hashlib
import uuid

from ..models import UserProfile, UserRole
from ..utils import log_activity, validate_email, validate_phone


@dataclass
class User:
    """Класс, представляющий пользователя системы.
    
    Атрибуты:
        user_id: Уникальный идентификатор пользователя
        name: Имя пользователя
        email: Электронная почта (опционально)
        password_hash: Хеш пароля (опционально)
        access_level: Уровень доступа (по умолчанию 'user')
        profile: Дополнительная информация о пользователе
        roles: Список ролей пользователя
        created_at: Дата и время создания пользователя
        updated_at: Дата и время последнего обновления
    """
    
    user_id: int
    name: str
    email: Optional[str] = None
    password_hash: Optional[str] = None
    access_level: str = 'user'
    profile: UserProfile = field(default_factory=UserProfile)
    roles: List[UserRole] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self) -> None:
        """Выполняет валидацию после инициализации."""
        self._validate_name(self.name)
        self._validate()
        log_activity(self.user_id, "Пользователь создан")
    
    def _validate_name(self, name: str) -> None:
        """Проверяет валидность имени пользователя."""
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Имя пользователя должно быть непустой строкой")
    
    def _validate(self) -> None:
        """Проверяет валидность данных пользователя."""
        if not isinstance(self.user_id, int) or self.user_id <= 0:
            raise ValueError("ID пользователя должен быть положительным целым числом")
            
        # Проверка email, если он указан
        if self.email and not validate_email(self.email):
            raise ValueError("Некорректный формат email")
    
    @property
    def name(self) -> str:
        """Возвращает имя пользователя."""
        return self.__dict__['name']
        
    @name.setter
    def name(self, value: str) -> None:
        """Устанавливает имя пользователя с валидацией.
        
        Args:
            value: Новое имя пользователя
            
        Raises:
            ValueError: Если имя пустое или не является строкой
        """
        self._validate_name(value)
        self.__dict__['name'] = value.strip()
        self.updated_at = datetime.utcnow()
    
    def set_password(self, password: str) -> None:
        """Устанавливает хеш пароля.
        
        Args:
            password: Пароль для хеширования
        """
        if not password or not isinstance(password, str) or len(password) < 6:
            raise ValueError("Пароль должен быть строкой не менее 6 символов")
            
        salt = uuid.uuid4().hex
        self.password_hash = hashlib.sha256(
            (password + salt).encode('utf-8')
        ).hexdigest()
        self.updated_at = datetime.utcnow()
        log_activity(self.user_id, "Пароль обновлен")
    
    def check_password(self, password: str) -> bool:
        """Проверяет соответствие пароля.
        
        Args:
            password: Пароль для проверки
            
        Returns:
            bool: True если пароль верный, иначе False
        """
        if not self.password_hash:
            return False
            
        salt = self.password_hash[:32]  # Соль хранится в начале хеша
        return self.password_hash == hashlib.sha256(
            (password + salt).encode('utf-8')
        ).hexdigest()
    
    def update_profile(self, **kwargs: Any) -> None:
        """Обновляет профиль пользователя.
        
        Args:
            **kwargs: Атрибуты для обновления
        """
        for key, value in kwargs.items():
            if hasattr(self.profile, key):
                setattr(self.profile, key, value)
            
        self.updated_at = datetime.utcnow()
        log_activity(self.user_id, "Профиль обновлен", kwargs)
    
    def add_role(self, role: UserRole) -> None:
        """Добавляет роль пользователю.
        
        Args:
            role: Роль для добавления
        """
        if not any(r.name == role.name for r in self.roles):
            self.roles.append(role)
            self.updated_at = datetime.utcnow()
            log_activity(self.user_id, f"Добавлена роль: {role.name}")
    
    def has_permission(self, permission: str) -> bool:
        """Проверяет наличие разрешения у пользователя.
        
        Args:
            permission: Проверяемое разрешение
            
        Returns:
            bool: True если разрешение есть, иначе False
        """
        return any(permission in role.permissions for role in self.roles)
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертирует объект пользователя в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с данными пользователя
        """
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'access_level': self.access_level,
            'profile': self.profile.__dict__,
            'roles': [role.__dict__ for role in self.roles],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self) -> str:
        """Возвращает строковое представление пользователя."""
        return f"Пользователь {self.name} (ID: {self.user_id})"
    
    def __repr__(self) -> str:
        """Возвращает формальное строковое представление объекта."""
        return f"User(user_id={self.user_id}, name='{self.name}')"
