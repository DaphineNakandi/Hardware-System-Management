
from rest_framework import generics

from hardware_app.models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    List all products or create a new product.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update an individual product.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
