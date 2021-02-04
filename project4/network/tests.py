from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from .models import User, Post, ProfileFollows
import json


class ModelTest(TestCase):
    def setUp(self):
        # Create test user.
        test_user = User.objects.create_user(
            username='a',
            password='a',
            email='a@ex.com',
        )
        self.c = Client()

    def test_GET_login_correct_status_code(self):
        """ Check redirection to index for logged users """
        # Get the responses
        response = self.c.get('/login', {'username': 'a', 'password': 'a'})
        # Check redirect status code and redirection url
        self.assertEqual(response.status_code, 200)

    def test_POST_login_no_user_status_code(self):
        """ Check redirection to index for logged users """
        # Get the responses
        response = self.c.post('/login', {'username': '', 'password': ''})
        # Check redirect status code
        self.assertEqual(response.status_code, 403)


    def test_logout_logged_user(self):
        """Test status code after logout"""
        # login
        self.c.login(username='a', password='a')
        # get request to logout
        response = self.c.get('/logout')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_login_wrong_password(self):
        """Test message trying to login with wrong password"""
        response = self.c.post('/login', {'username': 'a', 'password': '11'})

        self.assertEqual(response.context["message"], "Invalid username and/or password.")

    def test_new_post_wrong_call_returns_error(self):
        """Test error message trying to create new post via get request"""

        self.c.post('/login', {'username': 'a', 'password': 'a'})
        response = self.c.get('/post')
        #print(response)

        self.assertJSONEqual(response.content, {"error": "POST request required."})
        self.assertEqual(response.status_code, 400)

    def test_new_post_added_success(self):
        """Test message trying to create new post via post request"""

        self.c.post('/login', {'username': 'a', 'password': 'a'})
        request = {'new_post_text': 'new post'}
        response = self.c.post('/post', request)

        self.assertJSONEqual(response.content, {"message": "Post added successfully."})
        self.assertEqual(response.status_code, 201)

