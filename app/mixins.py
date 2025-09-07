from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from app.models import ApiToken, ApiUsage
from genesis.utils import current_timestamp
from genesis.supabase_client import get_supabase_client
import jwt
import os
from django.shortcuts import get_object_or_404
from app.models import User
from django.http import Http404
from rest_framework import status
import json
import logging
from supabase import AuthApiError

logger = logging.getLogger(__name__)

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET") 

class ApiTokenValidityCheckMixin:
    """Mixin to enforce API token validation and quota checking."""

    def dispatch(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header:
            return JsonResponse({
                "error": "MISSING_TOKEN",
                "message": "Authorization token is required.",
            }, status=401)

        if not auth_header.startswith("Bearer "):
            return JsonResponse({
                "error": "INVALID_AUTH_HEADER",
                "message": "Authorization header must be in format: Bearer <token>",
            }, status=401)

        plain_token = auth_header.split("Bearer ")[1].strip()

        # 1. Check token existence + active
        try:
            api_token = ApiToken.objects.select_related("user", "plan").get(
                token=plain_token, active=True
            )
        except ApiToken.DoesNotExist:
            return JsonResponse({
                "error": "INVALID_TOKEN",
                "message": "API token is invalid or inactive."
            }, status=401)

        # 2. Check expiry
        if current_timestamp() > api_token.expires_at:
            return JsonResponse({
                "error": "TOKEN_EXPIRED",
                "message": "API token has expired."
            }, status=401)

        # 3. Check if user is active
        if not api_token.user or not api_token.user.is_active:
            return JsonResponse({
                "error": "USER_INACTIVE",
                "message": "Associated user account is inactive."
            }, status=403)

        # 4. Quota check from ApiUsage table
        usage_count = ApiUsage.objects.filter(
            user=api_token.user,
            created_at__gte=api_token.created_at,
            created_at__lte=current_timestamp()
        ).count()

        if usage_count >= api_token.limit:
            return JsonResponse({
                "error": "QUOTA_EXCEEDED",
                "message": "API call limit has been reached for this token.",
            }, status=429)

        # Attach token for use inside the view
        request.api_token = api_token

        return super().dispatch(request, *args, **kwargs)
    

class LoginAuthTokenVerificationMixin:
    def dispatch(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse(
                {"error": "AUTH_ERROR", "message": "Authorization header missing or invalid"},
                status=401,
            )

        token = auth_header.split(" ")[1]

        try:
            # Verify JWT using Supabase JWT secret
            if not is_token_authenticated(token):
                return JsonResponse(
                    {
                        "error": "INVALID_TOKEN",
                        "message": "Token not authenticated"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            supabase_client = get_supabase_client()
            supabase_user_response = None

            try:
                supabase_user_response = supabase_client.auth.get_user(token)
            except AuthApiError as e:  # Handles expired/invalid token
                return JsonResponse(
                    {"error": "TOKEN_EXPIRED", "message": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not supabase_user_response or not hasattr(supabase_user_response, "user"):
                return JsonResponse(
                    {"error": "AUTH_ERROR", "message": "Failed to fetch user from Supabase"},
                    status=401,
            )

            supabase_user = json.loads(supabase_user_response.model_dump_json())
            email = supabase_user.get("user", {}).get("email")

            if not email:
                return JsonResponse(
                    {"error": "AUTH_ERROR", "message": "No email found in Supabase user"},
                    status=401,
                )

            
            user = get_object_or_404(User, email=email)
             # --- permission enforcement ---
            view = self.__class__
            method = request.method.upper()

            if hasattr(view, "permissions"):
                perms = view.permissions.get(method)
                if perms:
                    if perms.get("is_admin", False) and not user.is_admin:
                        return JsonResponse(
                            {
                                "error": "FORBIDDEN",
                                "message": "Admin privileges required for this operation.",
                            },
                            status=403,
                        )

            request.actor=user
        
        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"User with id {id} does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Unexpected error in LoginAuthTokenVerificationMixin:", str(e))
            return JsonResponse(
                {"error": "SERVER_ERROR", "message": "Something went wrong during authentication"},
                status=500,
            )
        # Continue to the view
        return super().dispatch(request, *args, **kwargs)
    



def is_token_authenticated(token):
    if not token:
        return False
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    try:
        if 'aud' in decoded_token and 'role' in decoded_token:
            if decoded_token['aud'] != 'authenticated' and "authenticated" not in decoded_token['aud']:
                return False
            if decoded_token['role'] != 'authenticated':
                return False
            return True
        return False
    except Exception as e:
        logger.warning(f"Error during token authentication check: {e}")
        return False
