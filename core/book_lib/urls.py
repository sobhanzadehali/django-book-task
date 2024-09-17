from django.urls import path, include

app_name = 'book_lib'

urlpatterns = [
    path('api/', include('book_lib.api.v1.urls')),
]
