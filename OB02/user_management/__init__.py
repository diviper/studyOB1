"""
Пакет user_management предоставляет функциональность для управления пользователями.

Основные компоненты:
- core: Основная логика приложения
- models: Модели данных
- utils: Вспомогательные утилиты

Пример использования:
    >>> from user_management import User, Admin, UserRole
    >>> admin = Admin(1, "Администратор", "admin@example.com")
    >>> user = User(2, "Пользователь", "user@example.com")
    >>> admin.add_user(user)
    True
"""

__version__ = '0.1.0'
__author__ = 'Чурэн Дмитрий Сергеевич'
__email__ = 'churendmitriy@gmail.com'
__license__ = 'MIT'

# Импорты из core
from .core.user import User
from .core.admin import Admin

# Импорты из models
from .models import UserProfile, UserRole

# Импорты из utils
from .utils import (
    validate_email,
    validate_phone,
    hash_password,
    verify_password,
    generate_jwt_token,
    verify_jwt_token,
    logger
)

# Экспортируемые имена
__all__ = [
    # Основные классы
    'User',
    'Admin',
    'UserProfile',
    'UserRole',
    
    # Утилиты
    'validate_email',
    'validate_phone',
    'hash_password',
    'verify_password',
    'generate_jwt_token',
    'verify_jwt_token',
    'logger',
]

# Настройка корневого логгера
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

try:
    from ._version import version as __version__  # noqa
    from ._version import version_tuple  # noqa
except ImportError:
    pass
