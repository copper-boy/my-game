# my-game

## How to start

First of all you need to create .env files:

+ Structure
  - .admin.env
    ```dotenv
    ADMIN_LOGIN=admin_login_here@email.com
    ADMIN_PASSWORD=admin_password_here
    INFINITY_ADMIN_TOKEN=access_token_here
    ```
  - .env
    ```dotenv
    COMPOSE_PROJECT_NAME=my-game
    
    PYTHONPATH=/app/
    PYTHONDONTWRITEBYTECODE=1
    PYTHONUNBUFFERED=1
 
    PG_API_USER=api
    PG_API_PASSWORD=api
    PG_API_DB=api
    
    API_DATABASE_URI=asyncpg://api:api@api_db:5432/api
    
    PG_HANDLER_USER=handler
    PG_HANDLER_PASSWORD=handler
    PG_HANDLER_DB=handler
    
    HANDLER_DATABASE_URI=asyncpg://handler:handler@handler_db:5432/handler
    
    RABBITMQ_USERNAME=rabbit
    RABBITMQ_PASSWORD=rabbit
    RABBITMQ_VHOST=rabbit
    AMQP_URI=amqp://rabbit:rabbit@rabbit:5672/rabbit
    ```
  - .keys.env
    ```dotenv
    # generate with: openssl rand -hex 32
    JWT_SECRET_KEY=34281c01acd27f44214bf306ed88cb5de20cfd1b667c75ff771e3afdbb8402c9
    ```
  - .site.env
    ```dotenv
    API_SITE_BASE_URL=http://api_service:14961
    ```
  - .telegram.env
    ```dotenv
    # see documentation how to get telegram bot access token
    TELEGRAM_BOT_API_TOKEN=telegram_bot_token
    ```
  
The next step is build docker images:
```shell
docker-compose build
```

After you need to start docker images:
```shell
docker-compose up -d
```

If you needs logs follow this command:
```shell
docker-compose logs -f
```

Stop docker images:
```shell
docker-compose down
```

Remove database data:
```shell
docker-compose down --volumes
```

## Contact me

+ How can you contact me:
  - sermed512@gmail.com
  - https://t.me/copper_boy
