from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Notification
from transactions.models import Transaction
from budgets.models import Budget

def create_budget_notifications(user):
    today = timezone.now().date()
    current_month = today.replace(day=1)
    
    budgets = Budget.objects.filter(user=user, month=current_month)
    for budget in budgets:
        spent = sum(
            t.amount for t in Transaction.objects.filter(
                user=user,
                category=budget.category,
                transaction_type='expense',
                date__month=today.month,
                date__year=today.year,
            )
        )
        percentage = (spent / budget.limit_amount * 100) if budget.limit_amount > 0 else 0

        if percentage >= 100:
            msg = f'งบประมาณ "{budget.category.name}" เต็มแล้ว! ใช้ไป ฿{spent:,.2f}'
            if not Notification.objects.filter(user=user, message=msg, is_read=False).exists():
                Notification.objects.create(
                    user=user,
                    message=msg,
                    notification_type='budget',
                )
        elif percentage >= 80:
            msg = f'งบประมาณ "{budget.category.name}" ใกล้เต็มแล้ว ({int(percentage)}%)'
            if not Notification.objects.filter(user=user, message=msg, is_read=False).exists():
                Notification.objects.create(
                    user=user,
                    message=msg,
                    notification_type='budget',
                )

@login_required
def notification_list(request):
    create_budget_notifications(request.user)
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()

    if request.method == 'POST':
        notifications.update(is_read=True)
        return redirect('notifications:list')

    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/list.html', context)