from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from expenses import settings
from expenses.utils import utils
from expenses.utils.permissions import IsCurrentUserOrAdmin
from expenses.utils.tokens import default_token_generator
from expenses_api.paginators import StandardResultsSetPagination
from users.models import User
from users.serializers import UserSerializer, UserRegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = UserRegisterSerializer
    permission_classes = (IsCurrentUserOrAdmin,)
    token_generator = default_token_generator

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all().order_by('-created')
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance
        user.is_active = True
        print(f'user: {user}')

        # password = serializer.initial_data['password']
        # print(f'view')
        # user.set_password(raw_password=password)
        # user.is_active = True
        # print(f'is user active? : {user.is_active}')
        user.save()

        if settings.AUTH.get('SEND_CONFIRMATION_EMAIL'):
            email_factory = utils.UserConfirmationEmailFactory.from_request(self.request, user=user, **{})
            email = email_factory.create()
            email.send()
            print('email sent successfully')

        # return Response(serializer.data)
        return Response(UserSerializer(user, context=self.get_serializer_context()).data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(f'upd instance : {instance}')

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        active = instance.is_active

        self.perform_update(serializer)

        return Response(UserSerializer(instance, context=self.get_serializer_context()).data)
