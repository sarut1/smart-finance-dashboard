from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wallet

@login_required
def wallet_list(request):
    wallets = Wallet.objects.filter(user=request.user)
    return render(request, 'wallets/list.html', {'wallets': wallets})

@login_required
def wallet_create(request):
    if request.method == 'POST':
        Wallet.objects.create(
            user=request.user,
            wallet_name=request.POST.get('wallet_name'),
            wallet_type=request.POST.get('wallet_type'),
            balance=request.POST.get('balance', 0),
        )
        messages.success(request, 'เพิ่มกระเป๋าเงินสำเร็จ!')
        return redirect('wallets:list')
    return render(request, 'wallets/create.html')

@login_required
def wallet_delete(request, pk):
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    if request.method == 'POST':
        wallet.delete()
        messages.success(request, 'ลบกระเป๋าเงินสำเร็จ!')
    return redirect('wallets:list')