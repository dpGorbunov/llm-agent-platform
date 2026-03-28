# Нагрузочное тестирование

## Установка

```bash
pip install -r loadtests/requirements.txt
```

## Запуск

### Все сценарии

```bash
export MASTER_TOKEN=<ваш-токен>
./loadtests/run_tests.sh http://localhost:8000
```

### Отдельный сценарий

```bash
# Normal: 15 пользователей, 60 секунд
locust -f loadtests/locustfile.py --headless --users 15 --spawn-rate 5 --run-time 60s --host http://localhost:8000

# С web-интерфейсом (http://localhost:8089)
locust -f loadtests/locustfile.py --host http://localhost:8000
```

## Сценарии

| Сценарий | Пользователи | Spawn Rate | Время | Модели |
|----------|-------------|------------|-------|--------|
| Normal   | 15          | 5/s        | 60s   | Бесплатные (step-3.5-flash, nemotron-3-super) |
| Peak     | 30          | 10/s       | 60s   | Бесплатные + платные (deepseek-chat, gpt-oss-120b) |
| Stress   | 50          | 20/s       | 30s   | Все модели, провоцирование 429 |

## Безопасность

- Каждый класс пользователей ограничен 200 запросами (по умолчанию)
- Промпты короткие (5-10 токенов), `max_tokens=10`
- Переопределение лимита: `export LOCUST_MAX_REQUESTS=500`

## Результаты

CSV-файлы сохраняются в `loadtests/results/`:
- `*_stats.csv` - общая статистика по эндпоинтам
- `*_stats_history.csv` - статистика по времени
- `*_failures.csv` - детали ошибок

### Метрики

- **RPS** (Requests Per Second) - пропускная способность
- **Median/P95/P99 latency** - время ответа
- **Failure rate** - доля ошибок (429, 502, 504)
- Ожидаемое поведение при Stress: рост 429 ошибок (rate limiting)

## Переменные окружения

| Переменная | По умолчанию | Описание |
|-----------|-------------|----------|
| `MASTER_TOKEN` | `test-master-token` | Токен авторизации |
| `LOCUST_MAX_REQUESTS` | `200` | Максимум запросов на класс |
