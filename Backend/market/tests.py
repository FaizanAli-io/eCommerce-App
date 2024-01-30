from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

LIST_VENDOR_URL = reverse('market:vendor-list')
LIST_PRODUCT_URL = reverse('market:product-list')
DETAIL_VENDOR_URL = reverse('market:vendor-detail', args=[0])
DETAIL_PRODUCT_URL = reverse('market:product-detail', args=[0])


class PublicUserAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
