# drf-nuxt-library

[![Django Tests](https://github.com/hazadus/drf-nuxt-library/actions/workflows/django_tests.yml/badge.svg)](https://github.com/hazadus/drf-nuxt-library/actions/workflows/django_tests.yml)

Приложение для ведения учета книг в домашней библиотеке, разработано по заказу жены.

Проект работает по адресу: http://library.hazadus.ru/.

Перечень реализованных возможностей: [wiki on GitHub](https://github.com/hazadus/drf-nuxt-library/wiki/Что-реализовано-на-сайте).

Подробный список последних изменений: [changelog.md](https://github.com/hazadus/drf-nuxt-library/blob/main/changelog.md).

Что сейчас в работе: [project on GitHub](https://github.com/users/hazadus/projects/5).

Все планы: [issues on GitHub](https://github.com/hazadus/drf-nuxt-library/issues).

### Использованные библиотеки

- Backend: **Django**
  - `django-rest-framework`
  - `djoser`
  - `django-debug-toolbar`
  - `django-imagekit`
- Frontend: **Nuxt 3**
  - `@vueuse/nuxt`
  - `nuxt-icon`
  - `@pinia/nuxt`
  - `@nuxt/content`

### Запуск проекта в режиме разработки

Создаём `docker-compose.yml`, используя шаблон `docker-compose.dev.yml`.

В нём устанавливаем переменные окружения:

| Переменная | Значение                                                                                                                                                                                                                          |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SECRET_KEY | Стандартный секретный ключ Django.                                                                                                                                                                                                |
| DEBUG      | `True` для режима разработки.                                                                                                                                                                                                     |
| FRONTEND_URL | На каком адресе будет работать фронтенд.<br/> Для использования фронтенда из контейнера Node, прописываем `http://localhost`.<br/> Для использования фронтенда, запущенного `npm run dev`, устанавливаем `http://localhost:3000`. |
| NUXT_PUBLIC_API_BASE | При работе API из контейнера, оставляем `http://localhost`.<br/> Эта переменная используется в модуле `useApi.ts` фронтенда для построения URL API.                                                                               |

### Запуск тестов

```bash
cd backend
make upd
make test
```

### Интересные материалы, использованные при разработке

- [GitHub Actions in action - Setting up Django and Postgres](https://www.hacksoft.io/blog/github-actions-in-action-setting-up-django-and-postgres)
- [Loading Django Fixtures in Tests](https://realpython.com/django-pytest-fixtures/#loading-django-fixtures-in-tests)