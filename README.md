# Twitter clone project
Проект для Skillbox

---

[application](http://158.160.29.218/)

[docs](http://158.160.29.218/docs)

---

[repository](https://gitlab.skillbox.ru/telitsin_andrei/python_advanced_diploma)

[kanban доска](https://miro.com/app/board/uXjVNfT-t9o=/)

[API schema](https://miro.com/app/board/uXjVNfNic6Y=/)

[database schema](https://miro.com/app/board/uXjVNfPptqU=/)

[app schema](https://miro.com/app/board/uXjVNfJlORE=/)

---

## migrations
Для dev миграции:
1. В .env поставить FASTAPI_DEBUG=True
2. Запустить docker compose
3. Запустить python poetry environment
4. Из корня проекта запустить команду alembic:
   * alembic upgrade head


Для prod миграции:
1. В .env поставить FASTAPI_DEBUG=False
2. Запустить docker compose
3. Выполнить команду в контейнере fastaAPI:
   * sudo docker exec fast_api alembic upgrade head

## testing
1. В .env поставить FASTAPI_DEBUG=False, TESTING=True
2. Запустить docker compose
3. Запустить python poetry environment
4. Запустить команду из корня проекта: pytest tests/

---

## technologies
### FastAPI
> Асинхронный python фреймворк для создания RESTful APIs

### Yandex computer cloud
> Облачный сервис. Используется виртуальная машина.
 
### Yandex object storage
> Хранилище файлов, используется для хранения загружаемых фотографий.

### NGINX
> Веб сервер, используется для проксирования запросов и для отдачи статики.

### Postgres
> Реляционная база данных, в проекте используется через SQLAlchemy

### PGAdmin
> Админ панель для Postgres
> 
> [PGAdmin](http://158.160.29.218:2345/)

### Redis
> Key-value база данных. 
> В проекте используется для celery и кэширования запросов на сервер 

### Celery
> Распределенная очередь заданий. 
> В приложении используется для обработки загружаемых изображений, 
> загрузки их в yandex cloud object storage и 
> обновления ссылки на изображение в базе данных.

### Flower
> Веб приложение для мониторинга задач celery
> 
> [web app](http://158.160.29.218:5555/)

### Prometheus
> Приложение для сбора метрик. 
> В приложении используется библиотека - prometheus-fastapi-instrumentator

### Grafana
> Веб приложение для визуализации метрик.
> 
> [web app](http://158.160.29.218:3000/)

### Sentry
> Приложение для мониторинга производительности приложений и отслеживание ошибок. 
> Не развернуто локально!!!
