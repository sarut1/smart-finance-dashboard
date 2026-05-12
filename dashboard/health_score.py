from transactions.models import Transaction
from budgets.models import Budget
from django.utils import timezone

def calculate_health_score(user):
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    transactions = Transaction.objects.filter(user=user)
    
    total_income = sum(
        float(t.amount) for t in transactions
        if t.transaction_type == 'income'
        and t.date.month == current_month
        and t.date.year == current_year
    )
    total_expense = sum(
        float(t.amount) for t in transactions
        if t.transaction_type == 'expense'
        and t.date.month == current_month
        and t.date.year == current_year
    )

    # --- 1. Saving Ratio Score (40 คะแนน) ---
    saving_ratio = ((total_income - total_expense) / total_income * 100) if total_income > 0 else 0
    if saving_ratio >= 30:
        saving_score = 40
    elif saving_ratio >= 20:
        saving_score = 30
    elif saving_ratio >= 10:
        saving_score = 20
    elif saving_ratio >= 0:
        saving_score = 10
    else:
        saving_score = 0

    # --- 2. Budget Compliance Score (35 คะแนน) ---
    budgets = Budget.objects.filter(
        user=user,
        month=today.replace(day=1)
    )
    budget_score = 35
    if budgets.exists():
        exceeded = 0
        for budget in budgets:
            spent = sum(
                float(t.amount) for t in transactions
                if t.transaction_type == 'expense'
                and t.category == budget.category
                and t.date.month == current_month
                and t.date.year == current_year
            )
            if spent > float(budget.limit_amount):
                exceeded += 1
        ratio = exceeded / budgets.count()
        budget_score = int(35 * (1 - ratio))

    # --- 3. Consistency Score (25 คะแนน) ---
    has_income = total_income > 0
    has_expense_tracking = total_expense > 0
    has_budget = budgets.exists()
    consistency_score = 0
    if has_income:
        consistency_score += 10
    if has_expense_tracking:
        consistency_score += 10
    if has_budget:
        consistency_score += 5

    total_score = saving_score + budget_score + consistency_score

    # --- Level ---
    if total_score >= 80:
        level = 'ดีเยี่ยม'
        level_color = '#00ff88'
        level_icon = 'bi-trophy'
    elif total_score >= 60:
        level = 'ดี'
        level_color = '#00d4ff'
        level_icon = 'bi-graph-up-arrow'
    elif total_score >= 40:
        level = 'พอใช้'
        level_color = '#ffa502'
        level_icon = 'bi-exclamation-circle'
    else:
        level = 'ต้องปรับปรุง'
        level_color = '#ff4757'
        level_icon = 'bi-exclamation-triangle'

    # --- Recommendations ---
    recommendations = []
    if saving_ratio < 20:
        recommendations.append('พยายามออมเงินอย่างน้อย 20% ของรายรับ')
    if budget_score < 20:
        recommendations.append('ควบคุมรายจ่ายให้อยู่ในงบประมาณที่ตั้งไว้')
    if not has_budget:
        recommendations.append('ตั้งงบประมาณรายหมวดหมู่เพื่อควบคุมการใช้จ่าย')
    if saving_ratio >= 20 and budget_score >= 25:
        recommendations.append('สุขภาพการเงินดีมาก! รักษาระดับนี้ต่อไป')

    return {
        'total_score': total_score,
        'saving_score': saving_score,
        'budget_score': budget_score,
        'consistency_score': consistency_score,
        'level': level,
        'level_color': level_color,
        'level_icon': level_icon,
        'saving_ratio': round(saving_ratio, 1),
        'recommendations': recommendations,
    }