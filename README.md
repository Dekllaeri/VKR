# <Название проекта>

## Version <Версия проекта>

Дипломный проект.

**Цель создания проекта:** <Цель создания проекта>.

**Целевой пользователь системы:** <Целевой пользователь>.

**Програмный состав проекта:**

* Back-end приложение (Dgango REST API)

**Роли пользователей:**

* Администратор

**Основные функциональные возможности:**

* <Функциональные возможности>

**Используемые технологии:**

* Django (Django Rest Framework)
* PostgreSQL
* Docker / Docker Compose
* Nginx

## Запуск проекта

<details>
<summary>
<strong>
Локально
</strong>
</summary>

### Склонировать репозиторий:
```sh
git clone https://github.com/Dekllaeri/VKR.git
```

<details>
<summary>
<strong>
База данных (Подготовка БД PostgreSQL)
</strong>
</summary>

### 1. Установить PostgreSQL:
- Для Windows
  Скачать дистрибутив [PostgreSQL](https://postgrespro.ru/windows) и установить в соответствии с инструкцией
  (задать логин и пароль суперпользователя (по умолчанию - postgres), для локального использования можно отключить
  "Разрешить подключения с любых IP-адресов")

### 2. Открыть SQL Shell или запустить psql:
```sh
psql -U postgres
```
и ввести запрашиваемый пароль суперпользователя

### 3. Создать нового пользователя для проекта
```sh
CREATE USER vkrback WITH PASSWORD '1234';
```

### 4. Создать БД и задать владельца
```sh
CREATE DATABASE vkrback OWNER=vkrback;
```

### 5. Проверить наличие созданной БД, открыв список существующих:
```sh
\l
```

<details>
<summary>
Для удаления БД (при наличии ошибок) выполнить:
</summary>

```sh
DROP DATABASE vkrback;
```
</details>
</details>

<details>
<summary>
<strong>
Backend приложение
</strong>
</summary>

### 1. Установить виртуальное окружение:
```sh
python -m venv .venv
```
`.venv` - путь к виртуальному окружению

### 2. Активировать виртуальное окружение:

- Для Windows
```sh
.venv\Scripts\activate
```

- Для Linux и MacOS
```sh
source venv/bin/activate
```

### 3. Обновить pip и установить зависимости python:
```sh
pip install --upgrade pip
```
```sh
pip install -r requirements.txt
```

### 4. Создать и провести миграции БД:
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```

### 5. Загрузить фикстуры:
```sh
python manage.py loaddata vkrbackdata.json
```

### 6. Запустить тестовый web-сервер:
```sh
python manage.py runserver
```
По умолчанию сервер будет запущен по адресу [127.0.0.1:8000](http://127.0.0.1:8000)
</details>
</details>

####
<details>
<summary>
<strong>
Через Docker/DockerCompose
</strong>
</summary>

### Собрать билд и поднять контейнер
```sh
docker-compose -f docker-compose.yml up -d --build
```
</details>

####
<details>
<summary>
<strong>
Полезные команды
</strong>
</summary>

### Создание дампа базы данных
```sh
python -Xutf8 manage.py dumpdata --indent=2 --exclude sessions --exclude contenttypes --exclude admin.logentry --exclude auth.permission -o vkrbackdata.json
```
</details>
