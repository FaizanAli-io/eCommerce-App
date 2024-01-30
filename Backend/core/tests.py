from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model


from .models import (
    Product,
    Vendor,
)


class ModelTests(TestCase):

    def get_test_user(superuser=False):
        return get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            is_superuser=superuser,
        )

    def test_create_user(self):
        email = "testuser@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        email = "testuser@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            is_superuser=True,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_product(self):
        product_args = {
            'name': 'Test Product',
            'desc': 'A test Product',
            'stock': 20,
            'price': 4.99,
        }

        vendor = Vendor.objects.create()
        product = Product.objects.create(
            seller=vendor,
            **product_args,
        )

        self.assertEqual(product.seller, vendor)
        self.assertEqual(product.name, product_args['name'])
        self.assertEqual(product.desc, product_args['desc'])
        self.assertEqual(product.stock, product_args['stock'])
        self.assertEqual(product.price, product_args['price'])

    def test_create_vendor(self):
        vendor_args = {
            'name': 'Test Product',
            'desc': 'A test Product',
        }

        vendor = Vendor.objects.create(
            **vendor_args,
        )

        self.assertEqual(vendor.name, vendor_args['name'])
        self.assertEqual(vendor.desc, vendor_args['desc'])


class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.client.force_login(
            get_user_model().objects.create_user(
                email="adminuser@example.com",
                password="testpass123",
                is_superuser=True,
            )
        )

        self.base_user = get_user_model().objects.create_user(
            email="baseuser@example.com",
            password="testpass123",
            name="Test User",
        )

    def test_user_list(self):
        url = reverse('admin:core_consumer_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.base_user.name)
        self.assertContains(res, self.base_user.email)

    def test_user_create(self):
        url = reverse('admin:core_consumer_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_user_update(self):
        url = reverse('admin:core_consumer_change',
                      args=[self.base_user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
