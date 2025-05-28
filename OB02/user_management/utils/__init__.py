"""
Вспомогательные утилиты для работы с пользователями.

Содержит вспомогательные функции для валидации, логирования и других задач.
"""

import re
import logging
import hashlib
import hmac
import os
import json
from typing import Any, Optional, TypeVar, Type, Dict, Union, List
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секретный ключ для JWT (в продакшене должен быть в .env)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

T = TypeVar('T')

def validate_email(email: str) -> bool:
    """Проверяет корректность email-адреса.
    
    Args:
        email: Email-адрес для проверки
        
    Returns:
        bool: True если email корректен, иначе False
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Проверяет корректность номера телефона.
    
    Поддерживает форматы:
    - +7 XXX XXX-XX-XX
    - 8 XXX XXX-XX-XX
    - XXX-XX-XX
    
    Args:
        phone: Номер телефона для проверки
        
    Returns:
        bool: True если номер корректен, иначе False
    """
    pattern = r'^(\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$|^\d{3}-\d{2}-\d{2}$'
    return bool(re.match(pattern, phone))


def log_activity(user_id: int, action: str, details: Optional[dict] = None) -> None:
    """Логирует действия пользователя.
    
    Args:
        user_id: ID пользователя
        action: Описание действия
        details: Дополнительные детали (опционально)
    """
    log_message = f"User {user_id}: {action}"
    if details:
        log_message += f" | Details: {details}"
    logger.info(log_message)


def parse_datetime(dt_str: str, dt_format: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """Парсит строку с датой и временем в объект datetime.
    
    Args:
        dt_str: Строка с датой и временем
        dt_format: Формат даты (по умолчанию: "%Y-%m-%d %H:%M:%S")
        
    Returns:
        Optional[datetime]: Объект datetime или None в случае ошибки
    """
    try:
        return datetime.strptime(dt_str, dt_format)
    except (ValueError, TypeError):
        logger.warning(f"Не удалось распознать дату: {dt_str}")
        return None


def to_dict(obj: Any, exclude: Optional[list] = None) -> dict:
    """Конвертирует объект в словарь.
    
    Args:
        obj: Объект для конвертации
        exclude: Список атрибутов для исключения
        
    Returns:
        dict: Словарь с атрибутами объекта
    """
    if exclude is None:
        exclude = []
        
    if hasattr(obj, '__dict__'):
        return {
            k: v for k, v in obj.__dict__.items()
            if not k.startswith('_') and k not in exclude
        }
    return {}


def hash_password(password: str) -> str:
    """Хеширует пароль с использованием bcrypt.
    
    Args:
        password: Пароль в открытом виде
        
    Returns:
        str: Хешированный пароль
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля его хешу.
    
    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хешированный пароль
        
    Returns:
        bool: True если пароль верный, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_jwt_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Генерирует JWT токен.
    
    Args:
        data: Данные для кодирования в токен
        expires_delta: Время жизни токена
        
    Returns:
        str: Сгенерированный JWT токен
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """Проверяет и декодирует JWT токен.
    
    Args:
        token: JWT токен для проверки
        
    Returns:
        Optional[Dict[str, Any]]: Декодированные данные токена или None при ошибке
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        logger.error("Ошибка при проверке токена", exc_info=True)
        return None


__all__ = [
    'validate_email',
    'validate_phone',
    'log_activity',
    'parse_datetime',
    'to_dict',
    'logger'
]
