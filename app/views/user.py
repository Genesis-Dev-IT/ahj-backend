from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(View):
    def get(self, request):
        try:
            return JsonResponse({"message":"health check successfull"}, status=200)
        except Exception as e:
            pass