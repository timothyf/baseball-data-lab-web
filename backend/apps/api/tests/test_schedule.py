from unittest.mock import patch
from django.test import TestCase, Client


class ScheduleApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_schedule_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.fetch_schedule_for_date_range.return_value = [
            {
                'date': '2025-08-18',
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
        mock_client.fetch_team_spot_url.return_value = 'logo-url'
        client = Client()
        response = client.get('/api/schedule/', {'date': '2025-08-18'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        game = data[0]['games'][0]
        self.assertEqual(game['teams']['home']['team']['logo_url'], 'logo-url')
        self.assertEqual(game['teams']['away']['team']['logo_url'], 'logo-url')
