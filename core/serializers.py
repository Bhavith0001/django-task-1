from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    created_by = serializers.CharField()
    modified_by = serializers.CharField()
    premium = serializers.BooleanField()


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    premium = serializers.BooleanField()
    paid = serializers.BooleanField()

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UpdateUserSerializer(UserRegistrationSerializer):
    password = serializers.CharField(read_only=True)
    modified_by = serializers.CharField()

