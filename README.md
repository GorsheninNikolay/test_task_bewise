# test_task_bewise
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Docker Automated buil](https://img.shields.io/docker/automated/mongkok/coverage.svg)](https://hub.docker.com/r/mongkok/coverage)

- [Как запускать?](#как-запускать)
- [Примеры запросов](#примеры-запросов)

## Как запускать?

1. Зайдите в GitBash, при необходимости установите.

2. При помощи команд 

Перейти в каталог
```
cd "каталог"
```
Подняться на уровень вверх:
```
cd .. 
```
:exclamation: Перейдите в нужный каталог для клонирования репозитория :exclamation:

3. Клонирование репозитория
```
git clone https://github.com/GorsheninNikolay/test_task_bewise
```

Также переходим в директорию командой ```cd test_task_bewise```

4. Запуск проекта
```
docker-compose up -d --build
```

5. Переход в CLI

Командой ```docker ps``` находим запущенный процесс и копируем его id.

Затем выполняем команду ```docker exec -it <id> bash``` для перехода в среду CLI.

6. Миграции

Внутри CLI выполняем команду ```cd test_task``` для перехода в директорию приложения.

Затем выполняем команды ```flask db init && flask db migrate && flask db upgrade``` для создания миграций.

Готово! Можно заходить по ip адресу http://127.0.0.1:5000/ :wink:

:exclamation: Документация по адресу http://127.0.0.1:5000/

Если проект требуется остановить, нужно выполнить команду ```docker-compose down```


## Примеры запросов

GET запрос по адресу http://127.0.0.1:5000/api/document
![GET запрос на api/document](https://github.com/GorsheninNikolay/test_task_bewise/raw/main/examples/GET_document.png)

GET запрос по адресу http://127.0.0.1:5000/api/document/85427
![GET запрос на api/document](https://github.com/GorsheninNikolay/test_task_bewise/raw/main/examples/GET_document_85427.png)

POST запрос по адресу http://127.0.0.1:5000/api/document
![POST запрос на api/document](https://github.com/GorsheninNikolay/test_task_bewise/raw/main/examples/POST_document.png)

DELETE запрос по адресу http://127.0.0.1:5000/api/document
![DELETE запрос на api/document](https://github.com/GorsheninNikolay/test_task_bewise/raw/main/examples/DELETE_document.png)
