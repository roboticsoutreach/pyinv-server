"""API URLs for assets."""

from rest_framework.routers import SimpleRouter

from .views import assets

router = SimpleRouter()
router.register('assets', assets.AssetViewSet, basename='assets')

urlpatterns = router.urls
