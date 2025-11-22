from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from app.models.metadata import ReferenceCodes, PermitType, StandardLabels
from app.mixins import ApiTokenValidityCheckMixin


def success_response(message, data=None, status=200):
    return JsonResponse({
        "error": None,
        "message": message,
        "data": data
    }, status=status)


def error_response(message, status=400):
    return JsonResponse({
        "error": message,
        "message": None,
        "data": None
    }, status=status)


@method_decorator(csrf_exempt, name="dispatch")
class ReferenceCodesView(ApiTokenValidityCheckMixin, View):
    def get(self, request, id=None):
        if id:
            try:
                code = ReferenceCodes.objects.get(id=id)
                return success_response("Reference code fetched successfully", model_to_dict(code))
            except ReferenceCodes.DoesNotExist:
                return error_response("Reference code not found", 404)
        codes = list(ReferenceCodes.objects.values())
        return success_response("Reference codes fetched successfully", codes)

    def post(self, request):
        try:
            data = json.loads(request.body)
            code = ReferenceCodes.objects.create(
                code=data.get("code"),
                description=data.get("description")
            )
            return success_response("Reference code created successfully", model_to_dict(code), 201)
        except Exception as e:
            return error_response(str(e))

    def patch(self, request, id=None):
        if not id:
            return error_response("ID is required for update")
        try:
            code = ReferenceCodes.objects.get(id=id)
            data = json.loads(request.body)
            for field, value in data.items():
                setattr(code, field, value)
            code.save()
            return success_response("Reference code updated successfully", model_to_dict(code))
        except ReferenceCodes.DoesNotExist:
            return error_response("Reference code not found", 404)
        except Exception as e:
            return error_response(str(e))


@method_decorator(csrf_exempt, name="dispatch")
class PermitTypeView(ApiTokenValidityCheckMixin, View):
    def get(self, request, id=None):
        if id:
            try:
                permit = PermitType.objects.get(id=id)
                return success_response("Permit type fetched successfully", model_to_dict(permit))
            except PermitType.DoesNotExist:
                return error_response("Permit type not found", 404)
        permits = list(PermitType.objects.values())
        return success_response("Permit types fetched successfully", permits)

    def post(self, request):
        try:
            data = json.loads(request.body)
            permit = PermitType.objects.create(type=data.get("type"))
            return success_response("Permit type created successfully", model_to_dict(permit), 201)
        except Exception as e:
            return error_response(str(e))

    def patch(self, request, id=None):
        if not id:
            return error_response("ID is required for update")
        try:
            permit = PermitType.objects.get(id=id)
            data = json.loads(request.body)
            for field, value in data.items():
                setattr(permit, field, value)
            permit.save()
            return success_response("Permit type updated successfully", model_to_dict(permit))
        except PermitType.DoesNotExist:
            return error_response("Permit type not found", 404)
        except Exception as e:
            return error_response(str(e))


@method_decorator(csrf_exempt, name="dispatch")
class StandardLabelsView(ApiTokenValidityCheckMixin, View):
    def get(self, request, id=None):
        if id:
            try:
                label = StandardLabels.objects.get(id=id)
                return success_response("Standard label fetched successfully", model_to_dict(label))
            except StandardLabels.DoesNotExist:
                return error_response("Standard label not found", 404)
        labels = list(StandardLabels.objects.values())
        return success_response("Standard labels fetched successfully", labels)

    def post(self, request):
        try:
            data = json.loads(request.body)
            label = StandardLabels.objects.create(
                name=data.get("name"),
                always_required=data.get("always_required", False)
            )
            return success_response("Standard label created successfully", model_to_dict(label), 201)
        except Exception as e:
            return error_response(str(e))

    def patch(self, request, id=None):
        if not id:
            return error_response("ID is required for update")
        try:
            label = StandardLabels.objects.get(id=id)
            data = json.loads(request.body)
            for field, value in data.items():
                setattr(label, field, value)
            label.save()
            return success_response("Standard label updated successfully", model_to_dict(label))
        except StandardLabels.DoesNotExist:
            return error_response("Standard label not found", 404)
        except Exception as e:
            return error_response(str(e))
