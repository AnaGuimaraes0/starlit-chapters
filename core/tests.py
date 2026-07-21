from django.test import TestCase
from django.urls import reverse


class CoreViewsTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_biblioteca_page_loads(self):
        response = self.client.get(reverse('biblioteca'))
        self.assertEqual(response.status_code, 200)

    def test_recommendations_page_loads(self):
        response = self.client.get(reverse('recomendacoes'))
        self.assertEqual(response.status_code, 200)
