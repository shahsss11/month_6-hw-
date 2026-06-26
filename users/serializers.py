from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import ConfirmationCode, CustomUser


class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField()
    phone_number = serializers.CharField(required=False)


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("User уже существует!")
        return email


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)
    def validate(self, attrs):
        user_id = attrs.get("user_id")
        code = attrs.get("code")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError("User не существует!")

        try:
            confirmation_code = ConfirmationCode.objects.get(user=user)
        except ConfirmationCode.DoesNotExist:
            raise ValidationError("Код подтверждения не найден!")

        if confirmation_code.code != code:
            raise ValidationError("Неверный код подтверждения!")
        attrs["user"] = user
        return attrs