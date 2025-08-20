from unittest.mock import patch
from django.test import TestCase, Client
from django.db import connection


class ScheduleApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_schedule_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.get_schedule_for_date_range.return_value = [
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
        mock_client.get_team_spot_url.return_value = 'logo-url'
        client = Client()
        response = client.get('/api/schedule/', {'date': '2025-08-18'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        game = data[0]['games'][0]
        self.assertEqual(game['teams']['home']['team']['logo_url'], 'logo-url')
        self.assertEqual(game['teams']['away']['team']['logo_url'], 'logo-url')


class StandingsApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_standings_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.get_standings_data.return_value = {
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


class PlayerHeadshotApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_player_headshot_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.fetch_player_headshot.return_value = b'image-bytes'

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO player_id_infos (id, key_mlbam, name_first, name_last) VALUES (%s, %s, %s, %s)",
                [1, '123', 'Test', 'Player'],
            )

        client = Client()
        response = client.get('/api/players/1/headshot/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'image-bytes')
        self.assertEqual(response['Content-Type'], 'image/png')
        mock_client.fetch_player_headshot.assert_called_once_with(123)
