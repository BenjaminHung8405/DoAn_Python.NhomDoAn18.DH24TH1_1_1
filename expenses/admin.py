from django.contrib import admin
from .models import User, Category, Expense


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'username', 'chat_id')
	search_fields = ('username', 'chat_id')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	search_fields = ('name',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'category', 'date', 'amount')
	list_filter = ('date', 'category')
	search_fields = ('user__username', 'note')
