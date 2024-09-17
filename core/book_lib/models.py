from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user.email} gave {self.book} {self.rating} out of 5 stars"
