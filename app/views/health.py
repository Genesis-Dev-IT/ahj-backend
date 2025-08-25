from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from app.utils import ApiTokenRequiredMixin
@method_decorator(csrf_exempt, name="dispatch")
class HealthCheck(ApiTokenRequiredMixin, View):
    def get(self, request):
        return JsonResponse({"message":"health check successfull"}, status=200)
