from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import (
    Product,
    ProductSold,
    ProductStock,
    Transaction,
    Cart,
)

userModel = get_user_model()


class ModelTests(TestCase):

    def setUp(self):
        self.user_payload = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpassword123",
        }

        self.prod_payload = {
            "name": "Test Product",
            "desc": "Test Description",
        }

    def test_create_invalid(self):
        with self.assertRaises(ValidationError) as context:
            userModel.objects.create_user(
                **self.user_payload, category="invalid")

        error_message = "Value 'invalid' is not a valid choice."
        self.assertTrue(error_message in str(context.exception))

    def test_create_default_user(self):
        user = userModel.objects.create_user(**self.user_payload)
        self.assertEqual(user.name, self.user_payload["name"])
        self.assertEqual(user.email, self.user_payload["email"])
        self.assertTrue(user.check_password(self.user_payload["password"]))
        self.assertEqual(user.category, userModel.UserCategory.CONSUMER)

    def test_create_consumer(self):
        category = userModel.UserCategory.CONSUMER
        user = userModel.objects.create_user(
            **self.user_payload, category=category)

        self.assertEqual(user.category, category)
        self.assertEqual(user.name, self.user_payload["name"])
        self.assertEqual(user.email, self.user_payload["email"])
        self.assertTrue(user.check_password(self.user_payload["password"]))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_vendor(self):
        category = userModel.UserCategory.VENDOR
        user = userModel.objects.create_user(
            **self.user_payload, category=category)

        self.assertEqual(user.category, category)
        self.assertEqual(user.name, self.user_payload["name"])
        self.assertEqual(user.email, self.user_payload["email"])
        self.assertTrue(user.check_password(self.user_payload["password"]))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_admin(self):
        category = userModel.UserCategory.ADMIN
        user = userModel.objects.create_user(
            **self.user_payload, category=category)

        self.assertEqual(user.category, category)
        self.assertEqual(user.name, self.user_payload["name"])
        self.assertEqual(user.email, self.user_payload["email"])
        self.assertTrue(user.check_password(self.user_payload["password"]))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)

    def test_create_transaction(self):
        consumer = userModel.objects.create_user(**self.user_payload)
        transaction = Transaction.objects.create(consumer=consumer)
        self.assertEqual(transaction.consumer.id, consumer.id)

    def test_create_product(self):
        product = Product.objects.create(**self.prod_payload)
        self.assertEqual(product.name, self.prod_payload["name"])
        self.assertEqual(product.desc, self.prod_payload["desc"])

    def test_create_product_stock(self):
        test_user = userModel.objects.create(**self.user_payload)
        product = Product.objects.create(**self.prod_payload)
        payload = {"stock": 20, "price": 4.99}

        stocked = ProductStock.objects.create(
            vendor=test_user,
            product=product,
            **payload,
        )

        self.assertEqual(stocked.vendor.id, test_user.id)
        self.assertEqual(stocked.product.id, product.id)
        self.assertEqual(stocked.stock, payload["stock"])
        self.assertEqual(stocked.price, payload["price"])

    def test_create_product_sold(self):
        test_user = userModel.objects.create(**self.user_payload)
        transaction = Transaction.objects.create(consumer=test_user)
        product = Product.objects.create(**self.prod_payload)
        payload = {"stock": 20, "price": 4.99}

        sold = ProductSold.objects.create(
            transaction=transaction,
            product=product,
            **payload,
        )

        self.assertEqual(sold.transaction.id, transaction.id)
        self.assertEqual(sold.product.id, product.id)
        self.assertEqual(sold.stock, payload["stock"])
        self.assertEqual(sold.price, payload["price"])

    def test_create_cart(self):
        test_user = userModel.objects.create(**self.user_payload)
        product = Product.objects.create(**self.prod_payload)
        payload = {"stock": 20, "price": 4.99}

        stock_product = ProductStock.objects.create(
            vendor=test_user,
            product=product,
            ** payload,
        )

        cart = Cart.objects.create(
            product=stock_product,
            consumer=test_user,
        )

        self.assertEqual(cart.consumer.id, test_user.id)
        self.assertEqual(cart.product.id, stock_product.id)
        self.assertEqual(cart.product.stock, payload["stock"])
        self.assertEqual(cart.product.price, payload["price"])


class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.client.force_login(
            get_user_model().objects.create_user(
                category=userModel.UserCategory.ADMIN,
                email="adminuser@example.com",
                password="testpass123",
                name="Admin User",
            )
        )

        self.base_user = userModel.objects.create_user(
            email="baseuser@example.com",
            password="testpass123",
            name="Test User",
        )

    def test_user_list(self):
        res = self.client.get(reverse("admin:core_user_changelist"))
        self.assertContains(res, self.base_user.name)
        self.assertContains(res, self.base_user.email)

    def test_user_create(self):
        res = self.client.get(reverse("admin:core_user_add"))
        self.assertEqual(res.status_code, 200)

    def test_user_update(self):
        res = self.client.get(
            reverse("admin:core_user_change", args=[self.base_user.id])
        )
        self.assertEqual(res.status_code, 200)
