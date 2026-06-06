from django.shortcuts import render, get_object_or_404
from .models import Book
from order.models import Order
from authentication.models import CustomUser

def book_list(request):
    """Список всіх книг + фільтрація"""
    books = Book.objects.all()
    
    search_title = request.GET.get('title')
    search_author = request.GET.get('author')

    if search_title:
        books = books.filter(name__icontains=search_title)
    
    if search_author:
        books = books.filter(authors__name__icontains=search_author) | books.filter(authors__surname__icontains=search_author)

    books = books.distinct()

    return render(request, 'book/book_list.html', {'books': books})

def book_detail(request, book_id):
    """Деталі конкретної книги"""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/book_detail.html', {'book': book})

def user_books(request, user_id):
    """Книги, видані конкретному юзеру (тільки для бібліотекаря)"""
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, '403_forbidden.html')

    target_user = get_object_or_404(CustomUser, id=user_id)
    orders = Order.objects.filter(user=target_user)
    
    return render(request, 'book/user_books.html', {'orders': orders, 'target_user': target_user})