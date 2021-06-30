# astra_test

### 1. Разворачиваем базу командой
```shell 
docker run --name postgres -e POSTGRES_PASSWORD=astra -e POSTGRES_USER=astra -e POSTGRES_DB=astra -d -p 5432:5432 postgres
```
### 2. Создаем виртуальное окружение и подгружаем зависимости
```shell
python3 -m venv venv # Может меняться в зависимости от платформы
source venv/bin/activate # Может меняться в зависимости от платформы
pip install -r requirements.txt
```
### 3. Производим миграцию
```shell
alembic upgrade head
```
### 4. Запускаем сервер
```shell
python start.py
```

### Сваггер доступен по http://localhost:8080/docs

---

### Консольное приложение запускается командой
```shell
python updater.py
```