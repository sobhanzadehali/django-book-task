from django.urls import path
from . import views

app_name = 'api-v1'

urlpatterns = [
    path('book/list/', views.BookListAPIView.as_view(), name='book-list'),
    path('review/', views.ReviewListCreateAPIView.as_view(), name='list-create-review'),
    # path('update/review/<int:pk>/', views.UpdateReviewView.as_view(), name='update-review'),
    # path('delete/review/<int:pk>/', views.DeleteReviewView.as_view(), name='delete-review'),
    # path('suggest/', views.SuggestBookView.as_view(), name='suggest'),
]
