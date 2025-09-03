from rest_framework import serializers
from app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "is_active", "is_admin", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False, "error_messages": {"blank": "First name cannot be empty.", "required": "First name is required."}},
            "last_name": {"required": True, "allow_blank": False, "error_messages": {"blank": "Last name cannot be empty.", "required": "Last name is required."}},
            "email": {"required": True, "allow_blank": False, "error_messages": {"blank": "Email cannot be empty.", "required": "Email is required."}},
        }

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        return value

    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Last name cannot be empty.")
        return value

    def validate_email(self, value):
        if not value or "@" not in value:
            raise serializers.ValidationError("Invalid email address.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate(self, data):
        """
        Extra cross-field validation (replicates SQL CHECK constraint).
        """
        if self.instance and "email" in data:
            raise serializers.ValidationError(
                {"email": "Email cannot be updated once set."}
            )
        
        if self.instance and "is_admin" in data:
            raise serializers.ValidationError(
                {"is_admin": "is_admin cannot be updated"}
            )
        
        email = data.get("email", self.instance.email if self.instance else None)
        is_admin = data.get("is_admin", self.instance.is_admin if self.instance else False)

        if is_admin and not email.endswith("@genesisdesign.io"):
            raise serializers.ValidationError(
                {"email": "Admin users must have an @genesisdesign.io email address."}
            )
        return data
