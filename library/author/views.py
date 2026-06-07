from django.shortcuts import render
from django.http import HttpResponse
from .models import Author


def authors_list(request):
    authors = Author.objects.all()
    return render(request, "author/authors_list.html", {"authors": authors})

def author_create(request):
    if request.method == "POST":
        Author.objects.create(
            name=request.POST.get("name"),
            surname=request.POST.get("surname"),
            patronymic=request.POST.get("patronymic")
        )
        return HttpResponse("Author created")

    return render(request, "author/author_create.html")

def author_delete(request, pk):
    try:
        author = Author.objects.get(id=pk)

        if author.books.count() == 0:
            author.delete()
            return HttpResponse("Author deleted")

        return HttpResponse("Author has books")

    except Author.DoesNotExist:
        return HttpResponse("Author not found")