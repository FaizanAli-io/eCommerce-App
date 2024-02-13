from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Product, ProductSold, ProductStock, Transaction, Cart

userModel = get_user_model()

LIST_CREATE_URL = reverse('sales:cart-list')


def get_cart_detail_url(cart_id):
    return reverse('sales:cart-detail', args=[cart_id])


def get_transaction_url(transaction_id):
    return reverse('sales:cart-detail', args=[transaction_id])


def get_test_user(updates={}):

    payload = {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpassword123',
    }

    payload.update(updates)

    return userModel.objects.create_user(**payload)


def get_test_product():
    return Product.objects.create(
        name="Test product",
        desc="Test desc",
    )


def get_test_product_sold(transaction, product, stock=10, price=1.0):
    return ProductSold.objects.create(
        transaction=transaction,
        product=product,
        stock=stock,
        price=price,
    )


def get_test_product_stock(vendor, product, stock=10, price=1.0):
    return ProductStock.objects.create(
        product=product,
        vendor=vendor,
        stock=stock,
        price=price,
    )


def get_test_cart(consumer, product, cart_stock=5):
    return Cart.objects.create(
        product=product,
        consumer=consumer,
        cart_stock=cart_stock,
    )


def get_test_transaction(consumer):
    return Transaction.objects.create(
        consumer=consumer,
    )


class PublicUserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_test_user()

    def test_list_create_fails(self):
        get_res = self.client.get(LIST_CREATE_URL)
        post_res = self.client.post(LIST_CREATE_URL)

        self.assertEqual(get_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(post_res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_cart_detail_fails(self):
        product = get_test_product()
        stock_product = get_test_product_stock(self.user, product)
        cart = get_test_cart(self.user, stock_product)
        detail_url = get_cart_detail_url(cart.id)

        get_res = self.client.get(detail_url)
        put_res = self.client.put(detail_url)
        patch_res = self.client.patch(detail_url)
        delete_res = self.client.delete(detail_url)

        self.assertEqual(get_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(put_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(patch_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_transaction_fails(self):
        transaction = get_test_transaction(self.user)
        get_res = self.client.get(get_cart_detail_url(transaction.id))
        self.assertEqual(get_res.status_code, status.HTTP_401_UNAUTHORIZED)


class ConsumerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.vendor = get_test_user({
            'category': userModel.UserCategory.VENDOR,
            'email': 'vendor@example.com',
        })

        self.consumer = get_test_user({
            'category': userModel.UserCategory.CONSUMER,
            'email': 'consumer@example.com',
        })

        self.client.force_authenticate(self.consumer)

        self.test_product = get_test_product()

        self.test_product_stock = get_test_product_stock(
            self.vendor, self.test_product)

        # self.test_transaction = get_test_transaction(
        #     self.consumer)

        # self.test_product_sold = get_test_product_sold(
        #     self.test_transaction, self.test_product)

    def test_create_cart(self):
        payload = {
            "product": self.test_product_stock.id,
            "cart_stock": 5,
        }

        res = self.client.post(LIST_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['product'], payload['product'])
        self.assertEqual(res.data['consumer']['id'], self.consumer.id)
        self.assertEqual(res.data['cart_stock'], payload['cart_stock'])

    def test_list_cart(self):
        cart_item = get_test_cart(self.consumer, self.test_product_stock)
        res = self.client.get(LIST_CREATE_URL)
        data = res.data[0]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data['consumer']['id'], self.consumer.id)
        self.assertEqual(data['product'], cart_item.product.id)
        self.assertEqual(data['cart_stock'], cart_item.cart_stock)
