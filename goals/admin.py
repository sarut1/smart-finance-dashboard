from django.contrib import admin
from .models import SavingGoal

@admin.register(SavingGoal)
class SavingGoalAdmin(admin.ModelAdmin):
    list_display = ['goal_name', 'target_amount', 'current_amount', 'deadline', 'user']