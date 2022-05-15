from rest_framework import viewsets

from .models import AssetModel, Manufacturer
from .serializers import AssetModelSerializer, ManufacturerSerializer


class AssetModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AssetModels to be viewed or edited.
    """
    queryset = AssetModel.objects.all()
    serializer_class = AssetModelSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows manufacturers to be viewed or edited.
    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
