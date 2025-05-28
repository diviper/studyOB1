"""
Пакет для управления пользователями с различными уровнями доступа.

Этот пакет предоставляет функциональность для работы с пользователями,
включая аутентификацию, авторизацию и управление правами доступа.
"""

from user_management.core import User, Admin
from user_management.models import UserProfile, UserRole

__version__ = '0.1.0'
__all__ = ['User', 'Admin', 'UserProfile', 'UserRole']
