from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from app.models import SubscriptionPlan, ApiToken, User, UserSubscription
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from genesis.utils import current_timestamp
from datetime import timedelta
from django.db import transaction
from app.mixins import LoginAuthTokenVerificationMixin


@method_decorator(csrf_exempt, name="dispatch")
class UserSuscriptionDetailView(LoginAuthTokenVerificationMixin, View):
    def post(self, request):
        try:
            actor = request.actor
            user_id = actor.id

            body = JSONParser().parse(request)
            plan = body.get("plan", None)

            if not plan:
                return JsonResponse({
                    "error": "PLAN_REQUIRED",
                    "message": "Subscription plan must be provided to generate a token."
                }, status=400)
            
            user = User.objects.get(id=user_id)
            if not user.is_active:
                return JsonResponse({
                    "error":"USER_INACTIVE",
                    "message":"This user account is inactive. Please contact support."
                }, status = status.HTTP_403_FORBIDDEN)
            
            subscription_plan = get_object_or_404(SubscriptionPlan, type=plan)
            additional_days = int(timedelta(days=subscription_plan.validity_days).total_seconds() * 1000)  #millisecond
            expires_at = current_timestamp() + additional_days
            
            
            with transaction.atomic():
                # if subscription exists first mark it as inactive
                UserSubscription.objects.filter(user=user, active=True).update(active=False)
                
                user_subscription = UserSubscription.objects.create(
                    plan=subscription_plan,
                    user = user,
                    expires_at = expires_at
                )

            user_subscription.save()

            return JsonResponse({
                    "error":None,
                    "message":"User subscribed to plan successfully."
                }, status=status.HTTP_200_OK)
        
        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": "Provided subscription plan does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print(e)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while subscribing to plan. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        try:
            actor = request.actor
            user_id = actor.id
            user = User.objects.get(id=user_id)
            if not user.is_active:
                return JsonResponse({
                    "error":"USER_INACTIVE",
                    "message":"This user account is inactive. Please contact support."
                }, status = status.HTTP_403_FORBIDDEN)
            
            active_subscription = UserSubscription.objects.filter(user=user, active=True).first()

            if active_subscription:
                return JsonResponse({
                    "error": None,
                    "message": "Active subscription detail fetched successfully",
                    "data": {
                        "id": active_subscription.id,
                        "plan": active_subscription.plan.type,   # adjust field name
                        "start_date": active_subscription.created_at,
                        "end_date": active_subscription.expires_at,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return JsonResponse({
                    "error": "NO_ACTIVE_SUBSCRIPTION",
                    "message": "No active subscription found for this user."
                }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while getting subscription details. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
