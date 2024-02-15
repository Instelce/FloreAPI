import random

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from flore.filters import PlantSearchFilter
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
    search_fields = ("french_name",)
    ordering_fields = ("family", "genre", "scientific_name", "correct_name", "french_name")
    filterset_fields = ("rank_code", "family__name", "genre__name", "author")

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadPlantSerializer
        return WritePlantSerializer


class GetRandomPlantsView(APIView):
    def get(self, request, number, format=None):
        ids = []
        plants = []
        min_id = None
        max_id = None

        # Params
        family = 'family' in self.request.query_params.keys()
        include_images = 'images' in self.request.query_params.keys() and self.request.query_params['images'] == 'true'

        # Filter by family
        if family:
            plants_data = Plant.objects.all().filter(family__name__exact=self.request.query_params.get('family'))
            for plant in plants_data:
                ids.append(plant.id)
        else:
            min_id = Plant.objects.order_by('id')[0].id
            max_id = Plant.objects.order_by('-id')[0].id

        # Get random plants
        i = 0
        while i < number:
            if family:
                random_id = random.choice(ids)
            else:
                random_id = random.randint(min_id, max_id)

            if Plant.objects.filter(id=random_id).count() > 0:
                plant = self.get_plant_data(Plant.objects.filter(id=random_id)[0], include_images)

                while plant in plants:
                    if family:
                        random_id = random.choice(ids)
                    else:
                        random_id = random.randint(min_id, max_id)
                    plant = self.get_plant_data(Plant.objects.filter(id=random_id)[0], include_images)

                plants.append(plant)
                i += 1

        serializer = CompletePlantImagesSerializer(plants, many=True)
        return Response(serializer.data)

    @staticmethod
    def get_plant_data(plant, include_images=False):
        plant_data = {
            'id': plant.id,
            'french_name': plant.french_name,
            'family': plant.family,
            'genre': plant.genre,
            'scientific_name': plant.scientific_name,
            'correct_name': plant.correct_name,
            'author': plant.author,
            'publ_year': plant.publ_year,
            'eflore_url': plant.eflore_url,
            'images': []
        }

        if include_images:
            plant_data['images'] = ReadImageNoPlantSerializer(
                Image.objects.filter(plant_id=plant.id), many=True
            ).data

        return plant_data


class PlantsIdsListView(APIView):
    def get(self, request, format=None):
        if 'ids' in request.query_params.keys():
            ids = [int(id) for id in request.query_params['ids'].split(',')]
            plants = []

            for id in ids:
                print(id)
                plants.append(Plant.objects.filter(id=id)[0])

            for plant in plants:
                print(plant.french_name)

            serializer = ReadPlantSerializer(plants, many=True)
            return Response(serializer.data)
        return Response({"detail": "'ids' query param is missing"})


class ImageModelViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Image.objects.select_related("plant")
    pagination_class = PageNumberPagination

    permission_classes = [AllowAny]
    permission_classes_per_method = {
        "create": [IsSuperUser],
        "destroy": [IsSuperUser],
        "update": [IsSuperUser],
        "partial_update": [IsSuperUser],
    }

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("publ_date",)
    filterset_fields = ("plant__id", "plant__french_name", "organ")

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadImageSerializer
        return WriteImageSerializer


class PlantsIdsListImagesView(APIView):
    def get(self, request, format=None):
        if 'ids' in request.query_params.keys():
            ids = [int(id) for id in request.query_params['ids'].split(',')]
            data = []

            for id in ids:
                print(id)
                data.append({
                    'id': id,
                    'images': Image.objects.filter(plant_id=id)
                })

            serializer = PlantImagesSerializer(data, many=True)
            return Response(serializer.data)
        return Response({"detail": "'plants_ids' query param is missing"})


class ImagesIdsListView(APIView):
    def get(self, request, format=None):
        if 'ids' in request.query_params.keys():
            ids = [int(id) for id in request.query_params['ids'].split(',')]
            images = []

            for id in ids:
                images.append(Image.objects.get(id=id))

            if 'with_plants' in request.query_params.keys() and request.query_params['with_plants'] == 'true':
                serializer = ReadImageSerializer(images, many=True)
            else:
                serializer = ReadImageNoPlantSerializer(images, many=True)

            return Response(serializer.data)
        return Response({"detail": "'ids' query param is missing"})
