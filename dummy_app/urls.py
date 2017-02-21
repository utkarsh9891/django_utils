from rest_framework.routers import SimpleRouter
from dummy_app.views import LoggingDemoViewSet

router = SimpleRouter()
router.register('logging', LoggingDemoViewSet, base_name='logging')

urlpatterns = router.urls
