# AutoTracker

AutoTracker is a minimal Django web application that lets users subscribe to their favourite TV series or anime RSS feeds. It automatically downloads new episodes and sends SMS notifications via a pluggable gateway. The included scheduler (`rss_worker.py`) runs daily checks and notifies each subscriber when new content arrives.

## Features
- User registration, login, and personal dashboard
- Add shows with RSS feeds and track download state per episode
- Daily RSS synchronisation and automated downloads
- Console-based SMS gateway abstraction ready for real-world providers
- Clean Bootstrap 5 interface and comprehensive unit tests

## Requirements
- Python 3.11+
- MySQL server (8.x recommended)
- Virtual environment tool such as `venv`

## Setup
1. **Clone the repository and create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Create the environment file**
   ```bash
   cp .env.example .env
   ```
   Update the values for your MySQL credentials and SMS gateway secrets. The Django settings read these values automatically using `python-dotenv`.

3. **Configure MySQL**
   ```sql
   CREATE DATABASE autotracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'autotracker'@'localhost' IDENTIFIED BY 'strong-password';
   GRANT ALL PRIVILEGES ON autotracker.* TO 'autotracker'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Run migrations and create a superuser**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   Visit http://127.0.0.1:8000/ to register and start adding shows.

6. **Run the RSS worker**
   In a separate terminal keep the scheduler running:
   ```bash
   python rss_worker.py
   ```
   It will call the daily check every day at 04:00 server time.

7. **Run tests**
   ```bash
   python manage.py test
   ```

## Makefile (optional)
If you prefer `make`, you can create the following targets:

```makefile
venv:
python -m venv venv
source venv/bin/activate && pip install -r requirements.txt

migrate:
source venv/bin/activate && python manage.py migrate

run:
source venv/bin/activate && python manage.py runserver

test:
source venv/bin/activate && python manage.py test

worker:
source venv/bin/activate && python rss_worker.py
```

Feel free to adapt the scheduler to a production-grade task runner (e.g., systemd or a container-based cron job).
