from django.urls import path
from .views import authors_list, author_create, author_delete

urlpatterns = [
    path("", authors_list, name="authors_list"),
    path("create/", author_create, name="author_create"),
    path("<int:pk>/delete/", author_delete, name="author_delete"),
]