from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Product, ProductStock

userModel = get_user_model()

LIST_CREATE_URL = reverse('product:productstock-list')


def get_detail_url(product_id):
    return reverse('product:productstock-detail', args=[product_id])


def get_test_product(vendor):
    return ProductStock.objects.create(
        product=Product.objects.create(
            name="Test product",
            desc="Test description",
        ),
        vendor=vendor,
        stock=500,
        price=5.0,
    )


class PublicUserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = userModel.objects.create_user(
            name='Test User',
            email='test@example.com',
            password='testpassword123',
        )

    def test_list_create_fails(self):
        get_res = self.client.get(LIST_CREATE_URL)
        post_res = self.client.post(LIST_CREATE_URL)

        self.assertEqual(get_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(post_res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_detail_fails(self):
        stock_product = get_test_product(self.user)
        detail_url = get_detail_url(stock_product.id)

        get_res = self.client.get(detail_url)
        put_res = self.client.put(detail_url)
        patch_res = self.client.patch(detail_url)
        delete_res = self.client.delete(detail_url)

        self.assertEqual(get_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(put_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(patch_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_res.status_code, status.HTTP_401_UNAUTHORIZED)


class ConsumerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = userModel.objects.create_user(
            name='Test Consumer',
            email='consumer@example.com',
            password='consumerpassword123',
            category=userModel.UserCategory.CONSUMER,
        )

        self.client.force_authenticate(self.user)

    def test_create_product(self):
        payload = {
            "product": {
                "name": "Test Product",
                "desc": "A product test",
            },
            "stock": 250,
            "price": 2.5,
        }

        res = self.client.post(LIST_CREATE_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_product(self):
        stock_product = get_test_product(self.user)
        res = self.client.get(LIST_CREATE_URL)
        data = res.data[0]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['vendor']['id'], self.user.id)
        self.assertEqual(data['stock'], stock_product.stock)
        self.assertEqual(data['price'], stock_product.price)

        self.assertEqual(
            data['product']['name'],
            stock_product.product.name,
        )

        self.assertEqual(
            data['product']['desc'],
            stock_product.product.desc,
        )

    def test_partial_update_product(self):
        stock_product = get_test_product(self.user)
        detail_url = get_detail_url(stock_product.id)

        payload = {
            'product': {
                'name': 'Updated Stock Name',
            },
            'stock': 250,
        }

        res = self.client.patch(detail_url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_complete_update_product(self):
        stock_product = get_test_product(self.user)
        detail_url = get_detail_url(stock_product.id)

        payload = {
            "product": {
                "name": "Updated Test Product",
                "desc": "An updated product test",
            },
            "stock": 250,
            "price": 2.5,
        }

        res = self.client.put(detail_url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product(self):
        stock_product = get_test_product(self.user)
        detail_url = get_detail_url(stock_product.id)
        res = self.client.delete(detail_url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class VendorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = userModel.objects.create_user(
            name='Test Vendor',
            email='vendor@example.com',
            password='vendorpassword123',
            category=userModel.UserCategory.VENDOR,
        )

        self.client.force_authenticate(self.user)

    def test_create_product(self):
        payload = {
            "product": {
                "name": "Test Product",
                "desc": "A product test",
            },
            "stock": 250,
            "price": 2.5,
        }

        res = self.client.post(LIST_CREATE_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['vendor']['id'], self.user.id)
        self.assertEqual(res.data['stock'], payload['stock'])
        self.assertEqual(res.data['price'], payload['price'])

        self.assertEqual(
            res.data['product']['name'],
            payload['product']['name'],
        )

        self.assertEqual(
            res.data['product']['desc'],
            payload['product']['desc'],
        )

    def test_get_product(self):
        stock_product = get_test_product(self.user)
        res = self.client.get(LIST_CREATE_URL)
        data = res.data[0]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['vendor']['id'], self.user.id)
        self.assertEqual(data['stock'], stock_product.stock)
        self.assertEqual(data['price'], stock_product.price)

        self.assertEqual(
            data['product']['name'],
            stock_product.product.name,
        )

        self.assertEqual(
            data['product']['desc'],
            stock_product.product.desc,
        )

    def test_partial_update_product(self):
        stock_product = get_test_product(self.user)
        detail_url = get_detail_url(stock_product.id)

        payload = {
            'product': {
                'name': 'Updated Stock Name',
            },
            'stock': 250,
        }

        res = self.client.patch(detail_url, payload, format="json")
        stock_product.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(stock_product.stock, payload['stock'])

        self.assertEqual(
            stock_product.product.name,
            payload['product']['name'],
        )

    def test_complete_update_product(self):
        stock_product = get_test_product(self.user)
        detail_url = get_detail_url(stock_product.id)

        payload = {
            "product": {
                "name": "Updated Test Product",
                "desc": "An updated product test",
            },
            "stock": 250,
            "price": 2.5,
        }

        res = self.client.put(detail_url, payload, format="json")
        stock_product.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(stock_product.vendor, self.user)
        self.assertEqual(stock_product.stock, payload['stock'])
        self.assertEqual(stock_product.price, payload['price'])

        self.assertEqual(
            stock_product.product.name,
            payload['product']['name'],
        )

        self.assertEqual(
            stock_product.product.desc,
            payload['product']['desc'],
        )

    def test_delete_product(self):
        stock_product = get_test_product(self.user)
        detail_url = get_detail_url(stock_product.id)
        res = self.client.delete(detail_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProductStock.objects.filter(
            id=stock_product.id).exists())
