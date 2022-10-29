from rest_framework import serializers
from .models import Todo
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id','text', 'done']