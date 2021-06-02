from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from expenses import settings
from expenses.utils import utils, serializers_auth
from expenses.utils.http import JsonError
from expenses.utils.tokens import default_token_generator
from users.models import User


class PasswordResetView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to send email to user with password reset link.
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers_auth.PasswordResetSerializer

    _user = None

    def _action(self, serializer):
        try:
            user = self.get_user(serializer.data['email'])
        except User.DoesNotExist:
            return JsonError('No email', status=status.HTTP_404_NOT_FOUND)
        self.send_password_reset_email(user, serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_user(self, email):
        if self._user is None:
            self._user = User.objects.get(
                email__iexact=email,
                is_active=True,
            )
        return self._user

    def send_password_reset_email(self, user, data):
        email_factory = utils.UserPasswordResetEmailFactory.from_request(self.request, user=user, **data)
        email = email_factory.create()
        email.send()


class PasswordResetConfirmView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to finish reset password process.
    """
    token_generator = default_token_generator
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if settings.AUTH.get('PASSWORD_RESET_CONFIRM_RETYPE'):
            return serializers_auth.PasswordResetConfirmRetypeSerializer
        return serializers_auth.PasswordResetConfirmSerializer

    def _action(self, serializer):
        serializer.user.set_password(serializer.data['password'])
        serializer.user.save()

        self.send_password_changed_email(serializer.user)

        return Response({"status": "success"})

    def send_password_changed_email(self, user):
        email_factory = utils.UserPasswordChangedEmailFactory.from_request(self.request, user=user)
        email = email_factory.create()
        email.send()
