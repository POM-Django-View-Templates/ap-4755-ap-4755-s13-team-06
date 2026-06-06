from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser

def login_view(request):
    """Вхід користувача"""
    # Якщо користувач відправив дані з твоєї HTML-форми
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Перевіряємо чи є такий юзер в базі
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user) # Логінимо
            return redirect('book_list') # Перекидаємо на головну сторінку з книгами
        else:
            # Якщо пароль неправильний - повертаємо форму і передаємо їй помилку
            return render(request, 'authentication/login.html', {'error': 'Неправильний email або пароль'})
            
    # Якщо це просто GET-запит (відкрили посилання) - показуємо твій HTML
    return render(request, 'authentication/login.html')

def register_view(request):
    """Реєстрація користувача"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        role = request.POST.get('role', 0)
        
        if email and password:
            # Створюємо юзера через наш CustomUserManager
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=int(role)
            )
            login(request, user) # Одразу логінимо після реєстрації
            return redirect('book_list')
            
    return render(request, 'authentication/register.html')

def logout_view(request):
    """Вихід з акаунту"""
    logout(request)
    return redirect('book_list')

def user_list(request):
    """Список всіх юзерів (доступно тільки бібліотекарю)"""
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, '403_forbidden.html')
        
    users = CustomUser.objects.all()
    return render(request, 'authentication/user_list.html', {'users': users})

def user_detail(request, user_id):
    """Деталі профілю юзера (доступно тільки бібліотекарю)"""
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, '403_forbidden.html')
        
    user_obj = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'authentication/user_detail.html', {'user_obj': user_obj})