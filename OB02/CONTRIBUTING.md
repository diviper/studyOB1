# 🚀 Вклад в проект

Спасибо за интерес к участию в проекте! Вот несколько руководств, которые помогут вам начать.

## 📋 Как внести вклад

1. **Сообщите об ошибке**
   - Проверьте, не была ли ошибка уже зарегистрирована в [Issues](https://github.com/yourusername/user-management-system/issues).
   - Если ошибка еще не зарегистрирована, создайте новую issue с четким описанием проблемы.

2. **Предложите улучшение**
   - Откройте issue с описанием предлагаемого улучшения.
   - Укажите, почему вы считаете это улучшение полезным.

3. **Внесите изменения в код**
   - Сделайте форк репозитория.
   - Создайте ветку для вашей функции (`git checkout -b feature/amazing-feature`).
   - Зафиксируйте изменения (`git commit -m 'Add some amazing feature'`).
   - Отправьте изменения в ваш форк (`git push origin feature/amazing-feature`).
   - Откройте Pull Request.

## 🛠️ Настройка окружения для разработки

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/user-management-system.git
   cd user-management-system
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установите зависимости для разработки:
   ```bash
   pip install -e ".[dev]"
   ```

4. Установите pre-commit хуки:
   ```bash
   pre-commit install
   ```

## 🧪 Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск тестов с покрытием
pytest --cov=user_management

# Запуск линтеров
flake8 user_management
yapf -r -i user_management/
```

## 📝 Стиль кода

- Используйте [PEP 8](https://www.python.org/dev/peps/pep-0008/) в качестве руководства по стилю.
- Используйте [Google Style Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) для документации.
- Все новые функции должны быть покрыты тестами.
- Код должен проходить все проверки линтеров.

## 🔄 Pull Request Process

1. Убедитесь, что все тесты проходят.
2. Обновите документацию, если это необходимо.
3. Убедитесь, что ваш код соответствует стилю.
4. Опишите изменения в PR.
5. Убедитесь, что CI проходит успешно.

## 📜 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для дополнительной информации.

---

Спасибо за ваш вклад! 🙌
