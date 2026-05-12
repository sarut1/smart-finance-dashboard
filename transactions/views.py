from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction, Category
from wallets.models import Wallet
from django.utils import timezone

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    
    # Filters
    month = request.GET.get('month')
    category_id = request.GET.get('category')
    transaction_type = request.GET.get('type')
    keyword = request.GET.get('keyword')

    if month:
        transactions = transactions.filter(date__month=month)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    if keyword:
        transactions = transactions.filter(note__icontains=keyword)

    categories = Category.objects.filter(user=request.user)
    
    context = {
        'transactions': transactions,
        'categories': categories,
    }
    return render(request, 'transactions/list.html', context)

@login_required
def transaction_create(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        wallet_id = request.POST.get('wallet')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        note = request.POST.get('note', '')
        tags = request.POST.get('tags', '')
        date = request.POST.get('date')
        is_recurring = request.POST.get('is_recurring') == 'on'

        Transaction.objects.create(
            user=request.user,
            category_id=category_id,
            wallet_id=wallet_id,
            amount=amount,
            transaction_type=transaction_type,
            note=note,
            tags=tags,
            date=date,
            is_recurring=is_recurring,
        )
        messages.success(request, 'เพิ่มรายการสำเร็จ!')
        return redirect('transactions:list')

    categories = Category.objects.filter(user=request.user)
    wallets = Wallet.objects.filter(user=request.user)
    context = {
        'categories': categories,
        'wallets': wallets,
        'today': timezone.now().date(),
    }
    return render(request, 'transactions/create.html', context)

@login_required
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.category_id = request.POST.get('category')
        transaction.wallet_id = request.POST.get('wallet')
        transaction.amount = request.POST.get('amount')
        transaction.transaction_type = request.POST.get('transaction_type')
        transaction.note = request.POST.get('note', '')
        transaction.tags = request.POST.get('tags', '')
        transaction.date = request.POST.get('date')
        transaction.is_recurring = request.POST.get('is_recurring') == 'on'
        transaction.save()
        messages.success(request, 'แก้ไขรายการสำเร็จ!')
        return redirect('transactions:list')

    categories = Category.objects.filter(user=request.user)
    wallets = Wallet.objects.filter(user=request.user)
    context = {
        'transaction': transaction,
        'categories': categories,
        'wallets': wallets,
    }
    return render(request, 'transactions/edit.html', context)

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'ลบรายการสำเร็จ!')
    return redirect('transactions:list')

@login_required
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_type = request.POST.get('category_type')
        color = request.POST.get('color', '#00d4ff')
        icon = request.POST.get('icon', 'bi-tag')

        Category.objects.create(
            user=request.user,
            name=name,
            category_type=category_type,
            color=color,
            icon=icon,
        )
        messages.success(request, 'เพิ่มหมวดหมู่สำเร็จ!')
        return redirect('transactions:list')

    return render(request, 'transactions/category_create.html')