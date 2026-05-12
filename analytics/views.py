from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from transactions.models import Transaction
import pandas as pd
import json

@login_required
def analytics_index(request):
    user = request.user
    today = timezone.now().date()
    
    transactions = Transaction.objects.filter(user=user).values(
        'amount', 'transaction_type', 'date', 'category__name'
    )

    context = {
        'total_transactions': 0,
        'avg_daily_expense': 0,
        'top_category': '-',
        'saving_ratio': 0,
        'weekly_labels': json.dumps([]),
        'weekly_data': json.dumps([]),
        'category_labels': json.dumps([]),
        'category_data': json.dumps([]),
        'insights': [],
    }

    if not transactions:
        return render(request, 'analytics/index.html', context)

    df = pd.DataFrame(list(transactions))
    df['amount'] = df['amount'].astype(float)
    df['date'] = pd.to_datetime(df['date'])

    # --- Summary Stats ---
    expenses = df[df['transaction_type'] == 'expense']
    incomes = df[df['transaction_type'] == 'income']

    total_expense = expenses['amount'].sum()
    total_income = incomes['amount'].sum()
    saving_ratio = round(((total_income - total_expense) / total_income * 100), 1) if total_income > 0 else 0
    avg_daily = round(expenses.groupby('date')['amount'].sum().mean(), 2) if not expenses.empty else 0

    # --- Top Category ---
    top_category = '-'
    if not expenses.empty:
        top_category = expenses.groupby('category__name')['amount'].sum().idxmax()

    # --- Weekly Spending (last 7 weeks) ---
    weekly = expenses.copy()
    weekly['week'] = weekly['date'].dt.isocalendar().week
    weekly_group = weekly.groupby('week')['amount'].sum().tail(7)
    weekly_labels = [f'สัปดาห์ {w}' for w in weekly_group.index.tolist()]
    weekly_data = weekly_group.values.tolist()

    # --- Category Breakdown ---
    if not expenses.empty:
        cat_group = expenses.groupby('category__name')['amount'].sum()
        category_labels = cat_group.index.tolist()
        category_data = cat_group.values.tolist()
    else:
        category_labels = []
        category_data = []

    # --- AI-Style Insights ---
    insights = []
    current_month = today.month
    current_year = today.year

    this_month = expenses[
        (expenses['date'].dt.month == current_month) &
        (expenses['date'].dt.year == current_year)
    ]
    last_month = expenses[
        (expenses['date'].dt.month == (current_month - 1)) &
        (expenses['date'].dt.year == current_year)
    ]

    if not this_month.empty and not last_month.empty:
        this_total = this_month['amount'].sum()
        last_total = last_month['amount'].sum()
        change = round(((this_total - last_total) / last_total) * 100, 1)
        if change > 0:
            insights.append({
                'icon': 'bi-arrow-up-circle',
                'color': '#ff4757',
                'text': f'รายจ่ายเดือนนี้เพิ่มขึ้น {change}% จากเดือนที่แล้ว'
            })
        else:
            insights.append({
                'icon': 'bi-arrow-down-circle',
                'color': '#00ff88',
                'text': f'รายจ่ายเดือนนี้ลดลง {abs(change)}% จากเดือนที่แล้ว'
            })

    if not expenses.empty:
        top_day = expenses.copy()
        top_day['weekday'] = top_day['date'].dt.day_name()
        top_day_name = top_day.groupby('weekday')['amount'].sum().idxmax()
        days_th = {
            'Monday': 'วันจันทร์', 'Tuesday': 'วันอังคาร',
            'Wednesday': 'วันพุธ', 'Thursday': 'วันพฤหัสบดี',
            'Friday': 'วันศุกร์', 'Saturday': 'วันเสาร์', 'Sunday': 'วันอาทิตย์'
        }
        insights.append({
            'icon': 'bi-calendar-day',
            'color': '#ffa502',
            'text': f'{days_th.get(top_day_name, top_day_name)} คือวันที่ใช้จ่ายมากที่สุดของคุณ'
        })

    if top_category != '-':
        insights.append({
            'icon': 'bi-tag',
            'color': '#00d4ff',
            'text': f'หมวดหมู่ที่ใช้จ่ายมากที่สุด คือ "{top_category}"'
        })

    if saving_ratio > 20:
        insights.append({
            'icon': 'bi-piggy-bank',
            'color': '#00ff88',
            'text': f'คุณออมเงินได้ {saving_ratio}% ของรายรับ — ดีมาก!'
        })
    elif saving_ratio < 0:
        insights.append({
            'icon': 'bi-exclamation-triangle',
            'color': '#ff4757',
            'text': f'รายจ่ายมากกว่ารายรับ ควรตรวจสอบการใช้จ่าย'
        })

    context = {
        'total_transactions': len(df),
        'avg_daily_expense': avg_daily,
        'top_category': top_category,
        'saving_ratio': saving_ratio,
        'weekly_labels': json.dumps(weekly_labels, ensure_ascii=False),
        'weekly_data': json.dumps(weekly_data),
        'category_labels': json.dumps(category_labels, ensure_ascii=False),
        'category_data': json.dumps(category_data),
        'insights': insights,
    }
    return render(request, 'analytics/index.html', context)