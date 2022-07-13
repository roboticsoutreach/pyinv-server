"""API URLs for assets."""

from rest_framework.routers import SimpleRouter

from .views import (
    asset_events,
    asset_models,
    assets,
    manufacturers,
    nodes,
)

router = SimpleRouter()
router.register('assets', assets.AssetViewSet, basename='assets')
router.register('asset-events', asset_events.AssetEventViewSet, basename="asset-events")
router.register('asset-models', asset_models.AssetModelViewSet, basename='asset-models')
router.register('manufacturers', manufacturers.ManufacturerViewSet, basename='manufacturers')
router.register('nodes', nodes.NodeViewSet, basename='nodes')

urlpatterns = router.urls
