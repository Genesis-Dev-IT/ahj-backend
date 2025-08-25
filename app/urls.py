from django.urls import path
from app.views.health import HealthCheck
from app.views.api_token import APITokenDetailView
urlpatterns = [
    path('health', HealthCheck.as_view(), name='health-check'),
    path('v1/api-token', APITokenDetailView.as_view(), name='api-token-detail'),
]
