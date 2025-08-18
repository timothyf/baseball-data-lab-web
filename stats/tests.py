from django.test import TestCase, Client

class HomeViewTests(TestCase):
    def test_home_view(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hello-component')
