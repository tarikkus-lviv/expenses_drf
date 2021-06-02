from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from expenses.utils.permissions import IsOwnerOrAdmin, IsAdminOrReadOnly
from .models import Category, Expense, Salary, Wish
from .paginators import StandardResultsSetPagination
from .serializers import CategorySerializer, ExpenseSerializer, SalarySerializer, WishSerializer


class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = SalarySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def list(self, request, *args, **kwargs):
        # todo make all the entries visible for admin
        queryset = Salary.objects.filter(user=request.user, history=False).order_by('-salary_date')
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        salary = serializer.instance

        salary.end_salary = salary.start_salary
        # salary.total_salary = salary.start_salary
        salary.month = serializer.data['month']
        salary.user = request.user

        salary.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        current = self.get_object()

        if current.history is True:
            raise ValidationError(
                "You can not edit this salary because it is in history.")
        else:
            current.history = True
            current.save()

            request.data['parent'] = current.parent.id if current.parent is not None else current.id
            request.data['user'] = current.user.id
            request.data['end_salary'] = request.data['start_salary']
            serializer = self.serializer_class(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            new_salary = serializer.instance

            print('updating salary!!!')
            print('and agaaaainQQQ')

            new_salary.month = serializer.data['month']
            new_salary.total_salary = new_salary.count_total_salary()
            new_salary.save()
            print(f'total_slary in views: {new_salary.total_salary}')

        # current.history = True
        # current.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def list(self, request, *args, **kwargs):
        queryset = Expense.objects.filter(user=request.user).order_by('-id')
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        expense = serializer.instance

        expense.user = request.user

        salary = Salary.objects.filter(history=False, user=request.user).first()
        expense.salary = salary

        expense.save()

        salary.end_salary = salary.end_salary - expense.price
        salary.total_salary = salary.count_total_salary()
        salary.save(update_fields=['end_salary', 'total_salary'])

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_price = instance.price

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        updated_price = instance.price

        if old_price != updated_price:
            salary = instance.salary

            # todo перевіряти чи є достатньо грошей з яких відраховувати, якщо апдейтнули вищу ціну

            if old_price > updated_price:
                new_price = old_price - updated_price
                salary.end_salary = salary.end_salary + new_price
                salary.save(update_fields=['end_salary'])
                salary.total_salary = salary.count_total_salary()
                salary.save(update_fields=['total_salary'])
            else:
                new_price = updated_price - old_price
                salary.end_salary = salary.end_salary - new_price
                salary.save(update_fields=['end_salary'])
                salary.total_salary = salary.count_total_salary()
                salary.save(update_fields=['total_salary'])

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        price = instance.price
        salary = instance.salary
        salary.end_salary = salary.end_salary + price
        salary.save(update_fields=['end_salary'])

        salary.total_salary = salary.count_total_salary()
        salary.save(update_fields=['total_salary'])

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class WishViewSet(viewsets.ModelViewSet):
    queryset = Wish.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = WishSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def list(self, request, *args, **kwargs):
        queryset = Wish.objects.filter(user=request.user).order_by('-salary_date')
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        salary = serializer.instance

        salary.user = request.user

        salary.save()

        return Response(serializer.data)

