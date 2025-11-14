from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tracker.models import Show


class ViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='bob', password='password')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_create_show(self):
        self.client.login(username='bob', password='password')
        payload = {
            'title': 'My Show',
            'original_title': '',
            'rss_url': 'http://example.com/rss',
            'image_url': '',
            'is_active': 'on',
        }
        response = self.client.post(reverse('add_show'), payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Show.objects.count(), 1)
