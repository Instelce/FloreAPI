from django.urls import include, path
from rest_framework.routers import SimpleRouter

from flore.views import *

router = SimpleRouter(trailing_slash=False)
router.register(r'plants', PlantModelViewSet, basename='plants')
router.register(r'images', ImageModelViewSet, basename='images')


urlpatterns = [
    path('', include(router.urls)),
    path('families', FamilyView.as_view(), name='families'),
    path('genres', GenreView.as_view(), name='genres'),
    path('plants-list', PlantsIdsListView.as_view(), name='plants-ids-list'),
    path('plants-list/images', PlantsIdsListImagesView.as_view(), name='plants-ids-list-images'),
    path('images-list', ImagesIdsListView.as_view(), name='images-ids-list'),
    path('plants/random/<int:number>', GetRandomPlantsView.as_view(), name='random-plants'),
]
