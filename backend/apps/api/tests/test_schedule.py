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
        # The production code calls ``get_team_spot_url`` to obtain a team's
        # logo.  The previous version of this test patched the non-existent
        # ``fetch_team_spot_url`` method which left a ``MagicMock`` object in
        # the response and caused the test client to hang during JSON
        # serialisation.  Patch the correct method so a simple string is
        # injected into the response data.
        mock_client.get_team_spot_url.return_value = 'logo-url'

        response = self.client.get('/api/schedule/', {'date': '2025-08-18'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        game = data[0]['games'][0]
        self.assertEqual(game['teams']['home']['team']['logo_url'], 'logo-url')
        self.assertEqual(game['teams']['away']['team']['logo_url'], 'logo-url')
