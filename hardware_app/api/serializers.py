from rest_framework import serializers

from hardware_app.models import Product


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