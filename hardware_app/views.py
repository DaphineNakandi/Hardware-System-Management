from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, F
from datetime import date
from decimal import Decimal
from .models import (Product,StockEntry,Sale,DepositCustomer,DepositPayment,DepositWithdrawal,Supplier,)

from .forms import (ProductForm, DepositCustomerForm, DepositPaymentForm, DepositWithdrawalForm, SupplierForm, StockEntryForm, SaleForm,)


# Create your views here.

# ROLE CHECKS
def is_manager(user):
    return (
        user.groups.filter(name="Manager").exists()
        or user.is_superuser
    )


def is_cashier(user):
    return (
        user.groups.filter(name="Cashier").exists()
        or is_manager(user)
    )


def is_credit_officer(user):
    return (
        user.groups.filter(name="Credit Officer").exists()
        or is_manager(user)
    )



# DASHBOARD


@login_required
def dashboard(request):

    products = Product.objects.all()

    low_stock_products = [
        product for product in products
        if product.current_quantity <= product.reorder_level
    ]

    today_sales = Sale.objects.filter(
        date_sold=date.today()
    )

    total_sales = sum(
        sale.total_amount
        for sale in today_sales
    )

    active_customers = DepositCustomer.objects.filter(
        is_active=True
    ).count()

    context = {
        'total_products': products.count(),
        'low_stock_count': len(low_stock_products),
        'low_stock_products': low_stock_products,
        'today_sales': total_sales,
        'active_customers': active_customers,
    }

    return render(request, 'dashboard.html', context)



# PRODUCTS
@login_required
def product_list(request):

    products = Product.objects.all()

    return render(request, 'product_list.html', {
        'products': products
    })


@login_required
@user_passes_test(is_manager)
def add_product(request):

    form = ProductForm(request.POST or None)

    if form.is_valid():
        form.save()

        messages.success(
            request,
            'Product added successfully!'
        )

        return redirect('product_list')

    return render(request, 'add_product.html', {
        'form': form
    })


@login_required
@user_passes_test(is_manager)
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    form = ProductForm(
        request.POST or None,
        instance=product
    )

    if form.is_valid():
        form.save()

        messages.success(
            request,
            f'{product.name} updated!'
        )

        return redirect('product_list')

    return render(request, 'edit_product.html', {
        'form': form,
        'product': product
    })


@login_required
@user_passes_test(is_manager)
def delete_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        product.delete()

        messages.success(
            request,
            f'{product.name} deleted!'
        )

        return redirect('product_list')

    return render(request, 'delete_confirm.html', {
        'object': product,
        'type': 'product',
        'name': product.name
    })



# CUSTOMERS


@login_required
@user_passes_test(is_credit_officer)
def register_customer(request):

    form = DepositCustomerForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Customer registered successfully!'
        )

        return redirect('customer_list')

    return render(request, 'register_customer.html', {
        'form': form
    })


@login_required
def customer_list(request):

    customers = DepositCustomer.objects.all()

    total_deposits = sum(
        customer.total_deposited
        for customer in customers
    )

    total_withdrawals = sum(
        customer.total_withdrawn
        for customer in customers
    )

    context = {
        'customers': customers,
        'total_customers': customers.count(),
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
    }

    return render(request, 'customer_list.html', context)


@login_required
def customer_detail(request, customer_id):

    customer = get_object_or_404(
        DepositCustomer,
        id=customer_id
    )

    deposits = customer.deposits.all()

    withdrawals = customer.withdrawals.all()

    return render(request, 'customer_detail.html', {
        'customer': customer,
        'deposits': deposits,
        'withdrawals': withdrawals,
    })


@login_required
def edit_customer(request, customer_id):

    customer = get_object_or_404(
        DepositCustomer,
        id=customer_id
    )

    form = DepositCustomerForm(
        request.POST or None,
        instance=customer
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Customer updated!'
        )

        return redirect(
            'customer_detail',
            customer_id=customer.id
        )

    return render(request, 'edit_customer.html', {
        'form': form,
        'customer': customer
    })


@login_required
def delete_customer(request, customer_id):

    customer = get_object_or_404(
        DepositCustomer,
        id=customer_id
    )

    if request.method == 'POST':

        if customer.current_balance > 0:

            messages.error(
                request,
                f'Cannot delete! Balance of UGX '
                f'{customer.current_balance:,.2f} remains.'
            )

            return redirect(
                'customer_detail',
                customer_id=customer.id
            )

        customer.delete()

        messages.success(
            request,
            'Customer deleted!'
        )

        return redirect('customer_list')

    return render(request, 'delete_confirm.html', {
        'object': customer,
        'type': 'customer',
        'name': customer.full_name
    })



# DEPOSITS

@login_required
def record_deposit(request, customer_id):

    customer = get_object_or_404(
        DepositCustomer,
        id=customer_id
    )

    form = DepositPaymentForm(
        request.POST or None
    )

    if form.is_valid():

        deposit = form.save(commit=False)
        deposit.customer = customer
        deposit.save()

        messages.success(
            request,
            f'Deposit of UGX {deposit.amount:,.2f} '
            f'recorded successfully!'
        )

        return redirect(
            'customer_detail',
            customer_id=customer.id
        )

    return render(request, 'record_deposit.html', {
        'form': form,
        'customer': customer
    })


@login_required
def print_receipt(request, deposit_id):

    deposit = get_object_or_404(
        DepositPayment,
        id=deposit_id
    )

    return render(request, 'print_receipt.html', {
        'deposit': deposit
    })


# WITHDRAWAL

@login_required
@user_passes_test(is_credit_officer)
def withdraw_goods(request, customer_id):

    customer = get_object_or_404(
        DepositCustomer,
        id=customer_id
    )

    form = DepositWithdrawalForm(
        request.POST or None
    )

    if form.is_valid():

        withdrawal = form.save(commit=False)
        withdrawal.customer = customer
        withdrawal.save()

        messages.success(
            request,
            'Goods withdrawn successfully!'
        )

        return redirect(
            'customer_detail',
            customer_id=customer.id
        )

    return render(request, 'withdraw_goods.html', {
        'form': form,
        'customer': customer
    })


@login_required
def cancel_withdrawal(request, withdrawal_id):

    withdrawal = get_object_or_404(
        DepositWithdrawal,
        id=withdrawal_id
    )

    if request.method == 'POST':

        withdrawal.delete()

        messages.success(
            request,
            'Withdrawal cancelled!'
        )

        return redirect(
            'customer_detail',
            customer_id=withdrawal.customer.id
        )

    return render(request, 'delete_confirm.html', {
        'object': withdrawal,
        'type': 'withdrawal',
        'name': f'{withdrawal.quantity} x {withdrawal.product.name}'
    })



# SUPPLIERS
@login_required
def supplier_list(request):

    suppliers = Supplier.objects.all()

    return render(request, 'supplier_list.html', {
        'suppliers': suppliers
    })


@login_required
@user_passes_test(is_manager)
def add_supplier(request):

    form = SupplierForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Supplier added successfully!'
        )

        return redirect('supplier_list')

    return render(request, 'add_supplier.html', {
        'form': form
    })


@login_required
def edit_supplier(request, supplier_id):

    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)

        if form.is_valid():
            form.save()

            messages.successs(request, 'Supplier updated successfully!')
            return redirect('supplier_list')
        
        else:

            form = SupplierForm(instance=supplier)

        return render(request, 'edit_supplier.html', {
            'form': form,
            'supplier': supplier
        })
        

@login_required
def delete_supplier(request, supplier_id):

    supplier = get_object_or_404(
        Supplier,
        id=supplier_id
    )

    if request.method == 'POST':

        supplier.delete()

        messages.success(
            request,
            'Supplier deleted!'
        )

        return redirect('supplier_list')

    return render(request, 'delete_confirm.html', {
        'object': supplier,
        'type': 'supplier',
        'name': supplier.name
    })


@login_required
def supplier_detail(request, supplier_id):

    supplier = get_object_or_404(
        Supplier,
        id=supplier_id
    )

    stock_entries = StockEntry.objects.filter(
        supplier=supplier.name
    )

    return render(request, 'supplier_detail.html', {
        'supplier': supplier,
        'stock_entries': stock_entries,
    })

# STOCK ENTRIES
@login_required
@user_passes_test(is_manager)
def add_stock(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    form = StockEntryForm(
        request.POST or None
    )

    if form.is_valid():

        stock = form.save(commit=False)
        stock.product = product
        stock.save()

        messages.success(
            request,
            f'{stock.quantity} units added successfully!'
        )

        return redirect(
            'stock_item',
            product_id=product.id
        )

    return render(request, 'add_stock.html', {
        'form': form,
        'product': product
    })


@login_required
def stock_item(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    stock_entries = product.stock_entries.all()

    sales = product.sale_set.all()

    return render(request, 'stock_list.html', {
        'product': product,
        'stock_entries': stock_entries,
        'sales': sales,
    })


@login_required
def stock_history(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    stock_entries = product.stock_entries.all()

    sales = product.sale_set.all()

    return render(request, 'stock_history.html', {
        'product': product,
        'stock_entries': stock_entries,
        'sales': sales,
    })


@login_required
@user_passes_test(is_manager)
def edit_stock_entry(request, entry_id):

    entry = get_object_or_404(StockEntry, id=entry_id)

    if request.method == 'POST':
        form = StockEntryForm(request.POST, instance=entry)

        if form.is_valid():
            form.save()

            messages.success(request, 'Stock entry updated successfully!')

            return redirect('stock_history', product_id=entry.product.id)
        
    else:
        form = StockEntryForm(instance=entry)

    return render(request, 'edit_stock_entry.html', {
        'form': form,
        'entry': entry

    })

    


@login_required
@user_passes_test(is_manager)
def delete_stock_entry(request, entry_id):

    entry = get_object_or_404(
        StockEntry,
        id=entry_id
    )

    if request.method == 'POST':

        entry.delete()

        messages.success(
            request,
            'Stock entry deleted!'
        )

        return redirect(
            'stock_history',
            product_id=entry.product.id
        )

    return render(request, 'delete_confirm.html', {
        'object': entry,
        'type': 'stock_entry',
        'name': f'{entry.product.name} +{entry.quantity}'
    })


# SALES
@login_required
def sale_list(request):

    sales = Sale.objects.all()

    return render(request, 'sale_list.html', {
        'sales': sales
    })



@login_required
@user_passes_test(is_cashier)
def make_sale(request):

    if request.method == 'POST':
        form = SaleForm(request.POST)

        if form.is_valid():
            sale = form.save(commit=False)

            product = sale.product
            quantity_sold = sale.quantity_sold
            distance = sale.customer_distance_km

            available_stock = product.current_quantity

            if quantity_sold > available_stock:
                messages.error(
                    request,
                    f'Not enough stock! Only {available_stock} {product.get_unit_display()} available.'
                )
                return render(request, 'make_sale.html', {'form': form})

            latest_stock = product.stock_entries.order_by('-date_received').first()

            if not latest_stock:
                messages.error(request, 'This product has no stock entry yet.')
                return render(request, 'make_sale.html', {'form': form})

            sale.selling_price = latest_stock.selling_price

            product_total = quantity_sold * sale.selling_price

            # transport logic
            if distance <= 10 and product_total >= 500000:
                sale.transport = Decimal('0')
                transport_msg = 'Free transport applied'
            else:
                sale.transport = Decimal('30000')
                transport_msg = 'Transport charge: UGX 30,000'

            sale.save()

            grand_total = product_total + sale.transport

            messages.success(
                request,
                f'Sale recorded successfully! Total: UGX {grand_total:,.0f} ({transport_msg})'
            )

            return redirect('sale_list')

    else:
        form = SaleForm()

    return render(request, 'make_sale.html', {'form': form})

   
@login_required
def edit_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)

    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)

        if form.is_valid():
            form.save()
            messages.success(request, 'Sale updated successfully')
            return redirect('sale_list')
        
        else:
            form = SaleForm(instance=sale)

        return render(request, 'edit_sale.html', {
            'form': form,
            'sale': sale
        })

    


@login_required
def delete_sale(request, sale_id):

    sale = get_object_or_404(
        Sale,
        id=sale_id
    )

    if request.method == 'POST':

        sale.delete()

        messages.success(
            request,
            'Sale deleted!'
        )

        return redirect('sale_list')

    return render(request, 'delete_confirm.html', {
        'object': sale,
        'type': 'sale',
        'name': f'{sale.product.name} - {sale.quantity_sold} units'
    })

# REPORTS
@login_required
def reports(request):

    products = Product.objects.all()

    customers = DepositCustomer.objects.all()

    sales = Sale.objects.all()

    low_stock_products = [
        product for product in products
        if (
            product.current_quantity <= product.reorder_level
            and product.current_quantity >= 0
        )
    ]

    total_deposits = sum(
        customer.total_deposited
        for customer in customers
    )

    total_sales = sum(
        sale.total_amount
        for sale in sales
    )

    context = {
        'total_products': products.count(),
        'total_customers': customers.count(),
        'total_deposits': total_deposits,
        'total_sales': total_sales,
        'low_stock_products': low_stock_products,
    }

    return render(request, 'reports.html', context)
