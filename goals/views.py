from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SavingGoal

@login_required
def goal_list(request):
    goals = SavingGoal.objects.filter(user=request.user)
    return render(request, 'goals/list.html', {'goals': goals})

@login_required
def goal_create(request):
    if request.method == 'POST':
        SavingGoal.objects.create(
            user=request.user,
            goal_name=request.POST.get('goal_name'),
            target_amount=request.POST.get('target_amount'),
            current_amount=request.POST.get('current_amount', 0),
            deadline=request.POST.get('deadline'),
        )
        messages.success(request, 'สร้างเป้าหมายสำเร็จ!')
        return redirect('goals:list')
    return render(request, 'goals/create.html')

@login_required
def goal_deposit(request, pk):
    goal = get_object_or_404(SavingGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        from decimal import Decimal
        amount = Decimal(request.POST.get('amount', '0'))
        if amount > 0:
            goal.current_amount += amount
            if goal.current_amount >= goal.target_amount:
                goal.current_amount = goal.target_amount
                messages.success(request, f'🎉 ยินดีด้วย! บรรลุเป้าหมาย {goal.goal_name} แล้ว!')
            else:
                messages.success(request, f'เพิ่มเงินออม ฿{amount:,.2f} สำเร็จ!')
            goal.save()
    return redirect('goals:list')

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(SavingGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'ลบเป้าหมายสำเร็จ!')
    return redirect('goals:list')