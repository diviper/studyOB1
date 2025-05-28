"""
Основной модуль пакета user_management.

Содержит базовые классы и логику работы с пользователями.
"""

from .user import User
from .admin import Admin

__all__ = ['User', 'Admin']
