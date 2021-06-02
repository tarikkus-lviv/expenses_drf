from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, ExpenseViewSet, SalaryViewSet, WishViewSet

router = SimpleRouter()
router.register("expenses", ExpenseViewSet)
router.register("categories", CategoryViewSet)
router.register("salary", SalaryViewSet)
router.register("wish", WishViewSet)
