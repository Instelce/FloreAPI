import random

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from flore.filters import PlantSearchFilter
from rest_framework.response import Response

from flore.models import Image, Plant
from flore.serializers import *
from flore.permissions import IsSuperUser
from flore.mixins import PermissionPolicyMixin


class FamilyView(APIView):
    def get(self, request, format=None):
        if 'ordering' in request.query_params:
            families = Family.objects.order_by(request.query_params['ordering'])
        else:
            families = Family.objects.all()
        serializer = PlantFamilySerializer(families, many=True)
        return Response(serializer.data)


class GenreView(APIView):
    def get(self, request, format=None):
        if 'ordering' in request.query_params:
            genres = Genre.objects.order_by(request.query_params['ordering'])
        else:
            genres = Genre.objects.all()
        serializer = PlantGenreSerializer(genres, many=True)
        return Response(serializer.data)


class PlantModelViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Plant.objects.select_related("family", "genre")
    pagination_class = PageNumberPagination

    permission_classes = [AllowAny]
    permission_classes_per_method = {
        "create": [IsSuperUser],
        "destroy": [IsSuperUser],
        "update": [IsSuperUser],
        "partial_update": [IsSuperUser],
    }

    filter_backends = (PlantSearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ("family", "genre", "scientific_name", "correct_name", "french_name")
    filterset_fields = ("rank_code", "family__name", "genre__name", "author")

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

    permission_classes = [AllowAny]
    permission_classes_per_method = {
        "create": [IsSuperUser],
        "destroy": [IsSuperUser],
        "update": [IsSuperUser],
        "partial_update": [IsSuperUser],
    }

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadImageSerializer
        return WriteImageSerializer


class GetRandomPlantsView(APIView):
    def get(self, request, number, format=None):
        ids = []
        plants = []
        min_id = None
        max_id = None

        if 'family' in self.request.query_params.keys():
            plants_data = Plant.objects.all().filter(family__name__exact=self.request.query_params.get('family'))
            for plant in plants_data:
                ids.append(plant.id)
        else:
            min_id = Plant.objects.order_by('id')[0].id
            max_id = Plant.objects.order_by('-id')[0].id

        for i in range(number):
            if 'family' in self.request.query_params.keys():
                random_id = random.choice(ids)
            else:
                random_id = random.randint(min_id, max_id)
            plant = Plant.objects.filter(id=random_id)[0]

            while plant in plants:
                if 'family' in self.request.query_params.keys():
                    random_id = random.choice(ids)
                else:
                    random_id = random.randint(min_id, max_id)
                plant = Plant.objects.filter(id=random_id)[0]

            plants.append(Plant.objects.filter(id=random_id)[0])

        serializer = ReadPlantSerializer(plants, many=True)
        return Response(serializer.data)
