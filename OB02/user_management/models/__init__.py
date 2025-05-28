"""
Модуль с моделями данных для системы управления пользователями.

Содержит модели данных, используемые в приложении.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class UserProfile:
    """Дополнительная информация о пользователе."""
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    is_active: bool = True


@dataclass
class UserRole:
    """Роль пользователя в системе."""
    name: str
    permissions: list[str] = field(default_factory=list)
    description: str = ""


__all__ = ['UserProfile', 'UserRole']
