from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

# --- 1. الصفحة الرئيسية والبحث ---
def home(request):
    query = request.GET.get('q')
    articles_list = Article.objects.all().order_by('-created_at')
    
    if query:
        articles_list = articles_list.filter(Q(title__icontains=query) | Q(content__icontains=query))
        
    paginator = Paginator(articles_list, 3) # 3 مقالات في كل صفحة
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'home.html', {'page_obj': page_obj, 'query': query})

# --- 2. صفحة تفاصيل المقال والتعليقات ---
@login_required(login_url='login')
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            Comment.objects.create(article=article, name=request.user.username, body=body)
            messages.success(request, 'تم إضافة تعليقك بنجاح!')
            return redirect('article_detail', pk=article.pk)
            
    return render(request, 'article_detail.html', {'article': article})

# --- 3. تسجيل الدخول والخروج ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'تم تسجيل الدخول بنجاح!')
            return redirect('home')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'تم تسجيل الخروج بنجاح.')
    return redirect('home')

# --- 4. لوحة التحكم المخصصة ---
@login_required(login_url='login')
def dashboard(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'articles': articles})

@login_required(login_url='login')
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        if title and content:
            category = Category.objects.get(id=category_id) if category_id else None
            Article.objects.create(
                title=title, 
                content=content, 
                category=category,
                image=image
            )
            messages.success(request, 'تم إضافة المقالة بنجاح!')
            return redirect('dashboard')
            
    categories = Category.objects.all()
    return render(request, 'add_article.html', {'categories': categories})

@login_required(login_url='login')
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'تم حذف المقالة بنجاح.')
    return redirect('dashboard')