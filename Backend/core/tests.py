from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Product

userModel = get_user_model()


class ModelTests(TestCase):

    def setUp(self):
        self.payload = {
            'name': "Test User",
            'email': "testuser@example.com",
            'password': "testpassword123",
        }

    def test_create_invalid(self):
        with self.assertRaises(ValidationError) as context:
            userModel.objects.create_user(
                **self.payload, category='invalid')

        error_message = "Value 'invalid' is not a valid choice."
        self.assertTrue(error_message in str(context.exception))

    def test_create_default_user(self):
        user = userModel.objects.create_user(**self.payload)
        self.assertEqual(user.name, self.payload['name'])
        self.assertEqual(user.email, self.payload['email'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertEqual(user.category, userModel.UserCategory.CONSUMER)

    def test_create_consumer(self):
        category = userModel.UserCategory.CONSUMER
        user = userModel.objects.create_user(
            **self.payload, category=category)

        self.assertEqual(user.category, category)
        self.assertEqual(user.name, self.payload['name'])
        self.assertEqual(user.email, self.payload['email'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_vendor(self):
        category = userModel.UserCategory.VENDOR
        user = userModel.objects.create_user(
            **self.payload, category=category)

        self.assertEqual(user.category, category)
        self.assertEqual(user.name, self.payload['name'])
        self.assertEqual(user.email, self.payload['email'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_admin(self):
        category = userModel.UserCategory.ADMIN
        user = userModel.objects.create_user(
            **self.payload, category=category)

        self.assertEqual(user.category, category)
        self.assertEqual(user.name, self.payload['name'])
        self.assertEqual(user.email, self.payload['email'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_product(self):
        test_user = userModel.objects.create_user(**self.payload)

        product_args = {
            'name': 'Test Product',
            'desc': 'A test Product',
            'stock': 20, 'price': 4.99,
        }

        product = Product.objects.create(
            user=test_user,
            **product_args,
        )

        self.assertEqual(product.user, test_user)
        self.assertEqual(product.name, product_args['name'])
        self.assertEqual(product.desc, product_args['desc'])
        self.assertEqual(product.stock, product_args['stock'])
        self.assertEqual(product.price, product_args['price'])


# class AdminTests(TestCase):

#     def setUp(self):
#         self.client = Client()

#         self.client.force_login(
#             get_user_model().objects.create_user(
#                 email="adminuser@example.com",
#                 password="testpass123",
#                 is_superuser=True,
#             )
#         )

#         self.base_user = get_user_model().objects.create_user(
#             email="baseuser@example.com",
#             password="testpass123",
#             name="Test User",
#         )

#     def test_user_list(self):
#         url = reverse('admin:core_consumer_changelist')
#         res = self.client.get(url)
#         self.assertContains(res, self.base_user.name)
#         self.assertContains(res, self.base_user.email)

#     def test_user_create(self):
#         url = reverse('admin:core_consumer_add')
#         res = self.client.get(url)
#         self.assertEqual(res.status_code, 200)

#     def test_user_update(self):
#         url = reverse('admin:core_consumer_change',
#                       args=[self.base_user.id])
#         res = self.client.get(url)
#         self.assertEqual(res.status_code, 200)
