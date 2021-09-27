### Запуск проекта:

##### 1.    Добавление окружения в Docker:
В папке <code>celery</code> нужно создать файл <code>.env</code> в котором прописать данные для подключения к SMTP серверу

    MAIL_SMTP_SERVER=servername
    MAIL_SMTP_LOGIN=login
    MAIL_SMTP_PASSWORD=password


##### 2.    Запуск докера:
    docker-compose up -d --build
    
    
### Настройки:
При старте проекта происходит миграция суперпользователя

        login: admin@admin.com
        password: admin

##### Endpoints:

###### Авторизация:

 <code>/auth/login/</code>   <code>post</code>

    Body.json:

    {
        "email": "admin@admin.com",
        "password": "admin"
    }

###### Выход из авторизации:

<code>/auth/logout/</code>   <code>post</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
###### Регистрация:

<code>/auth/registration/</code>     <code>post</code>
    
    Body.json:

    {
        "email": "email@address.com",
        "password1": "email@address.com",
        "password2": "email@address.com",
    }

###### Импорт YAML файла с продуктами:

<code>/import_price/</code>     <code>post</code>
    
    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    Body.form
    files: file.yaml

###### Продукты:

#####1. Список

<code>/api/v1/product/</code>     <code>get</code>

#####2. Детализация

<code>/api/v1/product/product_number</code>     <code>get</code>

#####3. Создание

<code>/api/v1/product/</code>     <code>post</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    Body.json:

    {
        "name": "Смартфон Apple iPhone XS Max 512GB (розовый)",
        "category": 224,
        "features": [
            {
                "feature": "Диагональ (дюйм)",
                "value": "6.5"
            },
            {
                "feature": "Разрешение (пикс)",
                "value": "2688x1242"
            },
            {
                "feature": "Встроенная память (Гб)",
                "value": "512"
            },
            {
                "feature": "Цвет",
                "value": "Розовый"
            }
        ],
        "assortment": [
            {
                "quantity": 11,
                "available": true,
                "description": 123,
                "price": 10000
            }
        ]
    }

При создании создает именно единиица ассортимента и продукт, если такого не было ранее. 
Т.е. продукт привязанный к магазину продающему его. Можно не указывать <code>features</code>.

#####4. Изменеие

<code>/api/v1/product/product_number</code>     <code>patch</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    Body.json:

    {
        "name": "Смартфон Apple iPhone XS Max 512GB (розовый)",
        "features": [
            {
                "id": 1,
                "feature": "Диагональ (дюйм)",
                "value": "6.6"
            },
            {
                "id": 2,
                "feature": "Разрешение (пикс)",
                "value": "2688x1242"
            },
            {
                "id": 3,
                "feature": "Встроенная память (Гб)",
                "value": "512"
            },
            {
                "id": 4,
                "feature": "Цвет",
                "value": "Розовый"
            }
        ],
        "category": 224,
        "assortment": [
            {
                "quantity": 11,
                "available": true,
                "price": "10000.00",
                "description": "1233"
            }
        ]
    }
    
#####4. Удаление

<code>/api/v1/product/product_number</code>     <code>delete</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    
###### Характеристики:

#####1. Список

<code>/api/v1/feature</code>     <code>get</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
#####1. Детализация

<code>/api/v1/feature/feature_number</code>     <code>get</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
#####3. Добавление

<code>/api/v1/feature/</code>     <code>post</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    Body.json
    
    {
        "name": "Втроенная память(Гб)"
    }
    
#####4. Редактирование

<code>/api/v1/feature/feature_number/</code>     <code>patch</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    Body.json
    
    {
        "name": "Втроенная флэш память(Гб)"
    }
    
#####5. Удаление

<code>/api/v1/feature/feature_number/</code>     <code>delete</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX


###### Заказ:

Заказ в статусе <code>NEW</code> считается корзиной.

Как только переходит в <code>IN_PROGRESS</code> происходит отправка письма о заказе.

#####1. Список наименований в новом заказе

<code>/api/v1/order-item</code>     <code>get</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
Отдает сипок того, что лежит в заказе со статусом <code>NEW</code> текущего пользователя.
    
#####2. Добавление пункта в заказ
Добавление происходит с корзину, т.е. в заказ в статусе <code>NEW</code>

<code>/api/v1/order-item/</code>     <code>post</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    Body.json
    
    {
        "assortment": {
            "id": 28
    },
        "quantity": 1
    }
    
#####3. Изменение пункта заказа
Можно поменять только кол-во

<code>/api/v1/order-item/order-item_number/</code>     <code>patch</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    Body.json
    
    {
        "quantity": 10
    }
    
#####4. Удаление

<code>/api/v1/order-item/order-item_number/</code>     <code>delete</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    
#####5. Список заказов

<code>/api/v1/order/</code>     <code>get</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
#####6. детализация заказа

<code>/api/v1/order/order_number</code>     <code>get</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
#####6. Изменение заказа

<code>/api/v1/order/order_number</code>     <code>patch</code>

    Header:
    Authorization: Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    Body.json
    
        {
        "status": "IN_PROGRESS",
        "recipient_email": "zerroCrop@inbox.ru",
        "recipient_first_name": "FF",
        "recipient_last_name": "fd",
        "recipient_patronymic": "fd",
        "recipient_phone": "9898989",
        "profile": 4,
        "city": "Moscow",
        "street": "street",
        "house_number": 11,
        "housing": null,
        "structure": null,
        "apartment": "3",
        "additional_info": null,
        "order_items": [
            {
                "id": 5,
                "assortment": "Смартфон Apple iPhone XS Max 512GB (золотистый)",
                "quantity": 3,
                "price": 110000.0
            },
            {
                "id": 6,
                "assortment": "Смартфон Apple iPhone XR 256GB (красный)",
                "quantity": 10,
                "price": 65000.0
            }
        ]
    }
