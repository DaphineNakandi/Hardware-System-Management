from decimal import Decimal

from django.test import TestCase

from .models import (
    DepositCustomer,
    DepositPayment,
    DepositWithdrawal,
    Product,
    Sale,
    StockEntry,
)


class ProductInventoryTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Cement", category="cement", unit="bag", reorder_level=5
        )

    def test_current_quantity_is_stock_received_minus_sales(self):
        StockEntry.objects.create(
            product=self.product, quantity=20,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"), payment_method="cash",
        )
        Sale.objects.create(
            product=self.product, quantity_sold=3,
            selling_price=Decimal("32000.00"), payment_method="cash",
        )
        self.assertEqual(self.product.current_quantity, 17)

    def test_product_without_stock_has_zero_quantity(self):
        self.assertEqual(self.product.current_quantity, 0)


class SaleCalculationTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Iron bar", category="iron_bar")

    def test_total_amount_includes_transport(self):
        sale = Sale.objects.create(
            product=self.product, quantity_sold=2,
            selling_price=Decimal("250000.00"),
            transport=Decimal("30000.00"), payment_method="cash",
        )
        self.assertEqual(sale.total_amount, Decimal("530000.00"))

    def test_free_transport_requires_distance_and_minimum_purchase(self):
        eligible = Sale.objects.create(
            product=self.product, quantity_sold=2,
            selling_price=Decimal("250000.00"),
            customer_distance_km=Decimal("10.00"), payment_method="cash",
        )
        distant = Sale.objects.create(
            product=self.product, quantity_sold=2,
            selling_price=Decimal("250000.00"),
            customer_distance_km=Decimal("10.01"), payment_method="cash",
        )
        self.assertTrue(eligible.qualifies_for_free_transport)
        self.assertFalse(distant.qualifies_for_free_transport)


class DepositBalanceTests(TestCase):
    def setUp(self):
        self.customer = DepositCustomer.objects.create(
            full_name="Test Customer", nin="TEST-NIN-001", phone="0700000000"
        )
        self.product = Product.objects.create(name="Cement", category="cement")

    def test_current_balance_is_deposits_minus_withdrawals(self):
        DepositPayment.objects.create(
            customer=self.customer, amount=Decimal("200000.00"), payment_method="cash"
        )
        DepositWithdrawal.objects.create(
            customer=self.customer, product=self.product, quantity=2,
            value_deducted=Decimal("65000.00"),
        )
        self.assertEqual(self.customer.current_balance, Decimal("135000.00"))

    def test_customer_cannot_pick_goods_beyond_balance(self):
        DepositPayment.objects.create(
            customer=self.customer, amount=Decimal("50000.00"), payment_method="cash"
        )
        self.assertTrue(self.customer.can_pick_goods(Decimal("50000.00")))
        self.assertFalse(self.customer.can_pick_goods(Decimal("50000.01")))
