"""
Тестовый скрипт для проверки функциональности user_management.
"""

from user_management import User, Admin, UserRole, UserProfile
from datetime import datetime

def main():
    print("=== Тестирование системы управления пользователями ===\n")
    
    # Создаем администратора
    admin = Admin(
        user_id=1,
        name="Алексей Админов",
        email="admin@example.com"
    )
    admin.set_password("admin123")
    
    print(f"Создан администратор: {admin}")
    print(f"Email: {admin.email}")
    print(f"Уровень доступа: {admin.access_level}")
    print(f"Роли: {[r.name for r in admin.roles]}")
    
    # Создаем пользователя
    user = User(
        user_id=2,
        name="Иван Иванов",
        email="ivan@example.com"
    )
    user.set_password("user123")
    
    print(f"\nСоздан пользователь: {user}")
    print(f"Проверка пароля 'user123': {user.check_password('user123')}")
    print(f"Проверка неверного пароля: {user.check_password('wrong')}")
    
    # Добавляем пользователя через администратора
    if admin.add_user(user):
        print("\nПользователь успешно добавлен в систему")
    
    # Создаем и назначаем роль
    editor_role = UserRole(
        name="editor",
        permissions=["create_post", "edit_post", "delete_post"],
        description="Редактор контента"
    )
    
    admin.update_user_role(user.user_id, editor_role)
    print(f"\nНазначена роль: {editor_role.name}")
    print(f"Разрешения: {editor_role.permissions}")
    
    # Проверяем разрешения
    print("\nПроверка разрешений пользователя:")
    print(f"Может создавать посты: {user.has_permission('create_post')}")
    print(f"Может управлять пользователями: {user.has_permission('manage_users')}")
    
    # Обновляем профиль
    user.update_profile(
        phone="+79123456789",
        address="ул. Примерная, д. 123",
        is_active=True
    )
    
    print("\nОбновленный профиль:")
    print(f"Телефон: {user.profile.phone}")
    print(f"Адрес: {user.profile.address}")
    print(f"Активен: {user.profile.is_active}")
    
    # Выводим список пользователей
    print("\nСписок пользователей в системе:")
    for u in admin.users:
        print(f"- {u.name} (ID: {u.user_id}, Роли: {[r.name for r in u.roles]})")
    
    # Тестируем поиск пользователей
    print("\nПоиск пользователей по email 'example.com':")
    found_users = admin.search_users(email__contains="example.com")
    for u in found_users:
        print(f"Найден: {u.name} ({u.email})")

if __name__ == "__main__":
    main()
