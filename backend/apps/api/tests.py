from unittest.mock import patch
from django.test import TestCase, Client

from apps.api.models import PlayerIdInfo, TeamIdInfo


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


class GameDataApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_game_data_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.get_game_data.return_value = {
            'teams': {
                'home': {'team': {'name': 'Home'}, 'score': 5},
                'away': {'team': {'name': 'Away'}, 'score': 3},
            },
            'home_team_data': {'id': 1},
            'away_team_data': {'id': 2},
        }
        mock_client.get_team_spot_url.return_value = 'logo-url'
        mock_client.get_game_boxscore_data.return_value = {
            'info': [{'label': 'Att', 'value': '10,000'}]
        }
        client = Client()
        response = client.get('/api/games/123/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['teams']['home']['team']['name'], 'Home')
        self.assertEqual(data['teams']['away']['score'], 3)
        # boxscore data should be merged into liveData
        self.assertEqual(
            data['liveData']['boxscore']['info'][0]['label'],
            'Att',
        )
        mock_client.get_game_boxscore_data.assert_called_once_with(123)


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


class NewsApiTests(TestCase):
    def test_news_endpoint(self):
        client = Client()
        response = client.get('/api/news/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertIn('title', data[0])


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


class PlayerSearchApiTests(TestCase):
    def setUp(self):
        # Create more than 10 players to ensure the limit works
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
        # Case-insensitive search and limit
        response = client.get('/api/players/', {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 10)
        self.assertTrue(all('Test Player' in p['name_full'] for p in data))

        # Ensure key_mlbam is sanitized and search is case-insensitive
        response = client.get('/api/players/', {'q': 'foo'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['key_mlbam'], '123')


class TeamSearchApiTests(TestCase):
    def setUp(self):
        TeamIdInfo.objects.create(id=1, full_name='Red Sox', mlbam_team_id=111)
        TeamIdInfo.objects.create(id=2, full_name='Blue Jays', mlbam_team_id=222)

    def test_team_search_returns_results(self):
        client = Client()
        response = client.get('/api/teams/', {'q': 'red'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['full_name'], 'Red Sox')
        self.assertEqual(data[0]['mlbam_team_id'], '111')


class TeamInfoApiTests(TestCase):
    def setUp(self):
        TeamIdInfo.objects.create(id=1, full_name='Red Sox', mlbam_team_id=111)

    def test_team_info_returns_team(self):
        client = Client()
        response = client.get('/api/teams/111/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['full_name'], 'Red Sox')
        self.assertEqual(data['mlbam_team_id'], '111')

    def test_team_info_not_found(self):
        client = Client()
        response = client.get('/api/teams/999/')
        self.assertEqual(response.status_code, 404)


class TeamLogoApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_team_logo_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.get_team_logo_url.return_value = 'logo-url'

        TeamIdInfo.objects.create(id=1, mlbam_team_id=555, full_name='Team A')

        client = Client()
        response = client.get('/api/teams/1/logo/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'logo-url')
        self.assertEqual(response['Content-Type'], 'text/plain')
        mock_client.get_team_logo_url.assert_called_once_with(555)


class TeamRecordApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_team_record_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.get_team_record_for_season.return_value = {
            'wins': 10,
            'losses': 5,
            'divisionRank': '1',
            'streak': {
                'streakType': 'wins',
                'streakNumber': 3,
                'streakCode': 'W3'
            }
        }

        TeamIdInfo.objects.create(id=1, mlbam_team_id=555, full_name='Team A')

        client = Client()
        response = client.get('/api/teams/1/record/', {'season': '2025'})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['wins'], 10)
        mock_client.get_team_record_for_season.assert_called_once_with(555, 2025)


class TeamRecentScheduleApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_team_recent_schedule_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.get_recent_schedule_for_team.return_value = {
            'id': 555,
            'previousGameSchedule': {'dates': []},
            'nextGameSchedule': {'dates': []}
        }

        TeamIdInfo.objects.create(id=1, mlbam_team_id=555, full_name='Team A')

        client = Client()
        response = client.get('/api/teams/1/recent_schedule/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], 555)
        mock_client.get_recent_schedule_for_team.assert_called_once_with(555)

    def test_team_recent_schedule_team_not_found(self):
        client = Client()
        response = client.get('/api/teams/1/recent_schedule/')
        self.assertEqual(response.status_code, 404)


class TeamRosterApiTests(TestCase):
    @patch('apps.api.views.UnifiedDataClient')
    def test_team_roster_endpoint(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.get_team_roster.return_value = {
            'roster': [
                {
                    'id': 1,
                    'fullName': 'Test Player',
                    'primaryPosition': {'abbreviation': 'P'},
                    'stats': {'gamesPlayed': 10},
                }
            ]
        }

        TeamIdInfo.objects.create(id=1, mlbam_team_id=555, full_name='Team A')

        client = Client()
        response = client.get('/api/teams/1/roster/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['roster']), 1)
        mock_client.get_team_roster.assert_called_once_with(555)

    def test_team_roster_team_not_found(self):
        client = Client()
        response = client.get('/api/teams/1/roster/')
        self.assertEqual(response.status_code, 404)
