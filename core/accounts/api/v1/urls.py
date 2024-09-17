from django.urls import path
from rest_framework.authtoken import views as auth_views

from accounts.api.v1.views import CustomDiscardAuthToken, RegisterView, VerifyEmailView

app_name = 'api-v1'

urlpatterns = [
    # registration and verification
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='email-verify'),
    # log in/out
    path('login/', auth_views.ObtainAuthToken.as_view(), name='login'),
    path('logout/', CustomDiscardAuthToken.as_view(), name='logout'),

]
