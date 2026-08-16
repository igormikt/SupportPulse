# SupportPulse — Сервис обработки обращений (MVP)

MVP-сервис классификации обращений пользователей с помощью ИИ (GPT-4o-mini через ProxyAPI). Автоматически определяет тему обращения, генерирует ответ и сохраняет историю в базу данных.

## 📋 Требования

- **Python 3.11+**
- **Платформа:** Windows 11 / macOS / Linux
- **VPS (опционально):** Ubuntu/Debian, Docker, Docker Compose
- **Аккаунт:** [ProxyAPI](https://proxyapi.ru) (для работы ИИ)

---

## 🚀 Создание и запуск проекта (Локально)

### 1. Установка зависимостей

```powershell
# Создаём и активируем виртуальное окружение
python -m venv .venv
. .venv\Scripts\Activate.ps1

# Устанавливаем библиотеки
python -m pip install -r requirements.txt
```

### 2. Настройка окружения

```powershell
# Создаем файл настроек
Copy-Item .env.example .env

# Открываем файл для редактирования и вставляем ключ ProxyAPI
notepad .env
```

Содержимое `.env`:
```env
PROXYAPI_API_KEY=ваш_реальный_ключ_от_proxyapi
PROXYAPI_BASE_URL=https://api.proxyapi.ru/openai/v1
MODEL_NAME=gpt-4o-mini
DB_PATH=data/supportpulse.db
```

### 3. Запуск сервера

```powershell
# Активируем окружение
. .venv\Scripts\Activate.ps1

# Запускаем
python -m uvicorn app.main:app --reload
```

Сервер запустится на: **http://127.0.0.1:8000**

---

## 🧪 Тестирование и Проверка

После запуска сервера проверьте его работу двумя способами.

### Способ 1: Удобный (через Swagger UI)
1. Откройте браузер и перейдите по адресу: **http://127.0.0.1:8000/docs**
2. Найдите раздел **POST /triage** (зеленая кнопка).
3. Нажмите **Try it out**.
4. В поле **Request body** вставьте пример:
```json
{
  "text": "Не могу войти в аккаунт, забыл пароль",
  "channel": "chat",
  "client_id": "user_001"
}
```
5. Нажмите **Execute**.

**Ожидаемый результат:**
- **Status code:** `200`
- **Response body:**
```json
{
  "category": "support",
  "draft_reply": "Здравствуйте! Для восстановления доступа...",
  "confidence": "high",
  "escalate": false
}
```

### Способ 2: Через терминал (Python)
Используйте этот способ для проверки в консоли.

**Тест 1: Проверка здоровья сервера**
```powershell
curl.exe http://127.0.0.1:8000/health
# Ответ: {"status":"ok","version":"1.0.0"}
```

**Тест 2: Отправка обращения**
```powershell
python -c "import requests; r = requests.post('http://127.0.0.1:8000/triage', json={'text': 'С меня списали деньги дважды', 'channel': 'email', 'client_id': 'test_billing'}); print(r.json())"
# Ответ: {'category': 'billing', ...}
```

**Тест 3: Просмотр базы данных (API)**
```powershell
# Получить последние 5 обращений
python -c "import requests; r = requests.get('http://127.0.0.1:8000/api/tickets?limit=5'); print(r.json())"

# Получить статистику
python -c "import requests; r = requests.get('http://127.0.0.1:8000/api/stats'); print(r.json())"
```

---

## 🐳 Развёртывание на VPS (Beget / Ubuntu)

Проект подготовлен для размещения на виртуальном сервере с использованием **Docker Compose**. Это позволяет управлять несколькими сервисами (ботами, приложениями) на одном сервере.

### Структура файлов для сервера
Перед загрузкой на сервер убедитесь, что у вас есть следующие файлы:
- `Dockerfile` — инструкция для сборки образа приложения.
- `docker-compose.yml` — оркестратор для запуска нескольких сервисов.
- `nginx/nginx.conf` — конфиг для распределения доменов.

### Пошаговая инструкция по установке

**1. Подключение к серверу**
```bash
ssh user@your_server_ip
```

**2. Установка Docker и Docker Compose (если нет)**
```bash
sudo apt update
sudo apt install docker.io docker-compose-plugin -y
sudo systemctl start docker
sudo systemctl enable docker
```

**3. Развертывание проекта**
Скопируйте файлы проекта на сервер (или клонируйте репозиторий):
```bash
git clone https://github.com/your-username/supportpulse.git
cd supportpulse
```

**4. Настройка окружения**
Создайте файл `.env` на сервере:
```bash
nano .env
```
Вставьте туда свой ключ ProxyAPI.

**5. Запуск через Docker Compose**
```bash
# Собрать образы и запустить сервисы в фоне
sudo docker compose up -d --build
```

**6. Проверка**
Убедитесь, что контейнеры запущены:
```bash
sudo docker compose ps
```
Теперь ваш API доступен по адресу сервера (или домену) на порту 80 (если настроен Nginx) или 8001 (прямой доступ).

---

## 📁 Структура проекта

```
SupportPulse/
├── .env.example              # Шаблон переменных окружения
├── .gitignore                # Исключения для git
├── Dockerfile                # Инструкция для Docker
├── docker-compose.yml        # Управление сервисами (VPS)
├── requirements.txt          # Зависимости Python
├── README.md                 # Документация
│
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI приложение (маршруты)
│   ├── config.py             # Чтение настроек из .env
│   ├── schemas.py            # Pydantic модели (валидация)
│   ├── service.py            # Логика обработки
│   ├── llm.py                # Интеграция с OpenAI/ProxyAPI
│   ├── limiter.py            # Ограничение запросов (Rate Limit)
│   ├── db.py                 # SQLite база данных
│   └── api.py                # Эндпоинты для просмотра БД
│
├── nginx/
│   └── nginx.conf            # Настройка веб-сервера
│
├── data/                     # Папка для базы данных (сохраняется)
└── logs/                     # Логи работы
```

---

## 🔧 Компоненты и возможности

| Компонент | Описание |
|-----------|----------|
| **Endpoint** | `POST /triage` — принимает текст, канал, client_id |
| **Endpoint** | `GET /api/tickets` — просмотр истории обращений |
| **Endpoint** | `GET /api/stats` — статистика (по категориям/каналам) |
| **LLM** | ProxyAPI + GPT-4o-mini (автоматическое определение языка ответа) |
| **База данных** | SQLite, таблица `tickets` (хранит вход, результат, ошибки) |
| **Rate Limit** | До 10 запросов/мин на `client_id` |
| **Fallback** | При ошибке LLM → `escalate: true` + шаблонный ответ |
| **Docker** | Полная поддержка Docker Compose для VPS |

---

## ⚠️ Возможные проблемы

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError` | Убедитесь, что `.venv` активирован |
| `Connection refused` | Проверьте, запущен ли сервер (`docker compose ps`) |
| `429 Rate limit` | Подождите 1 минуту или измените `client_id` |
| `ProxyAPI key error` | Проверьте `.env`, ключ должен быть валидным |
| `Database locked` | Закрыть все соединения с БД и перезапустить |
