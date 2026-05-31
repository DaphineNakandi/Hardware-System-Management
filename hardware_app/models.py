from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator
from datetime import datetime



# PRODUCT MODEL

class Product(models.Model):
    name = models.CharField(max_length=100)
    specification = models.CharField(max_length=100, blank=True)

    CATEGORY_CHOICES = [
        ('cement', 'Cement'),
        ('iron_bar', 'Iron Bar'),
        ('nail', 'Nail'),
        ('wheelbarrow', 'Wheelbarrow'),
        ('wire_mesh', 'Wire Mesh'),
        ('barbed_wire', 'Barbed Wire'),
        ('iron_sheet', 'Iron Sheet'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='cement')

    UNIT_CHOICES = [
        ('bag', 'Bag'),
        ('piece', 'Piece'),
        ('kg', 'Kilogram'),
        ('meter', 'Meter'),
        ('box', 'Box'),
    ]

    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='piece')

    reorder_level = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.name} ({self.specification})" if self.specification else self.name

    @property
    def current_quantity(self):
        total_in = self.stock_entries.aggregate(total=Sum('quantity'))['total'] or 0
        total_out = self.sale_set.aggregate(total=Sum('quantity_sold'))['total'] or 0
        return total_in - total_out


# DEPOSIT CUSTOMER

class DepositCustomer(models.Model):
    full_name = models.CharField(max_length=200)
    nin = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)

    employer = models.CharField(max_length=200, blank=True)

    monthly_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    date_enrolled = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_enrolled']

    def __str__(self):
        return f"{self.full_name} ({self.nin})"

    @property
    def total_deposited(self):
        return self.deposits.aggregate(total=Sum('amount'))['total'] or 0

    @property
    def total_withdrawn(self):
        return self.withdrawals.aggregate(total=Sum('value_deducted'))['total'] or 0

    @property
    def current_balance(self):
        return self.total_deposited - self.total_withdrawn

    def can_pick_goods(self, amount):
        return self.current_balance >= amount



# DEPOSIT PAYMENT

class DepositPayment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
        ('bank', 'Bank Transfer'),
    ]

    customer = models.ForeignKey(
        DepositCustomer,
        on_delete=models.CASCADE,
        related_name='deposits'
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(1)])

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')

    temporary_receipt_number = models.CharField(max_length=50, unique=True, blank=True)

    date_deposited = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_deposited']

    def __str__(self):
        return f"{self.temporary_receipt_number} - {self.customer.full_name}"

    def save(self, *args, **kwargs):
        if not self.temporary_receipt_number:
            date_str = datetime.now().strftime('%Y%m%d')
            today_count = DepositPayment.objects.filter(
                date_deposited__date=datetime.now().date()
            ).count()

            self.temporary_receipt_number = f'TR-{date_str}-{today_count + 1:04d}'

        super().save(*args, **kwargs)



# DEPOSIT WITHDRAWAL

class DepositWithdrawal(models.Model):
    customer = models.ForeignKey(
        DepositCustomer,
        on_delete=models.CASCADE,
        related_name='withdrawals'
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    value_deducted = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )

    date_withdrawn = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_withdrawn']

    def __str__(self):
        return f"{self.customer.full_name} - {self.product.name}"



# STOCK ENTRY

class StockEntry(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
        ('bank', 'Bank'),
        ('credit', 'Credit'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_entries'
    )

    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')

    date_received = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_received']

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"



# SUPPLIER MODEL

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    credit_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    notes = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.name


# SALE MODEL
class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
        ('bank', 'Bank'),
        ('credit', 'Credit'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity_sold = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    customer_distance_km = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        validators=[MinValueValidator(0)]
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )

    date_sold = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_sold']

    def __str__(self):
        return f"{self.product.name} - {self.quantity_sold}"

    @property
    def total_amount(self):
        return (self.quantity_sold * self.selling_price) + (self.transport or 0)

    @property
    def qualifies_for_free_transport(self):
        return (
            self.customer_distance_km <= 10 and
            (self.quantity_sold * self.selling_price) >= 500000
        )