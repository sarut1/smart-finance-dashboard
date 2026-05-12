from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    WALLET_TYPES = [
        ('cash', 'เงินสด'),
        ('bank', 'บัญชีธนาคาร'),
        ('ewallet', 'กระเป๋าเงินดิจิทัล'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    wallet_name = models.CharField(max_length=100)
    wallet_type = models.CharField(max_length=20, choices=WALLET_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet_name} ({self.user.username})"