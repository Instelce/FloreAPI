from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from flore.models import Image, Plant
from flore.serializers import *
from flore.permissions import IsSuperUser
from flore.mixins import PermissionPolicyMixin


class PlantModelViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Plant.objects.all()
    pagination_class = PageNumberPagination

    permission_classes = [IsAuthenticated]
    permission_classes_per_method = {
        "create": [IsSuperUser],
        "destroy": [IsSuperUser],
        "partial_update": [IsSuperUser],
    }

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("num_inpn", "rank_code", "family", "genre", "scientific_name", "correct_name", "french_name", "author")
    ordering_fields = ("family", "genre", "scientific_name", "correct_name", "french_name")
    filterset_fields = ("rank_code", "family", "genre", "author")

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadPlantSerializer
        return WritePlantSerializer


class ImageModelViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Image.objects.select_related("plant")
    pagination_class = PageNumberPagination

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ("publ_date")
    filterset_fields = ("plant__id", "organ")

    permission_classes = [IsAuthenticated]
    permission_classes_per_method = {
        "create": [IsSuperUser],
        "destroy": [IsSuperUser],
        "partial_update": [IsSuperUser],
    }

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadImageSerializer
        return WriteImageSerializer
