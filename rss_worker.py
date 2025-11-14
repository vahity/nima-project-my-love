import os
import django
import schedule
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autotracker.settings')
django.setup()

from autotracker.tracker.services.daily_check import run_daily_check  # noqa: E402


def main():
    schedule.every().day.at('04:00').do(run_daily_check)
    print('RSS worker started. Waiting for scheduled tasks...')
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
