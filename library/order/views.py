from django.http import HttpResponse
from django.utils import timezone

from .models import Order
from book.models import Book
from authentication.models import CustomUser


def orders_list(request):
    orders = Order.objects.all()

    result = ""

    for order in orders:
        book_name = order.book.name if order.book else "No book"
        user_email = order.user.email if order.user else "No user"
        end_at = order.end_at if order.end_at else "Not returned"

        result += (
            f"Order #{order.id} | "
            f"Book: {book_name} | "
            f"User: {user_email} | "
            f"End at: {end_at}<br>"
        )

    return HttpResponse(result)


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

        return HttpResponse("Order closed")

    except Order.DoesNotExist:
        return HttpResponse("Order not found")