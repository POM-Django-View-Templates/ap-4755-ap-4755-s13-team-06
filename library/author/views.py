from django.http import HttpResponse
from .models import Author


def authors_list(request):
    authors = Author.objects.all()

    result = ""

    for author in authors:
        result += (
            f"{author.id} "
            f"{author.name} "
            f"{author.surname} "
            f"{author.patronymic}<br>"
        )

    return HttpResponse(result)

def author_create(request):
    Author.objects.create(
        name="Test",
        surname="Author",
        patronymic="Middle"
    )

    return HttpResponse("Author created")

def author_delete(request, pk):
    try:
        author = Author.objects.get(id=pk)

        if author.books.count() == 0:
            author.delete()
            return HttpResponse("Author deleted")

        return HttpResponse("Author has books")

    except Author.DoesNotExist:
        return HttpResponse("Author not found")