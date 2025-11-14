from __future__ import annotations
from ..models import Show, Subscription
from . import rss_service, download_service
from .notification_service import notify_user_new_episode


def run_daily_check():
    print('Starting daily RSS check...')
    shows = Show.objects.filter(is_active=True)
    for show in shows:
        print(f'Checking show: {show.title}')
        new_episodes = rss_service.sync_episodes_for_show(show)
        if not new_episodes:
            continue
        subscriptions = Subscription.objects.filter(show=show).select_related('user')
        for episode in new_episodes:
            try:
                if not episode.is_downloaded:
                    download_service.download_episode_file(episode)
            except Exception as exc:  # pragma: no cover
                print(f'Failed to download episode {episode.id}: {exc}')
            for subscription in subscriptions:
                notify_user_new_episode(subscription.user, episode)
                subscription.last_notified_episode = episode
                subscription.save(update_fields=['last_notified_episode'])
    print('Daily RSS check completed.')
