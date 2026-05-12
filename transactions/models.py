from django.db import models
from django.contrib.auth.models import User
from wallets.models import Wallet

class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'รายรับ'),
        ('expense', 'รายจ่าย'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    color = models.CharField(max_length=7, default='#00d4ff')
    icon = models.CharField(max_length=50, default='bi-tag')

    def __str__(self):
        return f"{self.name} ({self.category_type})"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'รายรับ'),
        ('expense', 'รายจ่าย'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    note = models.TextField(blank=True)
    tags = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.user.username})"