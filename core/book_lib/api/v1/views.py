from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVerified
from book_lib.api.v1.serializers import BookSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

from ...models import Review, Book


class BookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        genre = self.request.query_params.get('genre', None)
        if genre is not None:
            books = Book.objects.raw("SELECT * FROM book_lib_book WHERE genre = %s", [genre, ])
        else:
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


class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        review_id = self.kwargs.get('pk')
        user_id = self.request.user.id

        # Raw SQL query to retrieve the review based on the review ID and user ID
        raw_query = "SELECT * FROM book_lib_review WHERE id = %s AND user_id = %s"

        review = list(Review.objects.raw(raw_query, [review_id, user_id]))

        if review:
            return review[0]
        else:
            return None

    def retrieve(self, request, *args, **kwargs):
        review = self.get_object()
        if review is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(review)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        if review is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Raw SQL query to update the review rate
        raw_update_query = """
            UPDATE book_lib_review SET rating = %s WHERE id = %s AND user_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(raw_update_query, [serializer.validated_data['rating'], review.id, self.request.user.id])

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        if review is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # Raw SQL query to delete the review
        raw_delete_query = """
            DELETE FROM book_lib_review WHERE id = %s AND user_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(raw_delete_query, [review.id, self.request.user.id])

        return Response(status=status.HTTP_204_NO_CONTENT)


class SuggestBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id

        # Get authors of books rated 4 or 5 by the user
        query1 = """
            SELECT DISTINCT b.author
            FROM book_lib_book b
            JOIN book_lib_review r ON r.book_id = b.id
            WHERE r.user_id = %s AND r.rating >= 4
        """

        with connection.cursor() as cursor:
            cursor.execute(query1, [user_id])
            authors = cursor.fetchall()

        # Extract authors from the result
        author_list = [author[0] for author in authors]

        # If no authors are found, return an empty list early
        if not author_list:
            return Response([])

        # Create the placeholders for the authors
        placeholders = ','.join(['%s'] * len(author_list))

        # Find other books by those authors that the user hasn't already rated
        query2 = f"""
            SELECT DISTINCT b.id, b.title, b.author
            FROM book_lib_book b
            WHERE b.author IN ({placeholders})
            AND b.id NOT IN (
                SELECT r.book_id
                FROM book_lib_review r
                WHERE r.user_id = %s
            )
        """

        # Execute the second raw SQL query
        params = author_list + [user_id]
        with connection.cursor() as cursor:
            cursor.execute(query2, params)
            suggested_books = cursor.fetchall()

        # Prepare the response data
        suggested_books_data = [{'id': book[0], 'title': book[1], 'author': book[2]} for book in suggested_books]

        return Response(suggested_books_data)
