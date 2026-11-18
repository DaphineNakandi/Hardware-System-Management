from decimal import Decimal

from django.test import TestCase

from .forms import (
    DepositCustomerForm,
    DepositWithdrawalForm,
    ProductForm,
    SupplierForm,
)
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

    
    def test_current_quantity_also_subtracts_customer_withdrawals(self):
        StockEntry.objects.create(
            product=self.product,
            quantity=100,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"),
            payment_method="cash",
        )

        Sale.objects.create(
            product=self.product,
            quantity_sold=20,
            selling_price=Decimal("32000.00"),
            payment_method="cash",
        )

        customer = DepositCustomer.objects.create(
            full_name="Test Customer",
            nin="TEST-NIN-003",
            phone="0700000000",
        )

        DepositWithdrawal.objects.create(
            customer=customer,
            product=self.product,
            quantity=5,
            value_deducted=Decimal("160000.00"),
        )

        self.assertEqual(self.product.current_quantity, 75)


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


class FormValidationTests(TestCase):

    def setUp(self):
        self.eligible_product = Product.objects.create(
            name="Cement",
            category="cement",
            unit="bag",
        )

        self.ineligible_product = Product.objects.create(
            name="Nail",
            category="nail",
            unit="kg",
        )

    def test_product_form_does_not_allow_manual_product_names(self):
        form = ProductForm()

        self.assertNotIn("name", form.fields)
        self.assertEqual(
            list(form.fields),
            ["specification", "category", "unit", "reorder_level"],
        )

    def test_product_form_saves_name_from_approved_category(self):
        form = ProductForm(data={
            "specification": "  Hima 32.5N, 50kg  ",
            "category": "cement",
            "unit": "bag",
            "reorder_level": 10,
        })

        self.assertTrue(form.is_valid(), form.errors)
        product = form.save()

        self.assertEqual(product.name, "Cement")
        self.assertEqual(product.specification, "Hima 32.5N, 50kg")

    def test_product_form_rejects_blank_or_whitespace_specification(self):
        for specification in ("", "   "):
            with self.subTest(specification=specification):
                form = ProductForm(data={
                    "specification": specification,
                    "category": "cement",
                    "unit": "bag",
                    "reorder_level": 10,
                })
                self.assertFalse(form.is_valid())
                self.assertIn("specification", form.errors)

    def test_direct_product_save_cannot_store_arbitrary_name(self):
        product = Product.objects.create(
            name="Sugar",
            category="cement",
            specification="Hima 32.5N, 50kg",
            unit="bag",
        )

        self.assertEqual(product.name, "Cement")

    def test_withdrawal_form_only_shows_eligible_products(self):
        form = DepositWithdrawalForm()

        product_ids = list(
            form.fields["product"].queryset.values_list("id", flat=True)
        )

        self.assertIn(self.eligible_product.id, product_ids)
        self.assertNotIn(self.ineligible_product.id, product_ids)

    def test_supplier_form_does_not_expose_credit_balance(self):
        form = SupplierForm()

        self.assertNotIn("credit_balance", form.fields)

    def test_customer_form_strips_whitespace_from_full_name(self):
        form = DepositCustomerForm(data={
            "full_name": "  Test Customer  ",
            "nin": "TEST-NIN-002",
            "phone": "0700000000",
            "employer": "",
            "monthly_salary": "500000",
            "is_active": "on",
            "notes": "",
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data["full_name"],
            "Test Customer",
        )