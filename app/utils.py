from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import hashlib
from app.models import ApiToken
from genesis.utils import current_timestamp


class ApiTokenRequiredMixin:
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

        # token_hash = hashlib.sha256(plain_token.encode()).hexdigest()
        try:
            api_token = ApiToken.objects.get(token_hash=plain_token, active=True)
        except ApiToken.DoesNotExist:
            return JsonResponse({
                "error": "INVALID_TOKEN",
                "message": "API token is invalid or inactive."
            }, status=401)

        if current_timestamp() > api_token.expires_at:
            return JsonResponse({
                "error": "TOKEN_EXPIRED",
                "message": "API token has expired."
            }, status=401)

        if api_token.call_count >= api_token.max_calls:
            return JsonResponse({
                "error": "QUOTA_EXCEEDED",
                "message": "API call limit has been reached for this token.",
            }, status=429)

        # Increment usage
        api_token.call_count += 1
        api_token.save(update_fields=["call_count", "updated_at"])

        # Attach token for use inside the view
        request.api_token = api_token

        return super().dispatch(request, *args, **kwargs)
