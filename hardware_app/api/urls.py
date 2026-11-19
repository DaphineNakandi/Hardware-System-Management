
from django.urls import path

from .views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    StockEntryListCreateAPIView,
    StockEntryDetailAPIView,
)

urlpatterns = [
    # Product endpoints
    path(
        "products/",
        ProductListCreateAPIView.as_view(),
        name="product-list-create",
    ),
    path(
        "products/<int:pk>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),

    # Stock entry endpoints
    path(
        "stock-entries/",
        StockEntryListCreateAPIView.as_view(),
        name="stock-entry-list-create",
    ),
    path(
        "stock-entries/<int:pk>/",
        StockEntryDetailAPIView.as_view(),
        name="stock-entry-detail",
    ),
]
