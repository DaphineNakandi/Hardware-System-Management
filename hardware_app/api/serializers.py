
from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from hardware_app.models import Product, StockEntry, Supplier


class ProductSerializer(serializers.ModelSerializer):

    specification = serializers.CharField(
        max_length=100,
        allow_blank=False,
        required=True
    )

    def validate_specification(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Product specification is required."
            )

        return value

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "specification",
            "unit",
            "reorder_level",
            "date_created",
            "current_quantity",
        ]
        read_only_fields = [
            "id",
            "name",
            "date_created",
            "current_quantity",
        ]


class StockEntrySerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        required=False,
        allow_null=True
    )

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    supplier_name = serializers.CharField(
        source="supplier.name",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = StockEntry
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "cost_price",
            "selling_price",
            "supplier",
            "supplier_name",
            "payment_method",
            "date_received",
        ]
        read_only_fields = [
            "id",
            "date_received",
        ]

    def validate(self, attrs):
        cost_price = attrs.get(
            "cost_price",
            getattr(self.instance, "cost_price", None)
        )

        selling_price = attrs.get(
            "selling_price",
            getattr(self.instance, "selling_price", None)
        )

        if (
            cost_price is not None
            and selling_price is not None
            and selling_price < cost_price
        ):
            raise serializers.ValidationError({
                "selling_price": (
                    "Selling price cannot be less than cost price."
                )
            })

        return attrs

    def adjust_supplier_credit(self, supplier, amount):
        if supplier is None:
            return

        supplier = Supplier.objects.select_for_update().get(
            pk=supplier.pk
       )

        new_balance = supplier.credit_balance + amount

        if new_balance < Decimal("0"):
            raise serializers.ValidationError({
                "supplier": (
                    "This adjustment would make the supplier's "
                    "credit balance negative."
              )
        })

        supplier.credit_balance = new_balance
        supplier.save(update_fields=["credit_balance"])

    @transaction.atomic
    def create(self, validated_data):
        stock_entry = super().create(validated_data)

        if (
            stock_entry.payment_method == "credit"
            and stock_entry.supplier
        ):
            total_cost = (
                stock_entry.quantity * stock_entry.cost_price
            )

            self.adjust_supplier_credit(
                stock_entry.supplier,
                total_cost
            )

        return stock_entry

    @transaction.atomic
    def update(self, instance, validated_data):
        old_supplier = instance.supplier
        old_payment_method = instance.payment_method

        old_total_cost = (
            Decimal(instance.quantity) * instance.cost_price
        )

        updated_entry = super().update(instance, validated_data)

        if old_payment_method == "credit" and old_supplier:
            self.adjust_supplier_credit(
                old_supplier,
                -old_total_cost
            )

        if (
            updated_entry.payment_method == "credit"
            and updated_entry.supplier
        ):
            new_total_cost = (
                Decimal(updated_entry.quantity)
                * updated_entry.cost_price
            )

            self.adjust_supplier_credit(
                updated_entry.supplier,
                new_total_cost
            )

        return updated_entry
