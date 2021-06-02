from django.db import models
from django.db.models import CASCADE, Sum
from django.utils.timezone import now

from users.models import User


class Salary(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True, related_name='salary')
    start_salary = models.FloatField(verbose_name='Start salary', default=0, null=True, blank=True)
    end_salary = models.FloatField(verbose_name='End salary', default=0, null=True, blank=True)
    total_salary = models.FloatField(verbose_name='Total salary', default=0, null=True, blank=True)
    salary_date = models.DateField(verbose_name='Salary Date', default=now)
    month = models.CharField(default='', max_length=256, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=CASCADE, null=True, blank=True, related_name='history_records')
    history = models.BooleanField('History', default=False)
    created = models.DateTimeField('Date created', default=now)

    def __str__(self):
        return "%s" % (str(self.id))

    class Meta(object):
        verbose_name = 'Salary'
        verbose_name_plural = 'Salary'

    def count_total_salary(self):
        # сюди приходить правильна end_salary але total_salary ще не встигає змінитися і тому тотал для останнього обєкта рахується із помилкою.
        print(f'self: {self} with end_salary {self.end_salary} and total of {self.total_salary}')
        # print(f'self.end_salary in models: {self.end_salary}')
        prev_salaries = Salary.objects.filter(user=self.user, history=True)
        total_history_salary = prev_salaries.aggregate(total_history_salary=Sum('end_salary'))['total_history_salary']

        if self in prev_salaries:
            current_salary_object = Salary.objects.filter(user=self.user, history=False)
            current_salary = current_salary_object.values_list('end_salary', flat=True)[0]

            total_salary = total_history_salary + current_salary
            total_salary = 0 if total_salary is None else total_salary
            print(f'current salary: {current_salary}')
            print(f'total_history_salary: {total_history_salary}')
            print(f'total salary: {total_salary}')
            current_salary_object.update(total_salary=total_salary)
            # return total_salary
            return self.end_salary

        if total_history_salary:
            total_salary = total_history_salary + self.end_salary
            total_salary = 0 if total_salary is None else total_salary
            print(f'total salary in models: {total_salary}')
            return total_salary
        else:
            total_salary = self.end_salary
            return total_salary


class Category(models.Model):
    name = models.CharField(verbose_name='Name', default='', max_length=256, null=True, blank=True)

    def __str__(self):
        return "%s" % (str(self.name))

    class Meta(object):
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True, related_name='expense')
    name = models.CharField(verbose_name='Name', default='', max_length=256, null=True, blank=True)
    price = models.FloatField(verbose_name='Price', default=0, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=CASCADE, null=True, blank=True, related_name='expense')
    date = models.DateField(verbose_name='Date', default=now)
    salary = models.ForeignKey(Salary, on_delete=CASCADE, null=True, blank=True, related_name='expense')

    def __str__(self):
        return "%s" % (str(self.id))

    class Meta(object):
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'


class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True, related_name='wish')
    name = models.CharField(verbose_name='Name', default='', max_length=256, null=True, blank=True)
    link = models.URLField(verbose_name='Link', null=True, blank=True)
    price = models.FloatField(verbose_name='Price', default=0, null=True, blank=True)
    priority = models.PositiveSmallIntegerField(verbose_name="Wish's priority", default=0, null=True, blank=True)

    def __str__(self):
        return "%s" % (str(self.id))

    class Meta(object):
        verbose_name = 'Wish'
        verbose_name_plural = 'Wishes'
