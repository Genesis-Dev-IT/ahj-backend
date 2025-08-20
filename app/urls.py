from django.urls import path
from app.views.health import HealthCheck

urlpatterns = [
    path('health', HealthCheck.as_view(), name='health-check'),
]
