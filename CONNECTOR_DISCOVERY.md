# LearnUpon Connector — Discovery & Vendor API Specification

**Официальный сайт:** https://www.learnupon.com  
**Базовый эндпоинт API:** `https://<tenant>.learnupon.com/api/v1`  
**Схема авторизации:** Basic Auth (API Key : API Secret)

## Поддерживаемые сущности API
- пользователи (/users)
- курсы (/courses)
- зачисления (/enrollments)
- модули обучения
- группы пользователей

## Архитектурные требования
- Использование безопасного клиента с контролем таймаутов, повторных попыток (backoff) и обработкой rate limit.
- Валидация входных данных через Pydantic-схемы без утечки чувствительных полей в логи.
- Тестовая точка проверки подключения: `GET /api/v1/users`.
