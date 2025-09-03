from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from app.models import User, ApiToken
from rest_framework.parsers import JSONParser
from app.serializer import UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from genesis.utils import chain_errors
from django.db import transaction
from genesis.utils import current_timestamp
@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(View):
    def post(self, request):
        try:
            # user can be created by admin only

            body = JSONParser().parse(request)
            serializer = UserSerializer(data=body)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(
                    {
                        "error":None,
                        "message":"User created successfully",
                        "data":serializer.data
                    }, status=status.HTTP_201_CREATED
                )

            # error_messages = list(chain.from_iterable(serializer.errors.values()))
            error_messages = chain_errors(serializer.errors.values())
            return JsonResponse(
                {
                    "error": "VALIDATION_ERROR",
                    "message": " | ".join(error_messages)
                },
                status=status.HTTP_400_BAD_REQUEST
            )   
        except Exception as e:
            print(e)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while creating user. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            serializer = UserSerializer(user)
            return JsonResponse(
                {
                    "error":None,
                    "message":"User data fetched successfully",
                    "data":serializer.data
                },
                status=status.HTTP_200_OK, safe=False)

        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"User with id {id} does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Unexpected error:", e)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching user. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            body = JSONParser().parse(request)

            # check if the actor is admin then we can update is_active as well

            with transaction.atomic():
                serializer = UserSerializer(user, data=body, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    # if user becomes inactive then we will have to mark the token as inactive
                    if "is_active" in body:
                        tokens = ApiToken.objects.filter(user=user, active=True)
                        if tokens.exists():
                            tokens.update(
                                active=body["is_active"],
                                updated_by=user,
                                updated_at=current_timestamp()
                            )
                        else:
                            print(f"No active token found for user {user.id}")

                    return JsonResponse({
                        "error":None,
                        "message": "User updated successfully.",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)
                
                error_messages = chain_errors(serializer.errors.values())
                return JsonResponse({
                    "error": "VALIDATION_ERROR",
                    "message": " | ".join(error_messages)
                }, status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"User with id {id} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("Unexpected error:", e)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while updating user. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, id):
        try:
            # user can be deleted by admin only
            user = get_object_or_404(User, id=id)
            user.delete()
            return JsonResponse({
                "error":None,
                "message": f"User with id {id} deleted successfully."
            }, status=status.HTTP_200_OK)

        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"User with id {id} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("Unexpected error:", e)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while deleting user. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserListView(View):
    def get(seld, request):
        pass