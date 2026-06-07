from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect

from .models import Order
from book.models import Book
from authentication.models import CustomUser


def orders_list(request):
    orders = Order.objects.all()
    return render(request, "order/order_list.html", {"orders": orders})

def order_create(request):
    user = CustomUser.objects.first()
    book = Book.objects.first()

    if not user:
        return HttpResponse("No users in database")

    if not book:
        return HttpResponse("No books in database")

    Order.objects.create(
        user=user,
        book=book,
        plated_end_at=timezone.now()
    )

    return HttpResponse("Order created")


def order_close(request, pk):
    try:
        order = Order.objects.get(id=pk)
        order.end_at = timezone.now()
        order.save()
        return redirect("orders_list")

    except Order.DoesNotExist:
        return HttpResponse("Order not found")