from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Budget
from transactions.models import Category, Transaction

@login_required
def budget_list(request):
    today = timezone.now().date()
    current_month = today.replace(day=1)
    
    budgets = Budget.objects.filter(
        user=request.user,
        month=current_month
    ).select_related('category')

    budget_data = []
    for budget in budgets:
        spent = sum(
            t.amount for t in Transaction.objects.filter(
                user=request.user,
                category=budget.category,
                transaction_type='expense',
                date__month=today.month,
                date__year=today.year,
            )
        )
        percentage = min(int((spent / budget.limit_amount) * 100), 100) if budget.limit_amount > 0 else 0
        
        if percentage >= 100:
            status = 'danger'
        elif percentage >= 80:
            status = 'warning'
        else:
            status = 'success'

        budget_data.append({
            'budget': budget,
            'spent': spent,
            'remaining': max(budget.limit_amount - spent, 0),
            'percentage': percentage,
            'status': status,
        })

    context = {
        'budget_data': budget_data,
        'current_month': today.strftime('%B %Y'),
    }
    return render(request, 'budgets/list.html', context)

@login_required
def budget_create(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        limit_amount = request.POST.get('limit_amount')
        today = timezone.now().date()
        month = today.replace(day=1)

        if Budget.objects.filter(
            user=request.user,
            category_id=category_id,
            month=month
        ).exists():
            messages.error(request, 'มีงบประมาณหมวดหมู่นี้อยู่แล้วในเดือนนี้')
            return redirect('budgets:list')

        Budget.objects.create(
            user=request.user,
            category_id=category_id,
            limit_amount=limit_amount,
            month=month,
        )
        messages.success(request, 'ตั้งงบประมาณสำเร็จ!')
        return redirect('budgets:list')

    categories = Category.objects.filter(
        user=request.user,
        category_type='expense'
    )
    return render(request, 'budgets/create.html', {'categories': categories})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'ลบงบประมาณสำเร็จ!')
    return redirect('budgets:list')