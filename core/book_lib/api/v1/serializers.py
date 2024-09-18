from rest_framework import serializers

from book_lib.models import Book, Review


class BookSerializer(serializers.ModelSerializer):
    user_review = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'genre', 'user_review')

    def get_user_review(self, obj):
        user = self.context['request'].user
        try:
            query = "SELECT id, rating FROM book_lib_review WHERE book_id = %s and user_id = %s"
            review = Review.objects.raw(query, [obj.id, user.id])
            if review:
                data = {
                    'rating': review[0].rating
                }
                return data
        except Exception as e:
            return None


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'book',)
