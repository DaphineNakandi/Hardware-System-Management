from django import forms
from decimal import Decimal
from .models import (
    Product, DepositCustomer, DepositPayment,
    DepositWithdrawal, Supplier, StockEntry, Sale
)


#  PRODUCT FORM 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'specification': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise forms.ValidationError("Product name must be at least 2 characters")
        return name.title()


# DEPOSIT CUSTOMER FORM

class DepositCustomerForm(forms.ModelForm):
    class Meta:
        model = DepositCustomer
        fields = ['full_name', 'nin', 'phone', 'employer', 'monthly_salary', 'is_active', 'notes']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nin': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'employer': forms.TextInput(attrs={'class': 'form-control'}),
            'monthly_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


        def full_name(self):
            full_name = self.cleaned_data.get('full_name')
            if full_name and len(full_name.strip()) < 5:
                raise forms.ValidationError("Full name must be at least 5 characters")
            return full_name.title()



    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not phone.isdigit():
                raise forms.ValidationError('Phone number must contain digits only')
            if len(phone) != 10:
                raise forms.ValidationError('Phone number must be exactly 10 digits')
            if not phone.startswith('07'):
                raise forms.ValidationError('Enter a valid Ugandan phone number (starting with 07)')
        return phone

    def clean_nin(self):
        nin = self.cleaned_data.get('nin')
        if nin and len(nin.strip()) < 5:
            raise forms.ValidationError("Enter a valid NIN (at least 5 characters)")
        return nin.upper()


# DEPOSIT PAYMENT FORM 

class DepositPaymentForm(forms.ModelForm):
    class Meta:
        model = DepositPayment
        fields = ['amount', 'payment_method']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero")
        return amount


# DEPOSIT WITHDRAWAL FORM 

class DepositWithdrawalForm(forms.ModelForm):
    class Meta:
        model = DepositWithdrawal
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            # Limit product choices to eligible categories
            self.fields['product'].queryset = Product.objects.filter(category__in=['cement', 'iron_sheet', 'iron_bar'])

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero")
        return quantity
    
    def clean_product(self):
        product = self.cleaned_data.get('product')
        if product and product.category not in ['cement', 'iron_sheet', 'iron_bar']:
            raise forms.ValidationError('Only Cement, iron sheetts and iron bars can be witdrawn.')
        return product



#  SUPPLIER FORM 

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not phone.isdigit():
                raise forms.ValidationError('Phone number must contain digits only')
            if len(phone) != 10:
                raise forms.ValidationError('Phone number must be exactly 10 digits')
            if not phone.startswith('07'):
                raise forms.ValidationError('Enter a valid Ugandan phone number (starting with 07)')
        return phone


#  STOCK ENTRY FORM 

class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        exclude = ['product']
        # fields = '__all__'
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),  
            'payment_method': forms.Select(attrs={'class': 'form-control'}),  
        }

    def clean(self):
        cleaned_data = super().clean()
        cost_price = cleaned_data.get('cost_price')
        selling_price = cleaned_data.get('selling_price')
        
        if cost_price and selling_price:
            if selling_price < cost_price:
                raise forms.ValidationError('Selling price cannot be less than cost price')
        return cleaned_data


#  SALE FORM 

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity_sold', 'customer_distance_km', 'payment_method']  
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity_sold': forms.NumberInput(attrs={'class': 'form-control'}),
            'customer_distance_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),  
        }

    def clean_quantity_sold(self):
        quantity = self.cleaned_data.get('quantity_sold')
        if quantity is not None and quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than zero')
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity_sold')
        distance = cleaned_data.get('customer_distance_km')
        
        if not product or not quantity or distance is None:
            return cleaned_data
        
        # Check stock availability
        if quantity > product.current_quantity:
            raise forms.ValidationError(f'Only {product.current_quantity} {product.get_unit_display()} available')
        
        # Get latest selling price
        latest_stock = product.stock_entries.order_by('-date_received').first()
        
        if not latest_stock:
            raise forms.ValidationError('No stock pricing found for this product')
        
        selling_price = latest_stock.selling_price
        
        # Calculate transport
        product_total = quantity * selling_price
        
        if distance <= 10 and product_total >= 500000:
            transport = Decimal('0')
        else:
            transport = Decimal('30000')
        
        cleaned_data['selling_price'] = selling_price
        cleaned_data['transport'] = transport
        
        return cleaned_data

    def save(self, commit=True):
        sale = super().save(commit=False)
        sale.selling_price = self.cleaned_data['selling_price']
        sale.transport = self.cleaned_data['transport']
        if commit:
            sale.save()
        return sale