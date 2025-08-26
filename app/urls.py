from django.urls import path
from app.views.health import HealthCheck
from app.views.user import UserDetailView
from app.views.ahj import AHJDetailView
from app.views.utility import UtilityDetailView
from app.views.zipcode import ZipCodeAHJUtilityMappingDetailView

urlpatterns = [
    path('health', HealthCheck.as_view(), name='health-check'),
    path('v1/user', UserDetailView.as_view(), name='create-user'),
    path('v1/user/<int:id>', UserDetailView.as_view(), name='get-user'),
    path('v1/ahj/<int:id>', AHJDetailView.as_view(), name='ahj-detail'),
    path('v1/utility/<int:id>', UtilityDetailView.as_view(), name='utility-detail'),
    path('v1/zipcode/<str:id>', ZipCodeAHJUtilityMappingDetailView.as_view(), name='ahj-utility-for-a-zipcode'),
]
