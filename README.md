## Telegram bot for beauty salon

## Environment variables
| Переменная         |               Описание                | Значение по умолчанию |
|--------------------|:-------------------------------------:|:---------------------:|
| TELEGRAM_BOT_TOKEN |             TG bot token              |    some token here    |
| SQLITE_FILE | Test db file for CRM system imitation |        name.db        |
| OPENAI_API_KEY |            OpenAI api key             |     some key here     |
| TIMEZONE |     Timezone of docker container      |     Europe/Moscow     |

## How to launch
1. Create .env file based on .env.dist in ./bot module. Fill the varaibles.
2. Run command:
```sudo docker compose up --build -d```

