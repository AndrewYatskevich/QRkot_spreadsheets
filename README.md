# QRkot

### Описание

API фонда, который собирает пожертвования на различные целевые проекты:
на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей
колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели,
связанные с поддержкой кошачьей популяции

### Технологии

Python 3.9
FastAPI 0.78.0

### Запуск проекта в dev-режиме

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AndrewYatskevich/QRkot_spreadsheets.git
```

```
cd QRkot_spreadsheets
```

- Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

- Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

- Выполнить миграции:

```
alembic upgrade head
```

- Запустить проект:

```
uvicorn app.main:app
```

Автор: Андрей Яцкевич https://github.com/AndrewYatskevich