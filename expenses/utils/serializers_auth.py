from abc import ABC

from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from expenses import settings
from expenses.utils import constants, validators
from users.models import User


class PasswordRetypeSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'})

    default_error_messages = {
        'password_mismatch': constants.PASSWORD_MISMATCH_ERROR,
        'password_requirements': constants.PASSWORD_REQUIREMENTS_ERROR,
    }

    def validate(self, attrs):
        attrs = super(PasswordRetypeSerializer, self).validate(attrs)

        from django.core import exceptions
        # uncomment next line if you want to have detailed error messages
        # validators.validate_password(password=attrs['new_password'], user=user)
        try:
            validators.validate_password(password=attrs['password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"error": self.error_messages['password_requirements']})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error": self.error_messages['password_mismatch']})
        print('retype ser')
        return attrs


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'})
    default_error_messages = {
        # Custom message for password validation
        'password_requirements': constants.PASSWORD_REQUIREMENTS_ERROR,
    }

    def validate(self, attrs):
        try:
            uidb64, token = attrs['token'].split('-', 1)
            assert uidb64 is not None and token is not None
            uid = urlsafe_base64_decode(uidb64)
            user = User._default_manager.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError, KeyError) as error:
            user = None
        from django.core import exceptions
        # uncomment next line if you want to have detailed error messages
        # validators.validate_password(password=attrs['new_password'], user=user)
        try:
            validators.validate_password(password=attrs['password'], user=user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"error": self.error_messages['password_requirements']})
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    default_error_messages = {
        'email_not_found': constants.EMAIL_NOT_FOUND
    }

    def validate_email(self, value):
        if settings.AUTH.get('PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND') and \
                not self.context['view'].get_users(value):
            raise serializers.ValidationError(self.error_messages['email_not_found'])
        return value


class UidAndTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    default_error_messages = {
        'invalid_token': constants.INVALID_TOKEN_ERROR,
        'invalid_uid': constants.INVALID_UID_ERROR,
    }

    def validate(self, attrs):
        attrs = super(UidAndTokenSerializer, self).validate(attrs)
        try:
            uidb64, token = attrs['token'].split('-', 1)
            assert uidb64 is not None and token is not None
            uid = urlsafe_base64_decode(uidb64)
            self.user = User._default_manager.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError) as error:
            raise serializers.ValidationError(self.error_messages['invalid_uid'])

        if not self.context['view'].token_generator.check_token(self.user, token):
            raise serializers.ValidationError(self.error_messages['invalid_token'])
        return attrs


class PasswordResetConfirmSerializer(UidAndTokenSerializer, PasswordSerializer):
    pass


class PasswordResetConfirmRetypeSerializer(UidAndTokenSerializer, PasswordRetypeSerializer):
    pass
