import datetime
from expenses.celery import app
from expenses.utils import utils

from expenses_api.models import Expense
from users.models import User


@app.task()
def email_reminder():
    """Task to send emails to users if they did not fill in any expenses Today."""
    today = datetime.datetime.today()

    # this woooorks!! треба тепер перевіряти чи на сьогодні юзер заповнював чи ні і якщо ні то слати мило!

    users = User.objects.filter(role=2, is_receiving_notifications=True)
    today_expenses = Expense.objects.filter(date=today)
    today_users = User.objects.filter(expense__date=today, is_receiving_notifications=True)

    print(f'all users: {users}')
    print(f'users that filled up today: {today_users}')
    print(f'expenses that filled up today: {today_expenses}')

    for i in users:
        if i not in today_users:
            email_factory = utils.ExpensesReminderEmailFactory.from_request(i, user=i, **{})
            email = email_factory.create()
            email.send()
            print('email sent successfully')
        else:
            print(f'{i.email} reported today!')

