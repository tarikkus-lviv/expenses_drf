import calendar
from django.db.models import Q
from rest_framework import serializers
from .models import Salary, Category, Expense, Wish


class ShortSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'


class SalarySerializer(serializers.ModelSerializer):
    history_records = serializers.SerializerMethodField(method_name='get_history', required=False)
    month = serializers.SerializerMethodField(method_name='get_month', read_only=True)

    class Meta:
        model = Salary
        fields = '__all__'

    def get_history(self, obj):
        return ShortSalarySerializer(Salary.objects.filter(Q(history=True, parent__isnull=False, parent=obj.parent)
                                                           | Q(history=True, parent__isnull=True,
                                                               id=obj.parent.id if obj.parent is not None else None)),
                                     many=True).data

    def get_month(self, obj):
        numeric_month = obj.salary_date.month
        month_name = calendar.month_name[numeric_month]
        return month_name


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    category_info = CategorySerializer(many=False, source='category', required=False, read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = '__all__'


