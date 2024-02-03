from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product
from .serializers import ProductSerializer

userModel = get_user_model()

LIST_CREATE_URL = reverse('product:product-list')


def get_detail_url(product_id):
    return reverse('product:product-detail', args=[product_id])


def get_test_product(user):
    return Product.objects.create(
        user=user,
        name='Test Item',
        price=0.99, stock=1,
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
        product = get_test_product(self.user)
        detail_url = get_detail_url(product.id)

        get_res = self.client.get(detail_url)
        put_res = self.client.put(detail_url)
        patch_res = self.client.patch(detail_url)
        delete_res = self.client.delete(detail_url)

        self.assertEqual(get_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(put_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(patch_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    def setUp(self):
        self.consumer_client = APIClient()
        self.vendor_client = APIClient()

        self.consumer = userModel.objects.create_user(
            name='Test Consumer',
            email='consumer@example.com',
            password='consumerpassword123',
            category=userModel.UserCategory.CONSUMER,
        )

        self.vendor = userModel.objects.create_user(
            name='Test Vendor',
            email='vendor@example.com',
            password='vendorpassword123',
            category=userModel.UserCategory.VENDOR,
        )

        self.consumer_client.force_authenticate(self.consumer)
        self.vendor_client.force_authenticate(self.vendor)

    def test_create_as_consumer(self):
        res = self.vendor_client.post(LIST_CREATE_URL, {
            'user': self.consumer,
            'name': 'Consumer Test',
            'stock': 0, 'price': 0,
        })

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user'], self.vendor.name)

    def test_get_product_list(self):
        get_test_product(self.vendor)
        products = Product.objects.all()
        con_res = self.consumer_client.get(LIST_CREATE_URL)
        ven_res = self.vendor_client.get(LIST_CREATE_URL)
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(con_res.status_code, status.HTTP_200_OK)
        self.assertEqual(ven_res.status_code, status.HTTP_200_OK)
        self.assertEqual(con_res.data, serializer.data)
        self.assertEqual(ven_res.data, serializer.data)

    def test_create_product_list(self):

        payload = {'name': 'Vendor Item',
                   'price': 0.99, 'stock': 1}

        con_res = self.consumer_client.post(LIST_CREATE_URL, payload)
        ven_res = self.vendor_client.post(LIST_CREATE_URL, payload)

        self.assertEqual(con_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(ven_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ven_res.data['user'], self.vendor.name)
        self.assertEqual(ven_res.data['name'], payload['name'])
        self.assertEqual(ven_res.data['price'], payload['price'])
        self.assertEqual(ven_res.data['stock'], payload['stock'])

    def test_get_product(self):
        product = get_test_product(self.vendor)
        detail_url = get_detail_url(product.id)
        con_res = self.consumer_client.get(detail_url)
        ven_res = self.vendor_client.get(detail_url)
        serializer = ProductSerializer(product)

        self.assertEqual(con_res.status_code, status.HTTP_200_OK)
        self.assertEqual(ven_res.status_code, status.HTTP_200_OK)
        self.assertEqual(con_res.data, serializer.data)
        self.assertEqual(ven_res.data, serializer.data)

    def test_partial_update_product(self):
        product1 = get_test_product(self.vendor)
        product2 = get_test_product(self.vendor)
        detail_url1 = get_detail_url(product1.id)
        detail_url2 = get_detail_url(product2.id)
        payload = {'name': 'Updated Name'}

        con_res = self.consumer_client.patch(detail_url1, payload)
        ven_res = self.vendor_client.patch(detail_url2, payload)
        patched_product1 = Product.objects.get(id=product1.id)
        patched_product2 = Product.objects.get(id=product2.id)

        self.assertEqual(con_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(ven_res.status_code, status.HTTP_200_OK)
        self.assertEqual(patched_product1.name, product1.name)
        self.assertEqual(patched_product2.name, payload['name'])

    def test_complete_update_product(self):
        product1 = get_test_product(self.vendor)
        product2 = get_test_product(self.vendor)
        detail_url1 = get_detail_url(product1.id)
        detail_url2 = get_detail_url(product2.id)

        payload = {
            'name': 'Updated Name',
            'price': 1.99, 'stock': 2,
        }

        con_res = self.consumer_client.put(detail_url1, payload)
        ven_res = self.vendor_client.put(detail_url2, payload)
        updated_product1 = Product.objects.get(id=product1.id)
        product2.refresh_from_db()

        self.assertEqual(con_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(ven_res.status_code, status.HTTP_200_OK)
        self.assertEqual(product2.user, self.vendor)
        self.assertEqual(product2.name, payload['name'])
        self.assertEqual(product2.price, payload['price'])
        self.assertEqual(product2.stock, payload['stock'])
        self.assertEqual(
            ProductSerializer(product1).data,
            ProductSerializer(updated_product1).data,
        )

    def test_delete_product(self):
        product1 = get_test_product(self.vendor)
        product2 = get_test_product(self.vendor)

        con_res = self.consumer_client.delete(get_detail_url(product1.id))
        ven_res = self.vendor_client.delete(get_detail_url(product2.id))

        product1_exists = Product.objects.filter(id=product1.id).exists()
        product2_exists = Product.objects.filter(id=product2.id).exists()

        self.assertEqual(con_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(ven_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(product1_exists)
        self.assertFalse(product2_exists)
