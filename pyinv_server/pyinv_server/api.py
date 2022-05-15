import assets.api
from rest_framework import routers

router = routers.DefaultRouter()
router.register('assets/manufacturers', assets.api.ManufacturerViewSet)
