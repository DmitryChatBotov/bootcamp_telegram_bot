## Telegram bot for beauty salon

Environment variables
---------------------
| Переменная         |               Описание                | Значение по умолчанию |
|--------------------|:-------------------------------------:|:---------------------:|
| TELEGRAM_BOT_TOKEN |             TG bot token              |    some token here    |
| SQLITE_FILE | Test db file for CRM system imitation |        name.db        |
| OPENAI_API_KEY |            OpenAI api key             |     some key here     |


Project structure
-----------------
```
    ├── bot                       <- Telegram bot module.
    │   └── common                <- Module with useful utilities.
    │   └── crm_mock              <- Module that emulates the customer's CRM.
    │   └── crud                  <- Queries to the langchain models
    │   └── handlers              <- Telegram bot routings.
    │   └── models                <- NN models.
    │   └── schemas               <- Dataclasses.
    │   └── .env.dist             <- Template .env file.
    │   └── Dockerfile            <- Production Docker file.
    │   └── Dockerfile.dev        <- Development Docker file.
    │   └── main.py               <- Telegram bot entrypoint.
    │   └── poetry.lock           <- Dependency file.
    │   └── pyproject.toml        <- File with project configuration.
    ├── notebooks                 <- Experiments with langchain
    |
    ├── docker-compose.dev.yaml   <- Development docker-compose file
    |
    └── docker-compose.yaml       <- Production docker-compose file.
```



How to launch
---------------------
1. Create .env file based on .env.dist in ./bot module. Fill the varaibles.
2. Run command:
```sudo docker compose up --build -d```

