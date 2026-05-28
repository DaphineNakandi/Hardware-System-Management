from django import forms
from decimal import Decimal
from .models import (
    Product, DepositCustomer, DepositPayment,
    DepositWithdrawal, Supplier, StockEntry, Sale
)


# PRODUCT FORM

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'specification': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if name and len(name.strip()) < 2:
            raise forms.ValidationError("Product name is too short")

        return name.title()



# CUSTOMER FORM


class DepositCustomerForm(forms.ModelForm):
    class Meta:
        model = DepositCustomer
        fields = [
            'full_name',
            'nin',
            'phone',
            'employer',
            'monthly_salary',
            'is_active',
            'notes'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nin': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'employer': forms.TextInput(attrs={'class': 'form-control'}),
            'monthly_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_nin(self):
        nin = self.cleaned_data.get('nin')

        if nin and len(nin.strip()) < 5:
            raise forms.ValidationError("Enter a valid NIN")

        return nin.upper()



# DEPOSIT FORM


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


# WITHDRAWAL FORM


class DepositWithdrawalForm(forms.ModelForm):
    class Meta:
        model = DepositWithdrawal
        fields = ['product', 'quantity']

        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity is None or quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero")

        return quantity

    def clean(self):
        cleaned_data = super().clean()

        product = cleaned_data.get('product')
       

       ## SUPPLIER FORM 
class SupplierForm(forms.ModelForm):
         class Meta:
             model = Supplier
             fields = '__all__'

             widgets = {
                 'name': forms.TextInput(attrs={'class': 'form-control'}),
                 'contact_person':forms.TextInput(attrs={'class': 'form-control'}),
                 'phone':forms.TextInput(attrs={'class': 'form-control'}),
                 'email': forms.EmailInput(attrs={'class': 'form-control'}),
                 'address': forms.Textarea(attrs={'class': 'form-control'}),
                 'notes': forms.Textarea(attrs={'class': 'form-control', 'row': 3})
             }
         
         
## STOCK ENTRY FORM 
class StockEntryForm(forms.ModelForm): 
    class Meta:
        model = StockEntry

        exclude =['product']

        widgets = {
            'quantity':forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_price':forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price':forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier':forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method':forms.Select(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()

        cost_price = cleaned_data.get('cost_price')
        selling_price = cleaned_data('selling_price')

        if cost_price and selling_price:
            if selling_price < cost_price:
                raise forms.ValidationForm(
                    'Selling price cannot be less'
                    'than cost_price'
                )
            
            return cleaned_data
        

## SALE FORM
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale

        fields = [
            'product',
            'quantity_sold',
            'customer_distance_km',
            'payment_method'
        ]

        widgets = {
            'product':forms.Select(attrs={'class': 'form-select'}),
            'quantity_sold':forms.NumberInput(attrs={'class': 'form-control'}),
            'customer_distance_km':forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method':forms.Select(attrs={'class': 'form-control'}),
        }


    def clean_quantity_sold(self):
        quantity = self.cleaned_data.get(
            'quantity_sold'
        )
        if quantity <= 0:
            raise forms.ValidationError(
                'Quantity must be greater than zero.'
            )
        return quantity
    
    def clean(self):
        cleaned_data = super().clean()

        product = cleaned_data('product')
        quantity = cleaned_data.get('quantity_sold')
        distance = cleaned_data.get(
            'customer_distance_km'
        )

        #Check stock availability

        if quantity > product.current_quantity:

            raise forms.ValidationError(
                f'Only {product.current_quantity}'
                f'{product.unit} available'
            )
        #Get latest selling price
        latest_stock = product.stock_entries.order_by('-date_received').first()

        if not latest_stock:
            raise forms.ValidationError(
                'No stock pricing found'
                'for this product'
            )
        
        selling_price = latest_stock.selling_price

        #Add calculate transport

        product_total = quantity * selling_price

        if distance <= 10 and product_total >= 500000:
            transport = Decimal(0)
        else:
            transport = Decimal(30000)

            cleaned_data['selling_price']
            cleaned_data['transport'] = transport

            return cleaned_data
        
        def save(self, commit=True):
            sale = super().save(commit=False)
            sale.selling_price = self.cleaned_data['selling_price']
            sale.selling_price = self.cleaned_data['selling_price']
            sale.transport = self.cleaned_data['transport'] 
            if commit:
                sale.save() 
                return sale





  