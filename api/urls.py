from .views import get_active_version
from django.urls import path
from rest_framework import routers

urlpatterns = [
  path('get_active/', get_active_version)
]

router = routers.DefaultRouter()
(
)

urlpatterns = urlpatterns + router.urls