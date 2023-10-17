# FastApi

-  __`pip install fastapi[all]`__ -- установка фаст апи с всеми зависимостями
  - __uvicorn app.main:app --reload__ -- запуск приложения в дев режиме

---
# Alembic

- __alembic init migrations__ -- инициализация алембика
- __alembic.ini__ -- добавить метадату и модели
- __env.py__ -- если выносим alembic.ini выносим на уровень выше добавить <br/>  __sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))__
- __env.py__ -- добавляем настройку подключения к базе данных, расширяем настройки  <br/>  __config.set_main_option('sqlalchemy.url', f"{DATABASE_URL}?async_fallback=True")__
- __alembic revision --autogenerate -m "init project"__ -- создать первые миграции. Делать из корня проекта а не приложения
- __alembic upgrade head"__ -- применить миграции. Вместо HEAD можно подставить номер миграции
- __alembic downgrade -1"__ -- откатиться на 1 миграцию назад

---

# Celery

- __`pip install celery`__ --  установка селери и флавер
- создать файл с похожим содержанием <br/> __from celery import Celery__ <br/>
    __celery = Celery(__ <br/>
    __"tasks",__<br/>
    __broker="redis://localhost:6379",__<br/>
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

