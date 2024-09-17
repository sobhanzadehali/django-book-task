from django.urls import path
from rest_framework.authtoken import views as auth_views

from accounts.api.v1.views import CustomDiscardAuthToken

app_name = 'api-v1'

urlpatterns = [
    path('login/', auth_views.ObtainAuthToken.as_view(), name='login'),
    path('logout/', CustomDiscardAuthToken.as_view(), name='logout'),

]
