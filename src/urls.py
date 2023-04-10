from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('flore.urls')),
    path('login/', views.obtain_auth_token, name='obtain-auth-token')
]
