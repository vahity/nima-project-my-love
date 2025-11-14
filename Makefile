.PHONY: venv migrate run test worker

venv:
python -m venv venv
./venv/bin/pip install -r requirements.txt

migrate:
./venv/bin/python manage.py migrate

run:
./venv/bin/python manage.py runserver

test:
./venv/bin/python manage.py test

worker:
./venv/bin/python rss_worker.py
