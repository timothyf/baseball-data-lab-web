from unittest.mock import patch
from django.test import TestCase, Client
import pytest


class GameDataApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_game_data_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.fetch_game_live_feed.return_value = {
            'teams': {
                'home': {'team': {'name': 'Home'}, 'score': 5},
                'away': {'team': {'name': 'Away'}, 'score': 3},
            },
            'home_team_data': {'id': 1},
            'away_team_data': {'id': 2},
            'liveData': {
                'boxscore': {'info': [{'label': 'Att', 'value': '10,000'}]}
            },
        }
        mock_client.fetch_team_spot_url.return_value = 'logo-url'
        client = Client()
        response = client.get('/api/games/123/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['teams']['home']['team']['name'], 'Home')
        self.assertEqual(data['teams']['away']['score'], 3)
        self.assertEqual(
            data['liveData']['boxscore']['info'][0]['label'],
            'Att',
        )
