# LLM Agent Platform

Домашнее задание по бонус-треку LLM (ИТМО, магистратура AI, 2025-2026).

**Трек:** Инфраструктурный - Разработка Агентной платформы

**Автор:** Дмитрий Горбунов

**Сроки:** 23.03.2026 - 12.04.2026

## Описание

Агентная платформа с поддержкой:
- Регистрации A2A-агентов
- Подключения различных LLM-провайдеров
- Маршрутизации запросов (round-robin, latency-based, health-aware)
- Сбора телеметрии (OpenTelemetry, Prometheus, Grafana)

## Уровни реализации

### Уровень 1 - Минимальный прототип (10 баллов)
- Docker Compose окружение
- Несколько LLM-провайдеров (реальные API + мок-сервисы)
- LLM-балансировщик (round-robin, статические веса, роутинг по моделям)
- Поточная передача ответов (streaming)
- OpenTelemetry + Prometheus + Grafana
- Health-check endpoints

### Уровень 2 - Реестры и умная маршрутизация (20 баллов)
- A2A Agent Registry с Agent Card
- Динамическая регистрация LLM-провайдеров
- Latency-based и health-aware routing
- TTFT, TPOT метрики, стоимость запросов
- MLFlow трассировка

### Уровень 3 - Продвинутая платформа (25 баллов)
- Guardrails (prompt-injection detection, утечка секретов)
- Авторизация агентов и LLM (токены)
- Нагрузочное тестирование (throughput, латентность, устойчивость)

## Стек

- Python 3.12, FastAPI
- Docker Compose
- OpenTelemetry, Prometheus, Grafana
- MLFlow
- Locust (нагрузочное тестирование)

## Запуск

```bash
docker compose up --build
```

## Структура проекта

```
llm-agent-platform/
├── src/
│   ├── api/              # FastAPI endpoints
│   ├── balancer/         # Load balancing strategies
│   ├── registry/         # Agent & provider registry
│   ├── guardrails/       # Request filtering
│   ├── auth/             # Authorization
│   ├── telemetry/        # OpenTelemetry setup
│   └── providers/        # LLM provider adapters
├── tests/
├── docker-compose.yml
├── Dockerfile
├── grafana/              # Dashboards
├── prometheus/           # Config
└── README.md
```
