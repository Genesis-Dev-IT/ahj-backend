import secrets
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from app.models import PlanQuota, ApiToken
from app.models import User 
from django.http import Http404
from django.shortcuts import get_object_or_404

@method_decorator(csrf_exempt, name="dispatch")
class APITokenDetailView(View):
    def post(self, request):
        try:
            # i will get type of plan, user_id
            body = JSONParser().parse(request)
            plan = body.get("plan", None)
            user_id = body.get("user_id", None)
            if not plan:
                return JsonResponse({
                    "error": "PLAN_REQUIRED",
                    "message": "Subscription plan must be provided to generate a token."
                }, status=400)
            
            user = User.objects.get(id=user_id)
            plan_quota = get_object_or_404(PlanQuota, plan=plan)
            plain_token = secrets.token_urlsafe(32)
            
            token_obj = ApiToken.objects.create(
                user=user,
                plan=plan,
                token_hash=plain_token,
                max_calls=plan_quota.monthly_limit,
            )

            return JsonResponse({
                "error":None,
                "message":"API token generated successfully.",
                "data": {
                    "plan": plan_quota.plan,
                    "max_calls": plan_quota.monthly_limit,
                    "expires_at": token_obj.expires_at,
                    "token": plain_token
                }
            }, status=200)
        
        except Http404:
            return JsonResponse({
                "error": "PLAN_REQUIRED",
                "message": "Subscription plan must be provided to generate a token."
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while generating the token. Please try again later."
            }, status=500)