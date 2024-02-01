from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product, Vendor
from market.serializers import ProductSerializer

LIST_CREATE_URL = reverse('market:product-list')


def get_detail_url(obj_id):
    return reverse('market:product-detail', args=obj_id)


def create_object(name, seller, **params):
    return Product.objects.create(
        name=name, seller=seller,
        desc=params['desc'] if 'desc' in params else "",
        stock=params['stock'] if 'stock' in params else 0,
        price=params['price'] if 'price' in params else 0,
    )


class ProductAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name='Test Vendor')

    def test_create_successful(self):
        payload = {
            'seller': self.vendor.id,
            'name': "Test Product",
            'stock': 0, 'price': 0,
        }
        res = self.client.post(LIST_CREATE_URL, payload)
        obj = Product.objects.get(name=res.data['name'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for k, v in payload.items():
            if k == 'seller':
                self.assertEqual(getattr(obj, k).id, v)
            else:
                self.assertEqual(getattr(obj, k), v)

    def test_retrieve_successful(self):
        create_object("Product 1", self.vendor)
        create_object("Product 2", self.vendor)
        res = self.client.get(LIST_CREATE_URL)
        serializer = ProductSerializer(
            Product.objects.order_by('name'), many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
