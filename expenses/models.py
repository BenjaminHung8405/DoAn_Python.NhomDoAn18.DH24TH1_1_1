from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Custom user model based on AbstractUser so we can extend later (e.g. add chat_id)
class User(AbstractUser):
	chat_id = models.BigIntegerField(unique=True, null=True, blank=True)

	def __str__(self):
		return self.username


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True, null=True)

	# Link to the project's AUTH_USER_MODEL so it's compatible with a custom user
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

	def __str__(self):
		return self.name


class Expense(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
	date = models.DateField()
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	note = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		# Prefer username for readability
		username = getattr(self.user, 'username', str(self.user))
		return f"{username} - {self.amount} on {self.date}"
