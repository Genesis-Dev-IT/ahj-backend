from django.urls import path
from app.views.health import HealthCheck
from app.views.user import UserDetailView

urlpatterns = [
    path('health', HealthCheck.as_view(), name='health-check'),
    path('v1/user', UserDetailView.as_view(), name='create-user'),
    path('v1/user/<int:id>', UserDetailView.as_view(), name='get-user'),
]
