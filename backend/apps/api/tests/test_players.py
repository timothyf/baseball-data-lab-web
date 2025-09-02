from unittest.mock import patch, call
from django.test import TestCase, Client

from apps.api.models import PlayerIdInfo


class PlayerHeadshotApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_player_headshot_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.fetch_player_headshot.return_value = b'image-bytes'

        PlayerIdInfo.objects.create(
            id=1,
            key_mlbam='123',
            name_first='Test',
            name_last='Player',
        )

        client = Client()
        response = client.get('/api/players/1/headshot/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'image-bytes')
        self.assertEqual(response['Content-Type'], 'image/png')
        mock_client.fetch_player_headshot.assert_called_once_with(123)

    @patch('apps.api.views.UnifiedDataClient')
    def test_player_headshot_endpoint_accepts_mlbam_id(self, mock_client_cls):
        """The endpoint should work when passed a raw MLBAM id."""
        mock_client = mock_client_cls.return_value
        mock_client.fetch_player_headshot.return_value = b'image-bytes'

        client = Client()
        response = client.get('/api/players/456/headshot/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'image-bytes')
        self.assertEqual(response['Content-Type'], 'image/png')
        mock_client.fetch_player_headshot.assert_called_once_with(456)


class PlayerInfoApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_player_info_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.fetch_player_info.return_value = {
            'currentTeam': {'id': 111, 'name': 'Team A'},
            'primaryPosition': {'name': 'Pitcher'},
            'birthDate': '1990-01-01',
            'birthCity': 'Some City',
            'birthStateProvince': 'CA',
            'birthCountry': 'USA',
            'height': "6'2\"",
            'weight': 200,
            'batSide': {'description': 'Right'},
            'pitchHand': {'description': 'Left'},
        }

        PlayerIdInfo.objects.create(
            id=1,
            key_mlbam='123',
            name_first='Test',
            name_last='Player',
        )

        client = Client()
        response = client.get('/api/players/1/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['team_id'], 111)
        self.assertEqual(data['team_name'], 'Team A')
        self.assertEqual(data['position'], 'Pitcher')
        self.assertEqual(data['birth_date'], '1990-01-01')
        self.assertEqual(data['birth_place'], 'Some City, CA, USA')
        self.assertEqual(data['height'], "6'2\"")
        self.assertEqual(data['weight'], 200)
        self.assertEqual(data['bat_side'], 'Right')
        self.assertEqual(data['throw_side'], 'Left')
        mock_client.fetch_player_info.assert_called_once_with(123)


class PlayerStatsApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_player_stats_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.fetch_player_stats_career.side_effect = [
            {'stats': ['bat']},
            {'stats': ['pitch']},
        ]

        PlayerIdInfo.objects.create(
            id=1,
            key_mlbam='123',
            name_first='Test',
            name_last='Player',
        )

        client = Client()
        response = client.get('/api/players/1/stats/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['batting']['stats'], ['bat'])
        self.assertEqual(data['pitching']['stats'], ['pitch'])
        mock_client.fetch_player_stats_career.assert_has_calls([
            call(123, group='hitting'),
            call(123, group='pitching'),
        ])


class PlayerSearchApiTests(TestCase):
    def setUp(self):
        for i in range(11):
            PlayerIdInfo.objects.create(
                name_first='Test',
                name_last=f'Player{i}',
                key_mlbam=str(100 + i),
            )
        PlayerIdInfo.objects.create(
            name_first='Foo',
            name_last='Bar',
            key_mlbam='123.0',
        )

    def test_player_search_case_insensitive_and_limited(self):
        client = Client()
        response = client.get('/api/players/', {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 10)
        self.assertTrue(all('Test Player' in p['name_full'] for p in data))

        response = client.get('/api/players/', {'q': 'foo'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['key_mlbam'], '123')
