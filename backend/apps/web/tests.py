from unittest.mock import patch
from django.test import TestCase, Client


class HomeViewTests(TestCase):
    @patch('apps.web.views.UnifiedDataClient')
    def test_home_view(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.get_schedule_for_date_range.return_value = [
            {
                'games': [
                    {
                        'gameDate': '2025-08-18T18:20:00Z',
                        'teams': {
                            'away': {'team': {'name': 'Away Team', 'id': 1}},
                            'home': {'team': {'name': 'Home Team', 'id': 2}},
                        },
                    }
                ]
            }
        ]
        mock_client.get_team_spot_url.return_value = 'logo-url'
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'schedule-data')
        self.assertContains(response, 'id="vue-app"')
        self.assertContains(response, 'Away Team')
        self.assertContains(response, 'Home Team')
        self.assertContains(response, 'logo-url')
