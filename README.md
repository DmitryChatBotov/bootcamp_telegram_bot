## Telegram bot for beauty salon

## Environment variables
| Переменная         |               Описание                | Значение по умолчанию |
|--------------------|:-------------------------------------:|:---------------------:|
| TELEGRAM_BOT_TOKEN |             TG bot token              |    some token here    |
| SQLITE_FILE | Test db file for CRM system imitation |        name.db        |
| OPENAI_API_KEY |            OpenAI api key             |     some key here     |
| TIMEZONE |     Timezone of docker container      |     Europe/Moscow     |

## How to launch
1. Docker method:
```sudo docker compose up --build -d```
2. Local launch method:
```poetry install```
```python bot/main.py```

