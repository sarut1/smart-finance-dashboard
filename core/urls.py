from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('accounts:login')),  # หน้าแรก redirect ไป login
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('transactions/', include('transactions.urls')),
    path('wallets/', include('wallets.urls')),
    path('budgets/', include('budgets.urls')),
    path('analytics/', include('analytics.urls')),
    path('goals/', include('goals.urls')),
    path('notifications/', include('notifications.urls')),
    path('reports/', include('reports.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)