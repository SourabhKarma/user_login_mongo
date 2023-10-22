from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser  # Import your User model

class CreateUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_success(self):
        url = '/create_user/'
        data = {
            'phone_number': 'user123',
            'password': 'secure_password',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('auth_token', response.data)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_user_registration_existing_user(self):
        # Create a user with the same phone number before the test
        CustomUser.objects.create(phone_number='user123', password='hashed_password')

        url = '/create_user/'
        data = {
            'phone_number': 'user123',
            'password': 'secure_password',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('User with this phone number already exists', response.data)

    def test_user_registration_missing_fields(self):
        url = '/create_user/'
        data = {
            'phone_number': 'user123',
            # Password field is missing
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Please provide both phone number and password', response.data['error'])

    def test_user_registration_invalid_password(self):
        url = '/create_user/'
        data = {
            'phone_number': 'user123',
            'password': 'weak',  # Password is too weak
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Password must meet the requirements', response.data['error'])

    def test_user_registration_internal_server_error(self):
        # Simulate an internal server error in your view
        url = '/create_user/'
        data = {
            'phone_number': 'user123',
            'password': 'secure_password',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('Failed to create user', response.data['error'])
