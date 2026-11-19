
from rest_framework import generics

from hardware_app.models import Product, StockEntry
from .serializers import (
    ProductSerializer,
    StockEntrySerializer,
)
from .permissions import IsStoreManagerOrReadOnly


class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    List all products or create a new product.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStoreManagerOrReadOnly]


class ProductDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update an individual product.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStoreManagerOrReadOnly]


class StockEntryListCreateAPIView(generics.ListCreateAPIView):
    """
    List stock entries or record newly received stock.
    """

    queryset = StockEntry.objects.select_related(
        "product",
        "supplier",
    ).all()

    serializer_class = StockEntrySerializer
    permission_classes = [IsStoreManagerOrReadOnly]


class StockEntryDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update an individual stock entry.
    """

    queryset = StockEntry.objects.select_related(
        "product",
        "supplier",
    ).all()

    serializer_class = StockEntrySerializer
    permission_classes = [IsStoreManagerOrReadOnly]
