from rest_framework import serializers
from .models import LogInModel, SignUpModel, ChatModel


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUpModel
        fields = ["username", "email", "password"]

class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogInModel
        fields = ["username", "password"]

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = ["recieverID", "transmitterID", "sendingtime", "content"]