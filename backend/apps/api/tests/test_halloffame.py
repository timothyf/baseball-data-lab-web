from django.test import TestCase, Client

from apps.api.models import HallOfFameVote, PlayerIdInfo


class HallOfFamePlayersApiTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='localhost')

    def test_returns_inducted_players_with_mlbam_ids(self):
        HallOfFameVote.objects.create(bbref_id='ruthba01', year=1936, inducted=True, category='Player')
        HallOfFameVote.objects.create(bbref_id='doejo01', year=2000, inducted=True, category='Player')
        HallOfFameVote.objects.create(bbref_id='notind01', year=1990, inducted=False, category='Player')
        HallOfFameVote.objects.create(bbref_id='manager01', year=1988, inducted=True, category='Manager')

        PlayerIdInfo.objects.create(
            key_bbref='ruthba01', key_mlbam='12345', name_first='Babe', name_last='Ruth'
        )
        PlayerIdInfo.objects.create(
            key_bbref='doejo01', name_first='John', name_last='Doe'
        )

        response = self.client.get('/api/players/halloffame/')
        self.assertEqual(response.status_code, 200)
        players = response.json()['players']

        self.assertEqual(len(players), 2)
        self.assertIn(
            {
                'bbref_id': 'ruthba01',
                'year': 1936,
                'mlbam_id': '12345',
                'name': 'Babe Ruth',
                'first_name': 'Babe',
                'last_name': 'Ruth',
            },
            players,
        )
        self.assertIn(
            {
                'bbref_id': 'doejo01',
                'year': 2000,
                'mlbam_id': None,
                'name': 'John Doe',
                'first_name': 'John',
                'last_name': 'Doe',
            },
            players,
        )
