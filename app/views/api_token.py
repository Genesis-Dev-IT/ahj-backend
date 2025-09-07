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
class APITokenDetailView(LoginAuthTokenVerificationMixin, View):
    def post(self, request):
        try:
            actor = request.actor
            user_id = actor.id
            user = User.objects.get(id=user_id)
            
            with transaction.atomic():
                # Delete any existing token for this user
                ApiToken.objects.filter(user=user).delete()
                
                user_subscription = UserSubscription.objects.get(user=user, active=True)
                subscription_plan = SubscriptionPlan.objects.get(id = user_subscription.plan.id)
                
                token_obj = ApiToken.objects.create(
                    user=user,
                    limit = subscription_plan.limit,
                    expires_at=user_subscription.expires_at,
                    created_by = actor,
                    updated_by = actor
                )

                return JsonResponse({
                    "error":None,
                    "message":"API token generated successfully.",
                    "data": {
                        "plan": subscription_plan.type,
                        "expires_at": token_obj.expires_at,
                        "token": token_obj.token
                    }
                }, status=200)
            
        except UserSubscription.DoesNotExist:
            return JsonResponse({
                    "error": "NOT_FOUND",
                    "message": "You must have an active subscription to generate a token."
                }, status=status.HTTP_404_NOT_FOUND)
        
        except SubscriptionPlan.DoesNotExist:
            return JsonResponse({
                    "error": "NOT_FOUND",
                    "message": "Plan attached to subscription does not exists."
                }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print(e)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while generating token. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request):
        try:
            # we can only deactivate the token 
            body = JSONParser().parse(request)
            user_id = body.get("user_id")

            # fetch user
            user = User.objects.get(id=user_id)

            if not user.is_active:
                return JsonResponse({
                    "error": "USER_INACTIVE",
                    "message": "This user account is inactive. Please contact support."
                }, status=status.HTTP_403_FORBIDDEN)

            # fetch token
            token = get_object_or_404(ApiToken, user=user)
            if token.active == False:
                return JsonResponse({
                    "error": None,
                    "message":"API token is already disabled."
                }, status=status.HTTP_200_OK)
            
            token.active = False
            token.updated_by = user
            token.save()

            return JsonResponse({
                "error": None,
                "message": "API token disabled successfully."
            }, status=status.HTTP_200_OK)

        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": "API token not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print(e)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while updating the token."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request):
        try:
            body = JSONParser().parse(request)
            user_id = body.get("user_id")
            user = get_object_or_404(User, id=user_id)

            deleted_count, _ = ApiToken.objects.filter(user=user).delete()

            if deleted_count == 0:
                return JsonResponse({
                    "error": "NOT_FOUND",
                    "message": f"No API token found for user with id {user_id}"
                }, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({
                "error": None,
                "message": "API token deleted successfully."
            }, status=status.HTTP_200_OK)

        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"User with id {user_id} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("Unexpected error:", e)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while deleting the token. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)