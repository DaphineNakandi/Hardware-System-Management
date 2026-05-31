from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

# LOGIN VIEW
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser or user.groups.filter(name='Store Manager').exists():
                    return redirect('dashboard')
                elif user.groups.filter(name='Cashier').exists():
                    return redirect('product_list')
                elif user.groups.filter(name='Sales Attendant').exists():
                    return redirect('make_sale')
                elif user.groups.filter(name='Accounts/Admin').exists():
                    return redirect('customer_list')
                return redirect('dashboard')

            form.add_error(None, 'Invalid username or password.')

    return render(request, 'users/login.html', {'form': form})


# LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('login')