from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_repeat = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        password = data.get('password')
        password_repeat = data.get('password_repeat')

        if password and password_repeat and password != password_repeat:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        password_repeat = validated_data.pop('password_repeat')

        if password and password_repeat and password == password_repeat:
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user

        raise serializers.ValidationError("Passwords do not match")

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_repeat']
