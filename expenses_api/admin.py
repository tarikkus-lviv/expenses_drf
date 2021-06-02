from django.contrib import admin

from .models import Category, Expense, Salary, Wish


class SalaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'parent', 'start_salary', 'month']
    search_fields = ('month',)

    def name(self, obj):
        return obj.month


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ('name',)

    def name(self, obj):
        return obj.name


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'price', 'date']
    search_fields = ('name',)

    def name(self, obj):
        return obj.name


class WishAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'price', 'priority']
    search_fields = ('name',)

    def name(self, obj):
        return obj.name


admin.site.register(Salary, SalaryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Wish, WishAdmin)
