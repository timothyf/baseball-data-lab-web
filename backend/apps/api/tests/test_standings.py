from unittest.mock import patch
from django.test import TestCase, Client


class StandingsApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_standings_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.fetch_standings_data.return_value = {
            'records': [
                {
                    'league': {'name': 'American League'},
                    'division': {'name': 'East'},
                    'teamRecords': [
                        {'team': {'id': 1, 'name': 'Team A'}, 'wins': 10, 'losses': 5},
                        {'team': {'id': 2, 'name': 'Team B'}, 'wins': 8, 'losses': 7},
                    ],
                }
            ]
        }
        client = Client()
        response = client.get('/api/standings/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('records', data)
        self.assertEqual(len(data['records'][0]['teamRecords']), 2)
