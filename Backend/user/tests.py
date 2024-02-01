from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

LIST_CREATE_URL = reverse('consumer:list')
PROFILE_URL = reverse('consumer:profile')
TOKEN_URL = reverse('consumer:token')


class PublicUserAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user_payload = {
            'name': 'Base User',
            'email': 'base@example.com',
            'password': 'testpass123',
        }

    def test_create_user(self):
        res = self.client.post(LIST_CREATE_URL, self.user_payload)
        user = get_user_model().objects.get(email=self.user_payload['email'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(self.user_payload['password']))
        self.assertNotIn('password', res.data)

    def test_duplicate_email_error(self):
        get_user_model().objects.create_user(**self.user_payload)
        res = self.client.post(LIST_CREATE_URL, self.user_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        self.user_payload['password'] = '123'
        res = self.client.post(LIST_CREATE_URL, self.user_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(
            email=self.user_payload['email']).exists())

    def test_token_good_creds(self):
        get_user_model().objects.create_user(**self.user_payload)
        res = self.client.post(TOKEN_URL, {
            'email': self.user_payload['email'],
            'password': self.user_payload['password'],
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_token_bad_creds(self):
        get_user_model().objects.create_user(**self.user_payload)
        res = self.client.post(TOKEN_URL, {
            'email': self.user_payload['email'],
            'password': 'incorrectpassword',
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)


class PrivateUserAPITests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            name='Base User',
            email='base@example.com',
            password='testpass123',
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_profile_not_allowed(self):
        res = self.client.post(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_updating_user_profile(self):
        payload = {'name': 'New Name', 'password': 'newpass123'}
        res = self.client.patch(PROFILE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
