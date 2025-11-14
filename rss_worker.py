import os
import sys
import time
from pathlib import Path

import django
import schedule

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autotracker.settings')
django.setup()

from tracker.services.daily_check import run_daily_check  # noqa: E402


def main():
    schedule.every().day.at('04:00').do(run_daily_check)
    print('RSS worker started. Waiting for scheduled tasks...')
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
