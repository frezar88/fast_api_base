# FastApi

-  __`pip install fastapi[all] gunicorn`__ -- установка фаст апи с всеми зависимостями
  - __uvicorn app.main:app --reload__ -- запуск приложения в дев режиме

---

# Postgresql

- https://www.youtube.com/watch?v=kWUW3sMK0Mk&ab_channel=PythonToday -- установка 
- https://www.pgadmin.org/ -- Установка PgAdmin
- __`pip install asyncpg`__ --установка асинхронного драйвера постгрес
- __f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"__ -- пример урла асинхронного подключения к БД

---

# Alembic

- __alembic init migrations__ -- инициализация алембика
- __alembic.ini__ -- добавить метадату и модели
- __env.py__ -- если выносим alembic.ini выносим на уровень выше добавить <br/>  __sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))__
- __env.py__ -- добавляем настройку подключения к базе данных, расширяем настройки  <br/>  __config.set_main_option('sqlalchemy.url', f"{DATABASE_URL}?async_fallback=True")__
- __alembic revision --autogenerate -m "init project"__ -- создать первые миграции. Делать из корня проекта а не приложения
- __alembic upgrade head__ -- применить миграции. Вместо HEAD можно подставить номер миграции
- __alembic downgrade -1__ -- откатиться на 1 миграцию назад

---

# Redis
- __https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04-ru__ -- Инструкция по установке Redis для Linux
- - https://github.com/long2ice/fastapi-cache -- страница либы для работы с кешом в фас апи
- __`pip install "fastapi-cache2[redis]"`__-- установка
- в main.py подключить либу 
- -<br/> __from fastapi_cache.backends.redis import RedisBackend__ <br/><br/> __@app.on_event("startup")__<br/> __async def startup():__<br/>  &nbsp; &nbsp; &nbsp; &nbsp;  __redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")__ <br/>  &nbsp; &nbsp; &nbsp; &nbsp; __FastAPICache.init(RedisBackend(redis), prefix="cache")__
- __@cache(expire=60)__ -- Декоратор над ендпоинтом который нужно закешировать

---

# Celery

- __`pip install celery`__ --  установка селери и флавер
- создать файл с похожим содержанием <br/> __from celery import Celery__ <br/>  __celery = Celery(__ <br/> &nbsp; &nbsp; &nbsp; &nbsp;    __"tasks",__<br/> &nbsp; &nbsp; &nbsp; &nbsp;    __broker="redis://localhost:6379",__<br/> &nbsp; &nbsp; &nbsp; &nbsp;
    __include=["app.tasks.tasks"]__<br/>
    __)__
-  __celery -A app.tasks.celery:celery worker --loglevel=INFO --pool=solo__ -- Запуск задач селери
-  селери работает только с примитивными типами данных, по этому что бы закинуть что то из модели нужно сделать из этого словарь пример:<br/> __booking_dict = parse_obj_as(SBookings, booking).dict()__

---

# Flower

- __`pip install flower`__ --  установка Flower
- __celery -A app.tasks.celery:celery flower__ -- запуск flower

---

# Админка

- __`pip install sqladmin`__ -- установка админки
- __https://pypi.org/project/sqladmin/__ -- HomePage Admin

---
# Тесты

### PyTest

- __`pip install pytest pytest-asyncio`__-- установка pytest
- __pytest.ini__ -- создать в корне проекта 
- - содержимое файла: <br/> __[pytest]__ <br/> __pythonpath = . app__ <br/> __asyncio_mode = auto__
- __conftest.py__ --  создать внутри приложения рядом с main.py
- - содержимое файла: <br/> __import os__ <br/> __os.environ["MODE"] = "TEST"__
- в файле подключения к базе данных важно настроить режим приложения и передать в engine параметр <br/> __DATABASE_PARAMS = {"poolclass": NullPool}__ (Только для тестовой базы) 
- внутри приложения создать папку __tests__
- в папке __tests__ создать новый файл __conftest.py__ -- это точка входа всех тестов
- при асинхронном подключении важно в точке входа добавить эту функцию <br/>  
- - __@pytest.fixture(scope="session")__<br/>  __def event_loop(request):__<br/>   __loop = asyncio.get_event_loop_policy().new_event_loop()__<br/> __yield loop__<br/>  __loop.close()__ 
- __pytest -v__ -- запуск всех тестов из корня (если нужно видеть принты в тестах, добавить флаг -s)
- __pytest -v app/tests/unit_tests/users_test/test_service.py__ -- запуск конкретных тестов)
- ### Запуск фукнций теста с параметрами:
- - __@pytest.mark.parametrize("email,password,status_code", [
    ("kot@pes.com", "testPass", 200),
    ("kot@pes.com", "2121", 409),
])__
### HTTPX 

- __`pip install httpx`__ -- установка (тестирование запросов без поднятия сервера)
- __from fastapi.testclient import TestClient__ -- достаём клиента для теста
- __from httpx import AsyncClient__ -- достаём клиента для теста (асинхронный)

---

# Стилизация кода

__`pip install black flake8 autoflake isort pyright`__ -- установка всех пакетов

__pyproject.toml__-- создать файл конфигураций в корне c содержимым: 
## Black (форматирование кода)
- #### Black настройки (файл:pyproject.toml)
- - __[tool.black]__ <br/> __line-length = 88__ #длинна строки <br/>  __target-version = ['py39']__
- __black app/bookings/service.py --diff --color__ -- вывод различий между оригинальным и отформатированным кодом
- __black app/bookings/service.py__ -- отформатировать конкретный файл
- __black app/__ -- отформатировать все файлы
## Isort (сортировка импортов)
- __isort app/main.py__ -- отсортировать конкретный файл
- __isort app__ -- отсортировать все файлы
- - #### Isort настройки (файл:pyproject.toml)
- - __[tool.isort]__ <br/> __profile = "black"__
## AutoFlake (Убирает все лишние импорты)
- #### AutoFlake настройки (файл:pyproject.toml)
- __[tool.autoflake]__ <br/> __check_diff = true__ <br/> __imports = ["sqlalchemy","app", "sqladmin"]__ <br/> __exclude = ["app/migrations"]__
- __\# noqa__ -- комментарий который нужно проставить что бы не удалились нужные импорты
- __autoflake app/bookings/service.py__ -- запустить проверку конкретного файла
- __autoflake app/ --recursive__ -- запустить проверки всех файлов
## Pyright (Проверка типизации и ошибок)
- #### Pyright настройки (файл:pyproject.toml)
- __[tool.pyright]__ <br/> __include = ["app"]__
- __pyright app/bookings/service.py__ -- проверка конкретного файла
- __pyright app/__ -- проверка всех файлов и папок
## Flake8 (проверка кода на ошибки)
- __.flake8__-- создать файл конфигураций в корне c содержимым:
- #### Flake8 настройки (файл:.flake8):
- - __[flake8]__ <br/> __max-line-length = 88__ <br/> __extend-ignore = E203__ <br/> __exclude = app/migrations__
- __flake8 app/bookings/service.py__ -- проверка конкретного файла
- __flake8 app/__ -- проверка всех файлов

---

# Логирование
### Настройка под себя
- __`pip install python-json-logger`__ -- Установка
- __logger.py__ --создаём в приложении
- - Настройки logger.py:
- - - __import logging__ <br/> __from datetime import datetime__ <br/> __from pythonjsonlogger import jsonlogger__ <br/> __from app.config import settings__ <br/> <br/>  __logger = logging.getLogger()__ <br/> __logHandler = logging.StreamHandler()__ <br/><br/> __class CustomJsonFormatter(jsonlogger.JsonFormatter):__<br/> &nbsp; &nbsp; &nbsp; &nbsp; __def add_fields(self, log_record, record, message_dict):__<br/>  &nbsp; &nbsp; &nbsp; &nbsp; __super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)__<br/> &nbsp; &nbsp; &nbsp; &nbsp; __if not log_record.get('timestamp'):__<br/> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  __now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")__ <br/> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; __log_record["timestamp"] = now__ <br/> &nbsp; &nbsp; &nbsp; &nbsp; __if log_record.get("level"):__<br/> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; __log_record["level"] = log_record["level"].upper()__<br/> &nbsp; &nbsp; &nbsp; &nbsp; __else:__<br/> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; __log_record["level"] = record.levelname__<br/> <br/> __formatter = CustomJsonFormatter(__<br/> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; __"%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"__<br/> __)__ <br/><br/> __logHandler.setFormatter(formatter)__<br/> __logger.addHandler(logHandler)__<br/> __logger.setLevel(settings.LOG_LEVEL)__<br/><br/>
- Добавляем декоратор Middleware в main.py :
- - __@app.middleware("http")__ <br/> __async def add_process_header(request: Request, call_next):__<br/> &nbsp; &nbsp; &nbsp; &nbsp;   __start_time = time.time()__ <br/> &nbsp; &nbsp; &nbsp; &nbsp;    __response = await call_next(request)__ <br/> &nbsp; &nbsp; &nbsp; &nbsp;    __process_time = time.time() - start_time__ <br/> &nbsp; &nbsp; &nbsp; &nbsp;    __logger.info("Request execution time", extra={__ <br/> &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;         __"process_time": round(process_time, 4)__ <br/> &nbsp; &nbsp; &nbsp; &nbsp;    __})__ <br/> &nbsp; &nbsp; &nbsp; &nbsp;    __return response__
- __logger.error(msg, extra={"test":test}, exc_info=True)__ -- пример вызова логера 
- - __exc_info=True__ -- отвечает за вывод полученой ошибки <br/>

## Sentry
- __https://sentry.io/welcome/__ -- HomePage Sentry
- __https://sentry.io/auth/login/__ -- создать аккаунт
- __`pip install --upgrade sentry-sdk[fastapi]`__ --установка Sentry
- в __main.py__ подключаем Sentry до создания приложения fastapi:
- - __import sentry_sdk__ <br/> <br/> __sentry_sdk.init(__<br/>  &nbsp; &nbsp; &nbsp; &nbsp; __dsn="уникальная ссылка",__ <br/> &nbsp; &nbsp; &nbsp; &nbsp; __traces_sample_rate=1.0,__ <br/>  &nbsp; &nbsp; &nbsp; &nbsp; __profiles_sample_rate=1.0,__ <br/> __)__

---

# Версионирование API (fastapi-versioning)

- __https://github.com/DeanWay/fastapi-versioning__ -- HomePage fastapi-versioning
- __`pip install fastapi-versioning`__ -- установка библиотеки
- настройка в __main.py__:
- - __from fastapi_versioning import VersionedFastAPI__<br/><br/> 
- - __app = VersionedFastAPI(__<br/> &nbsp; &nbsp; &nbsp; &nbsp;__app,__ <br/> &nbsp; &nbsp; &nbsp; &nbsp;  __version_format='{major}',__ <br/> &nbsp; &nbsp; &nbsp; &nbsp;   __prefix_format='/v{major}',__<br/>  &nbsp; &nbsp; &nbsp; &nbsp;  __# description='Greet users with a nice message',__ <br/> &nbsp; &nbsp; &nbsp; &nbsp;  __\# middleware=[Middleware(SessionMiddleware, secret_key='mysecretkey')]__ <br/>__)__
- Если происходит ошибка __MOUNT__ то нужно все статики мидверы и админки опустить с вниз
- __@version(1)__ -- Декоратор над ендпоинтом что бы указать версию
- __Важно__ - если задать версию то свагер становиться на таком урле  http://127.0.0.1:8000/v1/docs#/ <br/> И если у нас есть __Middleware__ Их уже указывать в VersionedFastAPI 

---

# Docker

- https://docs.docker.com/engine/install/ubuntu/ -- установка докера
- __Dockerfile__ -- создать в корне проекта c содержимым 
- - - __FROM python:3.10.12__ <br/> __RUN mkdir /booking__<br/> __WORKDIR /booking__ <br/> __COPY requirements.txt .__ <br/> __RUN pip install -r requirements.txt__<br/> __COPY . .__ <br/> __RUN chmod a+x /project_folder/docker/*.sh__ <br/>__CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]__<br/><br/>
- ### Основные команды докекра
- - __Создание и запуск контейнера__:
- - - __docker run__ -- Создать и запустить контейнер на основе образа.
- - - __docker run -p 9000:8000 name__ -- запустить контейнер на конкретном порту.
- - - __docker create__ -- Создать контейнер без его запуска.
- - - __docker start__ -- Запустить остановленный контейнер.<br/><br/>
- - __Основные операции с контейнерами:__

- - - __docker stop__ -- Остановить работающий контейнер.
- - - __docker restart__ -- Перезапустить контейнер.
- - - __docker pause__ -- Приостановить выполнение контейнера.
- - - __docker unpause__ -- Возобновить выполнение приостановленного контейнера.
- - - __docker exec__ -- Запустить команду внутри контейнера. <br/><br/>

- - __Информация о контейнерах:__
- - - __docker ps__ -- Показать список работающих контейнеров.
- - - __docker ps -a__ -- Показать список всех контейнеров (включая остановленные).
- - - __docker inspect__ -- Получить подробную информацию о контейнере. <br/><br/>

- - __Удаление контейнеров:__
- - - __ docker rmi $(docker images -q) --force__ -- удалить все имеющиеся контейнеры принудительно
- - - __docker rm__ -- Удалить контейнер (нужно указать идентификатор или имя контейнера).
- - - __docker container prune__ -- Удалить все остановленные контейнеры. <br/><br/>

- - __Управление образами:__
- - - __docker images__ -- Показать список доступных образов.
- - - __docker rmi__ -- Удалить образ (по имени или идентификатору).
- - - __docker pull__ -- Загрузить образ с реестра Docker Hub. <br/><br/>

- - __Создание и управление собственными образами:__
- - - __docker build__ -- Создать образ из Dockerfile.
- - - __docker build -t name__ -- Создать образ с своим название.
- - - __docker commit__ -- Создать образ из контейнера.
- - - __docker push__ -- Опубликовать образ в Docker Hub или другом реестре.<br/><br/>

- - __Работа с сетями:__
- - - __docker network create__ -- Создать пользовательскую сеть Docker.
- - - __docker network ls__ -- Показать список сетей.
- - - __docker network connect__ -- Присоединить контейнер к сети.
- - - __docker network disconnect__ -- Отсоединить контейнер от сети.<br/><br/>
- - __Логи и мониторинг:__

- - - __docker logs__ -- Просмотреть логи контейнера.
- - - __docker stats__ -- Показать статистику использования ресурсов контейнера.<br/><br/>

---

# Docker compose
- __docker-compose build__ -- создать все образы
- __docker-compose up__ -- запустить все образы
- __docker-compose.yml__ -- создать в корне проекта с содержимым:
- - __version: '3.7'__<br/>
__services:__<br/>
  __&nbsp; &nbsp; &nbsp; &nbsp;db:__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;image: postgres:14.9____<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;container_name: booking_db__<br/> 
&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; __volumes:__ <br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- postgresdata:/var/lib/postgresql/data__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;env_file:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- .env-non-dev__<br/>
&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;__ports:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- "5431:5432"__<br/>

  __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;redis:__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;image: redis:7__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;container_name: booking_redis__<br/>

  __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;booking:__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;build:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;context: .__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;container_name: booking_app__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;env_file:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- .env-non-dev__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;depends_on:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- db__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- redis__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;command: ["/booking/docker/app.sh"]__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;ports:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- "8080:8000"__<br/>

  __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;celery:__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;build:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;context: .__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;container_name: booking_celery__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;command: ["/booking/docker/celery.sh", "celery"]__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;env_file:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- .env-non-dev__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;depends_on:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- redis__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- booking__<br/>

  __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;flower:__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;build:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;context: .__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;container_name: booking_flower__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;command: [ "/booking/docker/celery.sh", "flower" ]__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;env_file:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- .env-non-dev__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;depends_on:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- redis__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- celery__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;ports:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- "5555:5555"__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;prometheus:__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;image: prom/prometheus:v2.43.0__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;container_name: prometheus__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;volumes:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- ./prometheus.yml:/etc/prometheus/prometheus.yml__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- prometheusdata:/prometheus__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;restart: unless-stopped__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;ports:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- "9090:9090"__<br/><br/>

  __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;grafana:__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;image: grafana/grafana:9.4.7__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;container_name: grafana__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;volumes:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- grafanadata:/var/lib/grafana__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;restart: unless-stopped__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;ports:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- "3000:3000"__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;environment:__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- GF_SECURITY_ADMIN_USER=root__<br/>
      __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;- GF_SECURITY_ADMIN_PASSWORD=41111__<br/>
&nbsp; &nbsp; &nbsp; &nbsp;__volumes:__<br/>
  __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;postgresdata:__<br/>
  __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;prometheusdata:__<br/>
  __&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;grafanadata:__<br/>

---

# Grafana (prometheus)
### prometheus
- __https://github.com/trallnag/prometheus-fastapi-instrumentator__ -- HomePage Prometheus
- __http://localhost:9090/targets?search=__ -- проверить статус Prometheus
- __`pip install prometheus-fastapi-instrumentator`__ -- Установка prometheus<br/><br/>
- подключение файл (__main.py__) {__указывается после версионирования__}:
- - __instrumentator = Instrumentator(__ <br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;should_group_status_codes=False,__<br/>
    __&nbsp; &nbsp; &nbsp; &nbsp;excluded_handlers=[".*admin.*", "/metrics"],__<br/>
__)__<br/>
__instrumentator.instrument(app).expose(app)__<br/><br/>
- в корне создать файл (__prometheus.yml__):
- - __global:__<br/>
  &nbsp; &nbsp; &nbsp; &nbsp;__scrape_interval: 15s__<br/>
  &nbsp; &nbsp; &nbsp; &nbsp;__external_labels:__<br/>
    &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;__monitor: 'codelab-monitor'__<br/>
__scrape_configs:__<br/>
  &nbsp; &nbsp; &nbsp; &nbsp;__- job_name: "prometheus"__<br/>
    &nbsp; &nbsp; &nbsp; &nbsp;__scrape_interval: 15s__<br/>
    &nbsp; &nbsp; &nbsp; &nbsp;__static_configs:__<br/>
      &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;__- targets: [ 'localhost:9090' ]__<br/>
  __&nbsp; &nbsp; &nbsp; &nbsp;- job_name: 'booking'__<br/>
    &nbsp; &nbsp; &nbsp; &nbsp; __scrape_interval: 5s__<br/>
    &nbsp; &nbsp; &nbsp; &nbsp; __static_configs:__<br/>&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;__- targets: [ 'booking:8000' ]__<br/><br/>

### Grafana
- Переходим на __localhost:3000__
- Login,Password -- __admin__
- в настройках выбираем DataSource
- добавляем прометеус. И меняем localhost на то как он назван в докере
- Далее идём в дашборд и добавляем новый. Нажимаем импортировать настройки и вставляем json из __grafana-dashbord.json__ предварительно в 11 местах подставив свой айди вместо "ваш id"
