"""
Модуль конфигурации приложения.

Содержит настройки приложения, загружаемые из переменных окружения.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    """Класс для хранения настроек приложения."""
    
    # Основные настройки
    APP_ENV: str = os.getenv('APP_ENV', 'development')
    APP_SECRET_KEY: str = os.getenv('APP_SECRET_KEY', 'dev-secret-key')
    APP_DEBUG: bool = os.getenv('APP_DEBUG', 'False').lower() == 'true'
    
    # Настройки базы данных
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '5432'))
    DB_NAME: str = os.getenv('DB_NAME', 'user_management')
    DB_USER: str = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'postgres')
    
    # Настройки JWT
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = int(
        os.getenv('JWT_REFRESH_TOKEN_EXPIRE_DAYS', '7'))
    
    # Настройки логирования
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = os.getenv('LOG_FORMAT', 'json')
    
    # Настройки почты (опционально)
    SMTP_SERVER: Optional[str] = os.getenv('SMTP_SERVER')
    SMTP_PORT: Optional[int] = int(os.getenv('SMTP_PORT', '587')) \
        if os.getenv('SMTP_PORT') else None
    SMTP_USERNAME: Optional[str] = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD: Optional[str] = os.getenv('SMTP_PASSWORD')
    DEFAULT_FROM_EMAIL: Optional[str] = os.getenv('DEFAULT_FROM_EMAIL')
    
    @property
    def DATABASE_URL(self) -> str:
        """Возвращает URL для подключения к базе данных."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def TEST_DATABASE_URL(self) -> str:
        """Возвращает URL для подключения к тестовой базе данных."""
        return f"{self.DATABASE_URL}_test"
    
    def to_dict(self) -> Dict[str, Any]:
        """Возвращает настройки в виде словаря."""
        # Исключаем приватные атрибуты и методы
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_') and not callable(getattr(self, key))
        }


# Создаем экземпляр настроек
settings = Settings()

# Выводим настройки при запуске
if __name__ == "__main__":
    import json
    print(json.dumps(settings.to_dict(), indent=2, ensure_ascii=False))
