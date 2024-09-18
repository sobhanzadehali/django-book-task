from django.urls import path
from . import views

app_name = 'api-v1'

urlpatterns = [
    path('book/list/', views.BookListAPIView.as_view(), name='book-list'),
    path('review/', views.ReviewListCreateAPIView.as_view(), name='list-create-review'),
    path('review/<int:pk>/', views.ReviewRetrieveUpdateDestroyAPIView.as_view(), name='update-review'),
    path('suggest/', views.SuggestBooksView.as_view(), name='suggest'),
]
