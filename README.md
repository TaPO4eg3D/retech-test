Так как в задании сказано, что можно использовать любую СУБД, ничего не мудрил оставил, SQLITE. Debug режим отключать не стал,
так как проект все же тестовый. В .gitignore указал БД в т.ч.

# Инструкция

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Далее необходимо залогиниться в админку Джанго для создания данных для тестирования. Создать несклько организация, а также ToDo
списки и сами ToDo.

По умолчанию, суперпользователь не имеет никакой привязки к организациям, так необходимо пройти процесс регистрации.
Это можно сделать по адресу **/api/register**

Пример запроса:
```json
{
	"email": "fo.denis2010@yandex.ru",
	"password": 123,
	"organizations": [1,2]
}
```
Получить список организация для прохождения регистрации можно по адресу **/api/organizations**

Пример ответа (регистрация):
```json
{
    "token": "3af26893356f20cf4a2566e7abda9cc966cff8ae",
    "email": "fo.denis201001@yandex.ru",
    "organizations": [
        {
            "id": 1,
            "name": "ReTech"
        },
        {
            "id": 2,
            "name": "Google"
        }
    ],
    "active_organization": {
        "id": 1,
        "name": "ReTech"
    }
}
```

В приложении используется Bearer Token авторизация. Заголовки выглядят след. образом:
```
Authorization: Bearer 2f07d7ff8354b0a6023865cc8b3b0a0df4fb718b
```


Первая введенная организция становится активной, для того чтобы это изменить нужно пройти процесс авторизации,
где явно указать нужную организацию.

Пример запроса:
```json
{
	"email": "fo.denis201001@yandex.ru",
	"password": 123,
	"active_organization": 2
}
```
Для того, чтобы отобразить все организации, доступные пользователю, необходимо опустить ключ **active_organizatons**
Пример ответа:
```json
{
    "active_organization": {
        "message": "This field is required",
        "available_organizations": [
            {
                "id": 1,
                "name": "ReTech"
            },
            {
                "id": 2,
                "name": "Google"
            }
        ]
    }
}
```

Ну и наконец, чтобы отобразить ToDo списки, необходимо сделать GET запрос по эндпоинту **/api/todos**
Пример ответа:
```json
[
    {
        "id": 1,
        "todo_set": [
            {
                "id": 1,
                "created_at": "2019-07-08T17:27:53Z",
                "description": "Пройти собеседование",
                "list": 1,
                "created_by": 1
            }
        ],
        "name": "Список задач к 20 числу",
        "organization": {
            "id": 1,
            "name": "ReTech"
        }
    }
]
```
