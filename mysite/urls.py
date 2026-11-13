from django.contrib import admin
from django.urls import path
from pages.views import (
    home, 
    article_detail, 
    login_view, 
    logout_view, 
    dashboard, 
    add_article, 
    delete_article
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. الصفحة الرئيسية (هذا هو السطر الذي كان ناقصاً)
    path('', home, name='home'), 
    
    # 2. صفحة تفاصيل المقال
    path('article/<int:pk>/', article_detail, name='article_detail'),
    
    # 3. روابط الدخول والخروج
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # 4. روابط لوحة التحكم
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/add/', add_article, name='add_article'),
    path('dashboard/delete/<int:pk>/', delete_article, name='delete_article'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)