from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from app.models import ApiToken, ApiUsage
from genesis.utils import current_timestamp

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
        
        # validity_days = api_token.plan.validity_days
        # start_window = current_timestamp() - (validity_days * 24 * 60 * 60 * 1000)

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
