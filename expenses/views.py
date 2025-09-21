from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Expense, Category, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Đăng ký thành công!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'expenses/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Đăng nhập thành công!')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'expenses/login.html', {'form': form})


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    total_expenses = sum(exp.amount for exp in expenses)
    num_transactions = expenses.count()
    return render(request, 'expenses/dashboard.html', {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'num_transactions': num_transactions,
    })


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Đã đăng xuất.')
    return redirect('login')
