
from decimal import Decimal

from django.contrib.auth.models import Group, User

from django.db import transaction
from django.test import TestCase
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.test import APITestCase

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
    Supplier,
)


class ProductInventoryTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Cement",
            category="cement",
            specification="Test 32.5N, 50kg",
            unit="bag",
            reorder_level=5,
        )

    def test_current_quantity_is_stock_received_minus_sales(self):
        StockEntry.objects.create(
            product=self.product,
            quantity=20,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"),
            payment_method="cash",
        )
        Sale.objects.create(
            product=self.product,
            quantity_sold=3,
            selling_price=Decimal("32000.00"),
            payment_method="cash",
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

    def test_queryset_update_cannot_change_product_category(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Product categories cannot be changed using bulk updates.",
        ):
            Product.objects.filter(pk=self.product.pk).update(
                category="iron_bar"
            )

        self.product.refresh_from_db()

        self.assertEqual(self.product.category, "cement")

    def test_category_update_also_updates_derived_product_name(self):
        self.product.category = "iron_bar"
        self.product.save(update_fields=["category"])

        self.product.refresh_from_db()

        self.assertEqual(self.product.category, "iron_bar")
        self.assertEqual(self.product.name, "Iron Bar")

    def test_bulk_update_cannot_change_product_category(self):
        self.product.category = "iron_bar"

        with self.assertRaisesMessage(
            ValidationError,
            "Product categories cannot be changed using bulk updates.",
        ):
            with transaction.atomic():
                Product.objects.bulk_update(
                    [self.product],
                    ["category"],
                )

        self.product.refresh_from_db()

        self.assertEqual(self.product.category, "cement")

    def test_product_cannot_be_created_without_specification(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Product specification is required.",
        ):
            Product.objects.create(
                name="Cement",
                category="cement",
                specification="   ",
            )


class SaleCalculationTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Iron bar",
            category="iron_bar",
            specification="Test 12mm",
        )

    def test_total_amount_includes_transport(self):
        sale = Sale.objects.create(
            product=self.product,
            quantity_sold=2,
            selling_price=Decimal("250000.00"),
            transport=Decimal("30000.00"),
            payment_method="cash",
        )
        self.assertEqual(sale.total_amount, Decimal("530000.00"))

    def test_free_transport_requires_distance_and_minimum_purchase(self):
        eligible = Sale.objects.create(
            product=self.product,
            quantity_sold=2,
            selling_price=Decimal("250000.00"),
            customer_distance_km=Decimal("10.00"),
            payment_method="cash",
        )
        distant = Sale.objects.create(
            product=self.product,
            quantity_sold=2,
            selling_price=Decimal("250000.00"),
            customer_distance_km=Decimal("10.01"),
            payment_method="cash",
        )
        self.assertTrue(eligible.qualifies_for_free_transport)
        self.assertFalse(distant.qualifies_for_free_transport)


class DepositBalanceTests(TestCase):
    def setUp(self):
        self.customer = DepositCustomer.objects.create(
            full_name="Test Customer",
            nin="TEST-NIN-001",
            phone="0700000000",
        )
        self.product = Product.objects.create(
            name="Cement",
            category="cement",
            specification="Test 32.5N, 50kg",
        )

    def test_current_balance_is_deposits_minus_withdrawals(self):
        DepositPayment.objects.create(
            customer=self.customer,
            amount=Decimal("200000.00"),
            payment_method="cash",
        )
        DepositWithdrawal.objects.create(
            customer=self.customer,
            product=self.product,
            quantity=2,
            value_deducted=Decimal("65000.00"),
        )
        self.assertEqual(
            self.customer.current_balance,
            Decimal("135000.00"),
        )

    def test_customer_cannot_pick_goods_beyond_balance(self):
        DepositPayment.objects.create(
            customer=self.customer,
            amount=Decimal("50000.00"),
            payment_method="cash",
        )
        self.assertTrue(
            self.customer.can_pick_goods(Decimal("50000.00"))
        )
        self.assertFalse(
            self.customer.can_pick_goods(Decimal("50000.01"))
        )


class FormValidationTests(TestCase):
    def setUp(self):
        self.eligible_product = Product.objects.create(
            name="Cement",
            category="cement",
            specification="Test 32.5N, 50kg",
            unit="bag",
        )

        self.ineligible_product = Product.objects.create(
            name="Nail",
            category="nail",
            specification="Test 3-inch",
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

    def test_product_category_can_change_before_transaction_history(self):
        self.eligible_product.category = "iron_bar"
        self.eligible_product.save()

        self.assertEqual(self.eligible_product.name, "Iron Bar")

    def test_product_category_cannot_change_after_transaction_history(self):
        StockEntry.objects.create(
            product=self.eligible_product,
            quantity=20,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"),
            payment_method="cash",
        )

        customer = DepositCustomer.objects.create(
            full_name="History Customer",
            nin="HISTORY-NIN-001",
            phone="0700000000",
        )

        Sale.objects.create(
            product=self.eligible_product,
            quantity_sold=2,
            selling_price=Decimal("32000.00"),
            payment_method="cash",
        )

        DepositWithdrawal.objects.create(
            customer=customer,
            product=self.eligible_product,
            quantity=1,
            value_deducted=Decimal("32000.00"),
        )

        self.eligible_product.category = "iron_bar"

        with self.assertRaisesMessage(
            ValidationError,
            "A product category cannot be changed after stock, sales, "
            "or customer withdrawals have been recorded.",
        ):
            self.eligible_product.save()

    def test_product_form_rejects_category_change_after_history(self):
        StockEntry.objects.create(
            product=self.eligible_product,
            quantity=20,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"),
            payment_method="cash",
        )

        form = ProductForm(
            data={
                "specification": "Hima 32.5N, 50kg",
                "category": "iron_bar",
                "unit": "bag",
                "reorder_level": 10,
            },
            instance=self.eligible_product,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)

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

class ProductAPITests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Cement",
            category="cement",
            specification="Test 32.5N, 50kg",
            unit="bag",
            reorder_level=5,
        )

        self.list_url = "/api/products/"
        self.detail_url = f"/api/products/{self.product.id}/"

        # Create an authenticated Store Manager for normal API tests.
        manager_group, _ = Group.objects.get_or_create(
            name="Store Manager"
        )

        self.manager = User.objects.create_user(
            username="api_test_manager",
            password="test_password123",
        )
        self.manager.groups.add(manager_group)

        self.client.force_authenticate(user=self.manager)

        
    def test_list_products(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_product(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.product.id)
        self.assertEqual(response.data["category"], "cement")

    def test_create_product(self):
        data = {
            "category": "iron_bar",
            "specification": "12mm",
            "unit": "piece",
            "reorder_level": 10,
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Iron Bar")
        self.assertEqual(response.data["specification"], "12mm")

    def test_update_product_specification(self):
        response = self.client.patch(
            self.detail_url,
            {"specification": "50kg"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()
        self.assertEqual(self.product.specification, "50kg")

    def test_create_product_requires_specification(self):
        data = {
            "category": "cement",
            "unit": "bag",
            "reorder_level": 10,
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("specification", response.data)

    def test_unauthenticated_user_cannot_view_products(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_authenticated_staff_can_view_products(self):
        cashier_group = Group.objects.create(name="Cashier")
        cashier = User.objects.create_user(
            username="test_cashier",
            password="test_password123",
        )
        cashier.groups.add(cashier_group)

        self.client.force_authenticate(user=cashier)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cashier_cannot_create_products(self):
        cashier_group = Group.objects.create(name="Cashier")
        cashier = User.objects.create_user(
            username="test_cashier",
            password="test_password123",
        )
        cashier.groups.add(cashier_group)

        self.client.force_authenticate(user=cashier)

        response = self.client.post(
            self.list_url,
            {
                "category": "cement",
                "specification": "50kg",
                "unit": "bag",
                "reorder_level": 10,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_store_manager_can_create_products(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.post(
            self.list_url,
            {
                "category": "iron_bar",
                "specification": "12mm",
                "unit": "piece",
                "reorder_level": 10,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(response.data["name"], "Iron Bar")


class StockEntryAPITests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Cement",
            category="cement",
            specification="Test 32.5N, 50kg",
            unit="bag",
            reorder_level=5,
        )

        self.supplier = Supplier.objects.create(
            name="Test Supplier",
            credit_balance=Decimal("0.00"),
        )

        self.list_url = "/api/stock-entries/"

        manager_group, _ = Group.objects.get_or_create(
            name="Store Manager"
        )

        self.manager = User.objects.create_user(
            username="stock_api_manager",
            password="test_password123",
        )
        self.manager.groups.add(manager_group)

        self.client.force_authenticate(user=self.manager)

    def stock_data(self, **overrides):
        data = {
            "product": self.product.id,
            "quantity": 20,
            "cost_price": "28000.00",
            "selling_price": "32000.00",
            "supplier": self.supplier.id,
            "payment_method": "cash",
        }
        data.update(overrides)
        return data

    def test_list_stock_entries(self):
        StockEntry.objects.create(
            product=self.product,
            quantity=10,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"),
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_stock_entry(self):
        response = self.client.post(
            self.list_url,
            self.stock_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(response.data["quantity"], 20)
        self.assertEqual(StockEntry.objects.count(), 1)

    def test_create_credit_stock_entry_updates_supplier_balance(self):
        response = self.client.post(
            self.list_url,
            self.stock_data(payment_method="credit"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.supplier.refresh_from_db()

        self.assertEqual(
            self.supplier.credit_balance,
            Decimal("560000.00"),
        )

    def test_create_stock_entry_rejects_selling_price_below_cost(self):
        response = self.client.post(
            self.list_url,
            self.stock_data(selling_price="25000.00"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("selling_price", response.data)
        self.assertEqual(StockEntry.objects.count(), 0)

    def test_retrieve_stock_entry(self):
        entry = StockEntry.objects.create(
            product=self.product,
            quantity=10,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"),
        )

        response = self.client.get(
            f"{self.list_url}{entry.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["id"], entry.id)

    def test_update_credit_stock_entry_adjusts_supplier_balance(self):
        entry = StockEntry.objects.create(
            product=self.product,
            quantity=10,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"),
            supplier=self.supplier,
            payment_method="credit",
        )

        self.supplier.credit_balance = Decimal("280000.00")
        self.supplier.save()

        response = self.client.patch(
            f"{self.list_url}{entry.id}/",
            {"quantity": 20},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.supplier.refresh_from_db()

        self.assertEqual(
            self.supplier.credit_balance,
            Decimal("560000.00"),
        )

    def test_cashier_cannot_create_stock_entries(self):
        cashier_group, _ = Group.objects.get_or_create(
            name="Cashier"
        )

        cashier = User.objects.create_user(
            username="stock_api_cashier",
            password="test_password123",
        )
        cashier.groups.add(cashier_group)

        self.client.force_authenticate(user=cashier)

        response = self.client.post(
            self.list_url,
            self.stock_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_changing_credit_entry_to_cash_reverses_supplier_balance(self):
        entry = StockEntry.objects.create(
            product=self.product,
            quantity=10,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"),
            supplier=self.supplier,
            payment_method="credit",
        )

        self.supplier.credit_balance = Decimal("280000.00")
        self.supplier.save()

        response = self.client.patch(
            f"{self.list_url}{entry.id}/",
            {"payment_method": "cash"},
            format="json",
       )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.supplier.refresh_from_db()

        self.assertEqual(
            self.supplier.credit_balance,
            Decimal("0.00"),
        )

    def test_changing_supplier_on_credit_entry_adjusts_both_balances(self):
        second_supplier = Supplier.objects.create(
            name="Second Supplier",
            credit_balance=Decimal("0.00"),
       )

        entry = StockEntry.objects.create(
            product=self.product,
            quantity=10,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"),
            supplier=self.supplier,
            payment_method="credit",
       )

        self.supplier.credit_balance = Decimal("280000.00")
        self.supplier.save()

        response = self.client.patch(
            f"{self.list_url}{entry.id}/",
            {"supplier": second_supplier.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.supplier.refresh_from_db()
        second_supplier.refresh_from_db()

        self.assertEqual(
            self.supplier.credit_balance,
            Decimal("0.00"),
        )

        self.assertEqual(
            second_supplier.credit_balance,
            Decimal("280000.00"),
        )

    def test_credit_entry_update_is_rejected_if_supplier_balance_would_be_negative(self):
        entry = StockEntry.objects.create(
            product=self.product,
            quantity=10,
            cost_price=Decimal("28000.00"),
            selling_price=Decimal("32000.00"),
            supplier=self.supplier,
            payment_method="credit",
        )

        # The supplier has only partially paid the original debt.
        self.supplier.credit_balance = Decimal("100000.00")
        self.supplier.save()

        response = self.client.patch(
            f"{self.list_url}{entry.id}/",
            {"payment_method": "cash"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("supplier", response.data)

        # Confirm the stock entry was not changed.
        entry.refresh_from_db()
        self.assertEqual(entry.payment_method, "credit")

        # Confirm the supplier's balance was not changed.
        self.supplier.refresh_from_db()
        self.assertEqual(
            self.supplier.credit_balance,
            Decimal("100000.00"),
       )