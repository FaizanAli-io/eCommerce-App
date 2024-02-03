from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

LOGIN_URL = reverse('user:login')
LOGOUT_URL = reverse('user:logout')
PROFILE_URL = reverse('user:profile')
REGISTER_URL = reverse('user:register')


class PublicUserAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user_payload = {
            'name': 'Base User',
            'email': 'base@example.com',
            'password': 'testpassword12345',
        }

    def test_create_user(self):
        res = self.client.post(REGISTER_URL, self.user_payload)
        user = get_user_model().objects.get(email=self.user_payload['email'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.name, self.user_payload['name'])
        self.assertEqual(user.email, self.user_payload['email'])
        self.assertTrue(user.check_password(self.user_payload['password']))
        self.assertNotIn('password', res.data)

    def test_duplicate_email_error(self):
        get_user_model().objects.create_user(**self.user_payload)
        res = self.client.post(REGISTER_URL, self.user_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        self.user_payload['password'] = '123'
        res = self.client.post(REGISTER_URL, self.user_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(
            email=self.user_payload['email']).exists())

    def test_create_token_good_creds(self):
        get_user_model().objects.create_user(**self.user_payload)
        res = self.client.post(LOGIN_URL, {
            'email': self.user_payload['email'],
            'password': self.user_payload['password'],
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_bad_creds(self):
        get_user_model().objects.create_user(**self.user_payload)
        res = self.client.post(LOGIN_URL, {
            'email': self.user_payload['email'],
            'password': 'incorrectpassword',
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_delete_token_unauthorized(self):
        get_user_model().objects.create_user(**self.user_payload)
        res = self.client.delete(LOGOUT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_unauthorized(self):
        get_user_model().objects.create_user(**self.user_payload)
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.auth_client = APIClient()
        self.user_password = 'testpass123'

        self.user = get_user_model().objects.create_user(
            name='Base User', email='base@example.com',
            password=self.user_password)

        self.auth_client.force_authenticate(user=self.user)

    def get_token_headers(self):
        token = self.client.post(LOGIN_URL, {
            'email': self.user.email,
            'password': self.user_password,
        }).data['token']

        return {'Authorization': f'Token {token}'}

    def test_delete_token(self):
        headers = self.get_token_headers()
        res_initial = self.client.get(PROFILE_URL, headers=headers)
        res_delete = self.client.delete(LOGOUT_URL, headers=headers)
        res_final = self.client.get(PROFILE_URL, headers=headers)

        self.assertEqual(res_initial.status_code, status.HTTP_200_OK)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res_final.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile(self):
        res = self.auth_client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
            'category': self.user.category,
        })

    def test_post_profile_not_allowed(self):
        res = self.auth_client.post(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_updating_user_profile(self):
        payload = {'name': 'New Name', 'password': 'newpass123'}
        res = self.auth_client.patch(PROFILE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
