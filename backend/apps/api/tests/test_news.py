from django.test import TestCase, Client


class NewsApiTests(TestCase):
    def test_news_endpoint(self):
        client = Client()
        response = client.get('/api/news/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertIn('title', data[0])
