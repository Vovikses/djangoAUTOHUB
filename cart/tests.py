from django.test import TestCase, Client
from django.urls import reverse
from main.models import Product, Category
from decimal import Decimal

class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Тестова категорія", slug="test-category")
        self.product = Product.objects.create(
            category=self.category,
            name='Гальмівні колодки',
            slug='brake-pads',
            price=Decimal('250.00'),
            available=True
        )

    def test_add_product_to_cart(self):
        url = reverse('cart:cart_add', args=[self.product.id])
        response = self.client.post(url, {'quantity': 2, 'override': False}, follow=True)
        session = self.client.session
        cart = session.get('cart')
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)]['quantity'], 2)

    def test_update_product_quantity_in_cart(self):
        # Add first
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1, 'override': False})
        # Now override
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 5, 'override': True})
        session = self.client.session
        cart = session.get('cart')
        self.assertEqual(cart[str(self.product.id)]['quantity'], 5)

    def test_remove_product_from_cart(self):
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1, 'override': False})
        response = self.client.post(reverse('cart:cart_remove', args=[self.product.id]), follow=True)
        session = self.client.session
        cart = session.get('cart')
        self.assertNotIn(str(self.product.id), cart)

    def test_cart_detail_view(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart_detail.html')
