from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

LIST_USER_URL = reverse('user:consumer-list')
DETAIL_USER_URL = reverse('user:consumer-detail', args=[0])


class PublicUserAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
