# FastApi

-  __pip install fastapi[all]__ -- установка фаст апи с всеми зависимостями
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

- __pip install celery flower__ --  установка селери и флавер
- создать файл с похожим содержанием <br/> __from celery import Celery__ <br/>
    __celery = Celery(__ <br/>
    __"tasks",__<br/>
    __broker="redis://localhost:6379",__<br/>
    __include=["app.tasks.tasks"]__<br/>
    __)__
-  __celery -A app.tasks.celery:celery worker --loglevel=INFO --pool=solo__ -- Запуск задач селери
