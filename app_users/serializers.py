from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, validated_data):
        # Registration logic
        username = validated_data.get("username")
        email = validated_data.get("email")

        # Check if username or email already exists
        if UserModel.objects.filter(username=username).exists():
            raise APIException("Username already exists.")
        if UserModel.objects.filter(email=email).exists():
            raise APIException("Email already exists.")

        # Create user and return
        user_obj = UserModel.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        user_obj.username = validated_data["username"]
        user_obj.save()
        return user_obj


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "username")
