from unittest.mock import patch
from django.test import TestCase, Client


class LeagueLeadersApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_league_leaders_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value

        import pandas as pd

        bat_df = pd.DataFrame(
            {
                'xMLBAMID': [1, 2],
                'Name': ['<b>Player A</b>', 'Player B'],
                'PA': [100, 120],
                'HR': [10, 20],
                'AVG': [0.300, 0.350],
                'RBI': [30, 40],
                'SB': [5, 10],
                'SLG': [0.500, 0.600],
                'OPS': [0.800, 0.900],
            }
        )
        pit_df = pd.DataFrame(
            {
                'xMLBAMID': [3, 4],
                'Name': ['Pitcher C', 'Pitcher D'],
                'Pos': ['P', 'P'],
                'IP': [50, 60],
                'ERA': [2.5, 3.5],
                'SO': [100, 80],
                'W': [8, 10],
                'SV': [1, 5],
            }
        )

        mock_client.fetch_batting_leaderboards.return_value = bat_df
        mock_client.fetch_pitching_leaderboards.return_value = pit_df

        client = Client()
        response = client.get('/api/leaders/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('HR', data['batting'])
        self.assertEqual(data['batting']['HR'][0]['id'], '2')
        self.assertIn('ERA', data['pitching'])
        self.assertEqual(data['pitching']['ERA'][0]['id'], '3')
