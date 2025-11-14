from __future__ import annotations
from typing import List, Dict
from datetime import datetime
import feedparser
from django.utils import timezone

from tracker.models import Show, Episode


def fetch_episodes_for_show(show: Show) -> List[Dict]:
    feed = feedparser.parse(show.rss_url)
    episodes = []
    for entry in feed.entries:
        guid = getattr(entry, 'id', None) or getattr(entry, 'guid', None) or entry.get('link')
        if not guid:
            continue
        enclosure = entry.enclosures[0]['href'] if getattr(entry, 'enclosures', None) else entry.get('link', show.rss_url)
        published = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6])
        episodes.append({
            'guid': guid,
            'title': entry.get('title', 'Untitled'),
            'published': published,
            'download_url': enclosure,
        })
    return episodes


def sync_episodes_for_show(show: Show) -> List[Episode]:
    parsed_entries = fetch_episodes_for_show(show)
    new_episodes = []
    for entry in parsed_entries:
        if Episode.objects.filter(guid=entry['guid']).exists():
            continue
        published_at = entry['published']
        if published_at and timezone.is_naive(published_at):
            published_at = timezone.make_aware(published_at, timezone.get_current_timezone())
        episode = Episode.objects.create(
            show=show,
            guid=entry['guid'],
            title=entry['title'],
            published_at=published_at,
            download_url=entry['download_url'],
        )
        new_episodes.append(episode)
    show.last_checked_at = timezone.now()
    show.save(update_fields=['last_checked_at'])
    return new_episodes
