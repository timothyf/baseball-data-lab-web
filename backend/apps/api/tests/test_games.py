from unittest.mock import patch
from django.test import TestCase, Client
import pytest


class GameDataApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_game_data_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.fetch_game_live_feed.return_value = {
            'gameData': {
                'teams': {
                    'home': {
                        'id': 1,
                        'name': 'Home',
                        'score': 5
                    },
                    'away': {
                        'id': 2,
                        'name': 'Away',
                        'score': 3
                    },
                    'liveData': {
                        'boxscore': {'info': [{'label': 'Att', 'value': '10,000'}]}
                    }
                }
            }
        }
        mock_client.fetch_team_spot_url.return_value = 'logo-url'
        client = Client()
        response = client.get('/api/games/123/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['gameData']['teams']['home']['name'], 'Home')
        self.assertEqual(data['gameData']['teams']['away']['score'], 3)
        # self.assertEqual(
        #     data['liveData']['boxscore']['info'][0]['label'],
        #     'Att',
        # )
