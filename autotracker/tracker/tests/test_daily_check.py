from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest import mock

from tracker.models import Show, Subscription, Episode
from tracker.services import daily_check


class DailyCheckTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='eve', password='password')
        self.show = Show.objects.create(owner=self.user, title='Daily', rss_url='http://example.com/rss')
        Subscription.objects.create(user=self.user, show=self.show)

    @mock.patch('tracker.services.daily_check.download_service.download_episode_file')
    @mock.patch('tracker.services.daily_check.notify_user_new_episode')
    @mock.patch('tracker.services.daily_check.rss_service.sync_episodes_for_show')
    def test_run_daily_check_notifies(self, mock_sync, mock_notify, mock_download):
        episode = Episode.objects.create(show=self.show, guid='x', title='Ep', download_url='http://example.com/x')
        mock_sync.return_value = [episode]

        daily_check.run_daily_check()

        mock_sync.assert_called_once_with(self.show)
        mock_download.assert_called_once_with(episode)
        mock_notify.assert_called_once()
