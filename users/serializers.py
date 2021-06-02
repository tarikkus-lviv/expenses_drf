from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from expenses import settings
from expenses.utils import constants, validators, utils
from expenses.utils.serializers_auth import PasswordRetypeSerializer
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_superuser', 'is_staff']
        read_only_fields = ['last_login', 'created']

    def validate(self, attrs):
        # print(f'cur user validation: {self.instance}')
        attrs = super(UserRegisterSerializer, self).validate(attrs)

        if self.instance:
            return attrs

        password = attrs['password']
        if password:
            serializer = PasswordRetypeSerializer(data=self.context.get('request').data, context=self.context)
            serializer.is_valid(raise_exception=True)

        print('register ser validate')
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email', None)
        if email:
            email = email.lower()
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError({"error": [constants.USER_ALREADY_EXIST]})

        print(f'val data: {validated_data}')
        user = User.objects.create_user(**validated_data)
        print('ser create')
        return user

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions', 'is_superuser', 'is_staff']
        read_only_fields = ['last_login', 'created']

    # def create(self, validated_data):
        # email = validated_data.get('email', None)
        # if email:
        #     email = email.lower()
        # user = User.objects.filter(email=email)
        # if user:
        #     raise ValidationError({"error": [constants.USER_ALREADY_EXIST]})
        #
        # serializer = UserRegisterSerializer(data=self.context.get('request').data, context=self.context)
        # serializer.is_valid(raise_exception=True)
        #
        # print(f'val data: {validated_data}')
        # # user = User.objects.create_user(**validated_data)
        # print('ser create')
        # return user

    # def update(self, instance, validated_data):
    #     for (key, value) in validated_data.items():
    #         setattr(instance, key, value)
    #         print(f'{instance}; {key}; {value}')
    #
    #     password = validated_data['password']
    #     instance.set_password(password)
    #     instance.save()
    #     return instance





