# RESTAPI-service
Система авто индексации python - кода. Позволяет найти функцию или класс и понять, что она делает.

Проблема:
Первый день в крупном IT: сотни тысяч строк кода. Вопрос «где авторизация?» прост, но ответ ищется часами. Компания теряет время старших разработчиков на  объяснения, а новичок — в растерянности.

Решение: структурированный каталог кода — сервис, который знает, какие функции и классы есть в каждом файле, и умеет отвечать на запросы через API.


# 1. Установка зависимостей.

```bash
pip install -r requirements.txt
```

# 2. Запуск индексации.

```bash
python indexer.py
```

# 3. Запуск API сервера 
```bash
uvicorn main:app --reload
```

# ОПИСАНИЕ СХЕМЫ БД
Таблица pyfiles
| Колонка | Тип | Описание |
|---------|-----|----------|
| `name_file` | TEXT | Имя файла|
| `type_element` | TEXT | function, class, method|
| `name_element` | TEXT | Имя элемента|
| `parrent_class` | TEXT | Родительский класс(для методов)|
| `str_begin` | INTEGER | Номер строки начала|
| `str_end` | INTEGER | Номер строки конца|
| `docstring` | TEXT | Документация 


# Примеры ответов 
1.GET/api/files - получение списка файлов с количеством функций в нем
Запрос:
```bash
curl http:127.0.0.1:8000/api/files
```

Ответ: 
```json
[
  {
    "file name:": "account_db.py",
    "quantity functions in this file:": 2
  },
  {
    "file name:": "audit.py",
    "quantity functions in this file:": 2
  },
]
```

2.GET/api/files/{name}/structure -получение полной структуры всех функций, классов, методов определенного файла
Запрос:
```bash
curl http:127.0.0.1:8000/api/files/email.py/structure
```

Ответ:
```json
{
  "name file ": "email.py",
  "functions ": [
    {
      "name file ": "email.py",
      "name element ": "service_email_0",
      "start line ": 6,
      "end line ": 8,
      "docstring": "Manages system configuration within the current execution context."
    },
    {
      "name file ": "email.py",
      "name element ": "service_email_2",
      "start line ": 15,
      "end line ": 17,
      "docstring": "Manages user data within the current execution context."
    }
  ],
  "classes ": [
    {
      "name file ": "email.py",
      "name element ": "Email1",
      "start line ": 10,
      "end line ": 13,
      "docstring ": "Calculates the user data for the core application logic."
    }
  ],
  "methods ": [
    {
      "name file ": "email.py",
      "parrent class ": "Email1",
      "start line ": 12,
      "end line ": 13,
      "docstring ": ""
    }
  ]
}
```
3. GET/api/search?={keyword} - поиск функции, класса, метода по ключевому слову.

Запрос:
```bash
curl http:127.0.0.1:8000/api/search?keyword=converter
```

Ответ:
```json
[
  {
    "file name ": "converters.py",
    "type element ": "class",
    "name element ": "Converters0",
    "docstring ": "Calculates the system configuration for the core application logic."
  },
  {
    "file name ": "converters.py",
    "type element ": "class",
    "name element ": "Converters1",
    "docstring ": "Represents the authentication logic for the core application logic."
  },
  {
    "file name ": "converters.py",
    "type element ": "class",
    "name element ": "Converters2",
    "docstring ": "Validates the payment transaction for the core application logic."
  },
  {
    "file name ": "converters.py",
    "type element ": "class",
    "name element ": "Converters3",
    "docstring ": "Handles the user data for the core application logic."
  }
]
```
Опционално можно добавить фильтр по функциям,классам, методам.

Запрос:
```bash
curl http:127.0.0.1:8000/api/files/search?keyword=converter&type=class
```

Ответ: 
```json
[
  {
    "file name ": "converters.py",
    "type element ": "class",
    "name element ": "Converters0",
    "docstring ": "Calculates the system configuration for the core application logic."
  },
  {
    "file name ": "converters.py",
    "type element ": "class",
    "name element ": "Converters1",
    "docstring ": "Represents the authentication logic for the core application logic."
  },
  {
    "file name ": "converters.py",
    "type element ": "class",
    "name element ": "Converters2",
    "docstring ": "Validates the payment transaction for the core application logic."
  },
  {
    "file name ": "converters.py",
    "type element ": "class",
    "name element ": "Converters3",
    "docstring ": "Handles the user data for the core application logic."
  }
]
```
4. GET /api/stats - получение статистики обработанных файлов

Запрос: 
```bash
curl http:127.0.0.1:8000/api/files/stats
```

Ответ: 
```json
{
  "total files ": 30,
  "total functions ": 48,
  "total classes ": 89
}
```


