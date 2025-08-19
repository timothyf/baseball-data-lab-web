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
                            'away': {'team': {'name': 'Away Team'}},
                            'home': {'team': {'name': 'Home Team'}},
                        },
                    }
                ]
            }
        ]
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'schedule-data')
        self.assertContains(response, 'id="vue-app"')
        self.assertContains(response, 'Away Team')
        self.assertContains(response, 'Home Team')
