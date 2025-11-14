from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Show, Episode, Subscription
from ..services import rss_service


class ModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='alice', password='password')

    def test_create_show_episode_subscription(self):
        show = Show.objects.create(owner=self.user, title='Test Show', rss_url='http://example.com/rss')
        episode = Episode.objects.create(show=show, guid='guid-1', title='Ep1', download_url='http://example.com/ep1')
        subscription = Subscription.objects.create(user=self.user, show=show)
        self.assertEqual(Show.objects.count(), 1)
        self.assertEqual(Episode.objects.count(), 1)
        self.assertEqual(Subscription.objects.count(), 1)

    def test_sync_creates_new_episodes(self):
        show = Show.objects.create(owner=self.user, title='Test', rss_url='http://example.com/rss')

        def fake_fetch(show):
            return [
                {'guid': 'a', 'title': 'EpA', 'published': None, 'download_url': 'http://example.com/a'},
                {'guid': 'b', 'title': 'EpB', 'published': None, 'download_url': 'http://example.com/b'},
            ]
        original = rss_service.fetch_episodes_for_show
        rss_service.fetch_episodes_for_show = fake_fetch
        try:
            episodes = rss_service.sync_episodes_for_show(show)
            self.assertEqual(len(episodes), 2)
            episodes = rss_service.sync_episodes_for_show(show)
            self.assertEqual(len(episodes), 0)
        finally:
            rss_service.fetch_episodes_for_show = original
