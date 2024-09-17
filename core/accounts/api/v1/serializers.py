from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False  # User needs to verify email
        user.save()

        # Send verification email
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        url = reverse('email-verify', kwargs={'uidb64': uidb64, 'token': token})
        verification_link = f"http://your-frontend.com{url}"

        subject = 'Verify your email'
        message = f"Hi {user.email}, use the link below to verify your email:\n{verification_link}"
        send_mail(subject, message, 'from@example.com', [user.email])

        return user
