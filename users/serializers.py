from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User, Home


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=64, write_only=True)
    password = serializers.CharField(max_length=64, write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "age", "password", "confirm_password")

    def create(self, validated_data):
        if not validated_data.get('password') or not validated_data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")

        if validated_data.get('password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        del validated_data["confirm_password"]
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('password') or validated_data.get('confirm_password'):
            if validated_data.get('password') != validated_data.get('confirm_password'):
                raise serializers.ValidationError("Those passwords don't match.")
            del validated_data["confirm_password"]
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = "__all__"