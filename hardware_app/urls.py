from django.urls import path
from . import views

urlpatterns = [

    # DASHBOARD
    path('', views.dashboard, name='dashboard'),

    # PRODUCTS
    path('products/', views.product_list, name='product_list'),

    path(
        'products/add/',
        views.add_product,
        name='add_product'
    ),

    path(
        'products/<int:product_id>/edit/',
        views.edit_product,
        name='edit_product'
    ),

    path(
        'products/<int:product_id>/delete/',
        views.delete_product,
        name='delete_product'
    ),

    # STOCK
    path(
        'products/<int:product_id>/stock/',
        views.stock_item,
        name='stock_item'
    ),

    path(
        'products/<int:product_id>/stock/add/',
        views.add_stock,
        name='add_stock'
    ),

    path(
        'products/<int:product_id>/stock/history/',
        views.stock_history,
        name='stock_history'
    ),

    path(
        'stock/<int:entry_id>/edit/',
        views.edit_stock_entry,
        name='edit_stock_entry'
    ),

    path(
        'stock/<int:entry_id>/delete/',
        views.delete_stock_entry,
        name='delete_stock_entry'
    ),

    # CUSTOMERS
    path(
        'customers/',
        views.customer_list,
        name='customer_list'
    ),

    path(
        'customers/register/',
        views.register_customer,
        name='register_customer'
    ),

    path(
        'customers/<int:customer_id>/',
        views.customer_detail,
        name='customer_detail'
    ),

    path(
        'customers/<int:customer_id>/edit/',
        views.edit_customer,
        name='edit_customer'
    ),

    path(
        'customers/<int:customer_id>/delete/',
        views.delete_customer,
        name='delete_customer'
    ),

    path(
        'customers/<int:customer_id>/deposit/',
        views.record_deposit,
        name='record_deposit'
    ),

    path(
        'customers/<int:customer_id>/withdraw/',
        views.withdraw_goods,
        name='withdraw_goods'
    ),

    path(
        'receipt/<int:deposit_id>/',
        views.print_receipt,
        name='print_receipt'
    ),

    # SUPPLIERS
    path(
        'suppliers/',
        views.supplier_list,
        name='supplier_list'
    ),

    path(
        'suppliers/add/',
        views.add_supplier,
        name='add_supplier'
    ),

    path(
        'suppliers/<int:supplier_id>/',
        views.supplier_detail,
        name='supplier_detail'
    ),

    path(
        'suppliers/<int:supplier_id>/edit/',
        views.edit_supplier,
        name='edit_supplier'
    ),

    path(
        'suppliers/<int:supplier_id>/delete/',
        views.delete_supplier,
        name='delete_supplier'
    ),

    # SALES
    path(
        'sales/',
        views.sale_list,
        name='sale_list'
    ),

    path(
        'sales/make/',
        views.make_sale,
        name='make_sale'
    ),

    path(
        'sales/<int:sale_id>/edit/',
        views.edit_sale,
        name='edit_sale'
    ),

    path(
        'sales/<int:sale_id>/delete/',
        views.delete_sale,
        name='delete_sale'
    ),

    # REPORTS
    path(
        'reports/',
        views.reports,
        name='reports'
    ),
]

