from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from transactions.models import Transaction
from wallets.models import Wallet
from dashboard.health_score import calculate_health_score
import json

@login_required
def index(request):
    user = request.user
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    transactions = Transaction.objects.filter(user=user)

    monthly_income = sum(
        t.amount for t in transactions
        if t.transaction_type == 'income'
        and t.date.month == current_month
        and t.date.year == current_year
    )
    monthly_expense = sum(
        t.amount for t in transactions
        if t.transaction_type == 'expense'
        and t.date.month == current_month
        and t.date.year == current_year
    )
    total_balance = sum(w.balance for w in Wallet.objects.filter(user=user))
    net_this_month = monthly_income - monthly_expense

    expense_by_category = {}
    for t in transactions.filter(
        transaction_type='expense',
        date__month=current_month,
        date__year=current_year
    ):
        cat_name = t.category.name if t.category else 'อื่นๆ'
        expense_by_category[cat_name] = expense_by_category.get(cat_name, 0) + float(t.amount)

    chart_labels = list(expense_by_category.keys())
    chart_data = list(expense_by_category.values())

    months_th = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.',
                 'ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']
    bar_income, bar_expense, bar_labels = [], [], []
    for m in range(1, 13):
        inc = sum(float(t.amount) for t in transactions
                  if t.transaction_type == 'income'
                  and t.date.month == m and t.date.year == current_year)
        exp = sum(float(t.amount) for t in transactions
                  if t.transaction_type == 'expense'
                  and t.date.month == m and t.date.year == current_year)
        bar_labels.append(months_th[m-1])
        bar_income.append(inc)
        bar_expense.append(exp)

    recent_transactions = transactions.order_by('-date', '-created_at')[:5]
    health = calculate_health_score(user)

    context = {
        'total_balance': total_balance,
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'net_this_month': net_this_month,
        'recent_transactions': recent_transactions,
        'has_expense_data': len(chart_data) > 0,
        'chart_labels': json.dumps(chart_labels, ensure_ascii=False),
        'chart_data': json.dumps(chart_data),
        'bar_labels': json.dumps(bar_labels, ensure_ascii=False),
        'bar_income': json.dumps(bar_income),
        'bar_expense': json.dumps(bar_expense),
        'health': health,
    }
    return render(request, 'dashboard/index.html', context)