from unittest.mock import patch
from django.test import TestCase, Client

from apps.api.models import TeamIdInfo, Venue


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
        TeamIdInfo.objects.create(
            id=1,
            full_name='Red Sox',
            mlbam_team_id=111,
            location_name='Boston',
            abbrev='BOS'
        )
        Venue.objects.create(mlbam_id=10, name='Fenway Park', link='link', active=True, season=2024)

    @patch('apps.api.views.UnifiedDataClient')
    def test_team_info_returns_team(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.fetch_team.return_value = {'venue': {'id': 10}}

        client = Client()
        response = client.get('/api/teams/111/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['full_name'], 'Red Sox')
        self.assertEqual(data['mlbam_team_id'], '111')
        self.assertEqual(data['location_name'], 'Boston')
        self.assertEqual(data['abbrev'], 'BOS')
        self.assertEqual(data['venue_id'], '10')
        self.assertEqual(data['venue']['name'], 'Fenway Park')

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
        mock_client.fetch_recent_schedule_for_team.return_value = {
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
        mock_client.fetch_recent_schedule_for_team.assert_called_once_with(555)

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
