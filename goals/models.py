from django.db import models
from django.contrib.auth.models import User

class SavingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    goal_name = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def progress_percentage(self):
        if self.target_amount > 0:
            return min(round((self.current_amount / self.target_amount) * 100, 1), 100)
        return 0

    def __str__(self):
        return f"{self.goal_name} ({self.user.username})"