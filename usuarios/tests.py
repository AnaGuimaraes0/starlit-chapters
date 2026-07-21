from django.test import TestCase
from django.urls import reverse


class UsuariosUrlTests(TestCase):
    def test_home_url_name_exists(self):
        self.assertEqual(reverse('home'), '/')
