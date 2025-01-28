from rest_framework import routers
from .views.views import ProjectViewSet, UnitViewSet, CustomerViewSet

router = routers.DefaultRouter()

router.register('api/projects', ProjectViewSet, 'projects')
router.register('api/units', UnitViewSet, 'units')
router.register('api/customers', CustomerViewSet, 'customers')


urlpatterns = router.urls