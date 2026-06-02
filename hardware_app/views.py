from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.db.models import Sum, F, Q
from datetime import date, datetime, timedelta
from decimal import Decimal
from .models import (
    Product, StockEntry, Sale, DepositCustomer, 
    DepositPayment, DepositWithdrawal, Supplier,
)
from .forms import (
    ProductForm, DepositCustomerForm, DepositPaymentForm, 
    DepositWithdrawalForm, SupplierForm, StockEntryForm, SaleForm,
)

# ROLE CHECKS - Only 3 Roles


def is_store_manager(user):
    return (
        user.groups.filter(name="Store Manager").exists()
        or user.is_superuser
    )


def is_sales_attendant(user):
    return (
        user.groups.filter(name="Sales Attendant").exists()
        or user.is_superuser
    )



# DASHBOARD 


@login_required
@user_passes_test(is_store_manager)
def dashboard(request):
    products = Product.objects.all()

    low_stock_products = [
        product for product in products
        if product.current_quantity <= product.reorder_level
    ]

    # FIXED: Today's sales calculation
    today = date.today()
    today_sales_objects = Sale.objects.filter(date_sold__date=today)

    today_sales = 0
    for sale in today_sales_objects:
        # Calculate each sale's total
        sale_total = (sale.quantity_sold * sale.selling_price) + (sale.transport or 0)
        today_sales += sale_total

    active_customers = DepositCustomer.objects.filter(is_active=True).count()

    context = {
        'total_products': products.count(),
        'low_stock_count': len(low_stock_products),
        'low_stock_products': low_stock_products,
        'today_sales': today_sales,
        'active_customers': active_customers,
    }

    return render(request, 'dashboard.html', context)



# PRODUCT MANAGEMENT


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required
@user_passes_test(is_store_manager)
def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Product added successfully!')
        return redirect('product_list')
    return render(request, 'add_product.html', {'form': form})


@login_required
@user_passes_test(is_store_manager)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, f'{product.name} updated successfully!')
        return redirect('product_list')
    return render(request, 'edit_product.html', {'form': form, 'product': product})



# CUSTOMER MANAGEMENT


@login_required
@user_passes_test(is_sales_attendant)
def register_customer(request):
    form = DepositCustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Customer registered successfully!')
        return redirect('customer_list')
    return render(request, 'register_customer.html', {'form': form})


@login_required
@user_passes_test(is_sales_attendant)
def customer_list(request):
    customers = DepositCustomer.objects.all()
    
    # Calculate totals using database aggregation for efficiency
    total_deposits = DepositPayment.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_withdrawals = DepositWithdrawal.objects.aggregate(total=Sum('value_deducted'))['total'] or 0
    
    context = {
        'customers': customers,
        'total_customers': customers.count(),
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
    }
    return render(request, 'customer_list.html', context)


@login_required
@user_passes_test(is_sales_attendant)
def customer_detail(request, customer_id):
    customer = get_object_or_404(DepositCustomer, id=customer_id)
    deposits = customer.deposits.all()
    withdrawals = customer.withdrawals.all()
    
    return render(request, 'customer_detail.html', {
        'customer': customer,
        'deposits': deposits,
        'withdrawals': withdrawals,
    })


@login_required
@user_passes_test(is_sales_attendant)
def edit_customer(request, customer_id):
    customer = get_object_or_404(DepositCustomer, id=customer_id)
    form = DepositCustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        messages.success(request, 'Customer updated successfully!')
        return redirect('customer_detail', customer_id=customer.id)
    return render(request, 'edit_customer.html', {'form': form, 'customer': customer})



# DEPOSIT MANAGEMENT


@login_required
@user_passes_test(is_sales_attendant)
def record_deposit(request, customer_id):
    customer = get_object_or_404(DepositCustomer, id=customer_id)
    form = DepositPaymentForm(request.POST or None)
    
    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.customer = customer
        deposit.save()
        messages.success(request, f'Deposit of UGX {deposit.amount:,.2f} recorded successfully!')
        return redirect('customer_detail', customer_id=customer.id)
    
    return render(request, 'record_deposit.html', {'form': form, 'customer': customer})


@login_required
@user_passes_test(is_sales_attendant)
def print_receipt(request, deposit_id):
    deposit = get_object_or_404(DepositPayment, id=deposit_id)
    return render(request, 'print_receipt.html', {'deposit': deposit})



# WITHDRAWAL (Goods Purchase)


@login_required
@user_passes_test(is_sales_attendant)
def withdraw_goods(request, customer_id):
    customer = get_object_or_404(DepositCustomer, id=customer_id)
    form = DepositWithdrawalForm(request.POST or None)
    
    eligible_products = Product.objects.filter(category__in=['cement', 'iron_sheet', 'iron_bar'])
    
    if form.is_valid():
        withdrawal = form.save(commit=False)
        withdrawal.customer = customer
        
        product = withdrawal.product
        quantity = withdrawal.quantity
        
        if product.category not in ['cement', 'iron_sheet', 'iron_bar']:
            messages.error(request, 'This product is not eligible for deposit scheme withdrawal.')
            return redirect('withdraw_goods', customer_id=customer.id)
        
        latest_stock = product.stock_entries.order_by('-date_received').first()
        if not latest_stock:
            messages.error(request, f'No price set for {product.name}. Please add stock first.')
            return redirect('withdraw_goods', customer_id=customer.id)
        
        selling_price = latest_stock.selling_price
        value_deducted = quantity * selling_price
        
        if customer.current_balance < value_deducted:
            messages.error(request, f'Insufficient balance! Need UGX {value_deducted:,.2f}, have UGX {customer.current_balance:,.2f}')
            return redirect('withdraw_goods', customer_id=customer.id)
        
        if product.current_quantity < quantity:
            messages.error(request, f'Not enough stock! Only {product.current_quantity} available.')
            return redirect('withdraw_goods', customer_id=customer.id)
        
        withdrawal.value_deducted = value_deducted
        withdrawal.save()
        
        messages.success(request, 'Goods withdrawn successfully!')
        return redirect('customer_detail', customer_id=customer.id)
    
    return render(request, 'withdraw_goods.html', {
        'form': form,
        'customer': customer,
        'products': eligible_products,
    })


@login_required
@user_passes_test(is_sales_attendant)
def cancel_withdrawal(request, withdrawal_id):
    withdrawal = get_object_or_404(DepositWithdrawal, id=withdrawal_id)
    
    if request.method == 'POST':
        withdrawal.delete()
        messages.success(request, 'Withdrawal cancelled successfully!')
        return redirect('customer_detail', customer_id=withdrawal.customer.id)
    
    return render(request, 'delete_confirm.html', {
        'object': withdrawal,
        'type': 'withdrawal',
        'name': f'{withdrawal.quantity} x {withdrawal.product.name}'
    })



# SUPPLIER MANAGEMENT


@login_required
@user_passes_test(is_store_manager)
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})


@login_required
@user_passes_test(is_store_manager)
def add_supplier(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Supplier added successfully!')
        return redirect('supplier_list')
    return render(request, 'add_supplier.html', {'form': form})


@login_required
@user_passes_test(is_store_manager)
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        messages.success(request, 'Supplier updated successfully!')
        return redirect('supplier_list')
    return render(request, 'edit_supplier.html', {'form': form, 'supplier': supplier})


@login_required
@user_passes_test(is_store_manager)
def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    stock_entries = StockEntry.objects.filter(supplier=supplier)
    return render(request, 'supplier_detail.html', {
        'supplier': supplier,
        'stock_entries': stock_entries,
    })


@login_required
@user_passes_test(is_store_manager)
def pay_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', 0))
        except:
            messages.error(request, 'Invalid amount entered.')
            return redirect('supplier_detail', supplier_id=supplier.id)
        
        if amount <= 0:
            messages.error(request, 'Amount must be greater than zero.')
        elif amount > supplier.credit_balance:
            messages.error(request, f'Cannot pay more than owed. Current balance: UGX {supplier.credit_balance:,.2f}')
        else:
            supplier.credit_balance -= amount
            supplier.save()
            messages.success(request, f'Paid UGX {amount:,.2f} to {supplier.name}. Remaining balance: UGX {supplier.credit_balance:,.2f}')
        
        return redirect('supplier_detail', supplier_id=supplier.id)
    
    return render(request, 'pay_supplier.html', {'supplier': supplier})



# STOCK MANAGEMENT


@login_required
@user_passes_test(is_store_manager)
def add_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = StockEntryForm(request.POST or None)
    suppliers = Supplier.objects.all().order_by('name')
    
    if form.is_valid():
        stock = form.save(commit=False)
        stock.product = product
        stock.save()
        
        if stock.payment_method == 'credit' and stock.supplier:
            total_cost = stock.quantity * stock.cost_price
            stock.supplier.credit_balance += total_cost
            stock.supplier.save()
            messages.info(request, f'Credit of UGX {total_cost:,.2f} added to {stock.supplier.name} account.')
        
        messages.success(request, f'{stock.quantity} units added successfully!')
        return redirect('stock_item', product_id=product.id)
    
    return render(request, 'add_stock.html', {
        'form': form, 
        'product': product,
        'suppliers': suppliers,
    })


@login_required
@user_passes_test(is_store_manager)
def stock_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    stock_entries = product.stock_entries.all()
    sales = product.sale_set.all()
    return render(request, 'stock_list.html', {
        'product': product,
        'stock_entries': stock_entries,
        'sales': sales,
    })


@login_required
@user_passes_test(is_store_manager)
def stock_history(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    stock_entries = product.stock_entries.all()
    sales = product.sale_set.all()
    return render(request, 'stock_history.html', {
        'product': product,
        'stock_entries': stock_entries,
        'sales': sales,
    })


@login_required
@user_passes_test(is_store_manager)
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
    
    return render(request, 'edit_stock_entry.html', {'form': form, 'entry': entry})



# SALES MANAGEMENT
@login_required
@user_passes_test(is_sales_attendant)
def sale_list(request):
    sales = Sale.objects.all()
    
    # Calculate totals
    total_sales_count = sales.count()
    total_revenue = 0
    total_transport = 0
    
    for sale in sales:
        total_revenue += (sale.quantity_sold * sale.selling_price) + (sale.transport or 0)
        total_transport += sale.transport or 0
    
    context = {
        'sales': sales,
        'total_sales_count': total_sales_count,
        'total_revenue': total_revenue,
        'total_transport': total_transport,
    }
    
    return render(request, 'sale_list.html', context)




@login_required
@user_passes_test(is_sales_attendant)
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
                messages.error(request, f'Not enough stock! Only {available_stock} {product.get_unit_display()} available.')
                return render(request, 'make_sale.html', {'form': form})
            
            latest_stock = product.stock_entries.order_by('-date_received').first()
            if not latest_stock:
                messages.error(request, 'This product has no stock entry yet.')
                return render(request, 'make_sale.html', {'form': form})
            
            sale.selling_price = latest_stock.selling_price
            product_total = quantity_sold * sale.selling_price
            
            if distance <= 10 and product_total >= 500000:
                sale.transport = Decimal('0')
                transport_msg = 'Free transport applied'
            else:
                sale.transport = Decimal('30000')
                transport_msg = 'Transport charge: UGX 30,000'
            
            sale.save()
            grand_total = product_total + sale.transport
            
            messages.success(request, f'Sale recorded successfully! Total: UGX {grand_total:,.0f} ({transport_msg})')
            return redirect('sale_list')
    else:
        form = SaleForm()
    
    return render(request, 'make_sale.html', {'form': form})


@login_required
@user_passes_test(is_store_manager)
def edit_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sale updated successfully!')
            return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)
    
    return render(request, 'edit_sale.html', {'form': form, 'sale': sale})



# REPORTS 

@login_required
@user_passes_test(is_store_manager)
def reports(request):
    products = Product.objects.all()
    customers = DepositCustomer.objects.all()
    sales = Sale.objects.all()

    low_stock_products = [
        product for product in products
        if (product.current_quantity <= product.reorder_level and product.current_quantity >= 0)
    ]

    total_deposits = DepositPayment.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    #  Calculate total sales without total_amount field
    total_sales = 0
    for sale in sales:
        total_sales += (sale.quantity_sold * sale.selling_price) + (sale.transport or 0)

    # Sales by month (latest 6 months)
    six_months_ago = datetime.now().date() - timedelta(days=180)
    sales_by_month = {}
    for sale in sales.filter(date_sold__gte=six_months_ago):
        month_key = sale.date_sold.strftime('%Y-%m')
        # FIXED: Calculate each sale total
        sale_total = (sale.quantity_sold * sale.selling_price) + (sale.transport or 0)
        sales_by_month[month_key] = sales_by_month.get(month_key, 0) + sale_total

    # TOP 5 Selling products
    product_sales = {}
    for sale in sales:
        product_name = sale.product.name
        product_sales[product_name] = product_sales.get(product_name, 0) + sale.quantity_sold

    top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]

    # DEPOSIT SCHEME SUMMARY
    active_deposit_customers = customers.filter(is_active=True).count()
    total_withdrawals = DepositWithdrawal.objects.aggregate(total=Sum('value_deducted'))['total'] or 0

    # SUPPLIER CREDIT SUMMARY
    suppliers = Supplier.objects.all()
    total_credit_owed = sum(supplier.credit_balance for supplier in suppliers)

    context = {
        'total_products': products.count(),
        'total_customers': customers.count(),
        'total_deposits': total_deposits,
        'total_sales': total_sales,
        'low_stock_products': low_stock_products,
        'sales_by_month': sales_by_month,
        'top_products': top_products,
        'active_deposit_customers': active_deposit_customers,
        'total_withdrawals': total_withdrawals,
        'total_credit_owed': total_credit_owed,
        'suppliers_count': suppliers.count(),
    }

    return render(request, 'reports.html', context)