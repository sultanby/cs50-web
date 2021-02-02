from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from .models import User, Post, ProfileFollows

class ModelTest(TestCase):
    def setUp(self):
        # Create test user.
        test_user = User.objects.create_user(
            username='a',
            password='a',
            email='a@ex.com',
        )
        self.c = Client()

    def test_GET_login_correct_redirection(self):
        """ Check redirection to index for logged users """
        # Login user
        self.c.login(username='a', password="a")
        # Get the response
        response = self.c.get('/login')
        # Check redirect status code and redirection url
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_POST_login_correct_redirection(self):
        """ Check redirection to index for logged users """
        # Login user
        self.c.login(username='a', password="a")
        # Get the responses
        response = self.c.post('/login')
        # Check redirect status code and redirection url
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
