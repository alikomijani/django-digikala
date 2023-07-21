from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'mobile',
                  'password')

        read_only_fields = ('id',)
        write_only_fields = ('password',)

    def update(self, instance, validated_data):
        raise Exception('dont call update on UserRegisterSerializer')

    def create(self, validated_data):
        user = super().create(validated_data)
        # some action
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'mobile',
                  'last_login',
                  'date_joined',
                  )
        read_only_fields = ('last_login', 'date_joined')


class UserChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'password',
            'new_password'
        )
        write_only_fields = ('password', 'new_password')

    def update(self, instance, validated_data):
        if instance.check_password(validated_data['password']):
            instance.set_password(validated_data['new_password'])
            instance.save()
        else:
            raise serializers.ValidationError(
                {"password": "password incorrect"})

        return instance
