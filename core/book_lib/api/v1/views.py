from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVerified

from book_lib.models import Book
from book_lib.api.v1.serializers import BookSerializer, ReviewSerializer

from ...models import Review


class BookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        books = Book.objects.raw("SELECT * FROM book_lib_book")
        return books

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, IsVerified)

    def get_queryset(self):
        return Review.objects.raw("SELECT * FROM book_lib_review WHERE user_id= %s", [self.request.user.pk])
