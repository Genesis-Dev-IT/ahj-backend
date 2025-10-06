from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from app.models.metadata import ReferenceCodes, PermitType, StandardLabels
from app.mixins import ApiTokenValidityCheckMixin


@method_decorator(csrf_exempt, name="dispatch")
class ReferenceCodesView(ApiTokenValidityCheckMixin, View):
    def get(self, request, id=None):
        if id:
            try:
                code = ReferenceCodes.objects.get(id=id)
                return JsonResponse(model_to_dict(code), status=200)
            except ReferenceCodes.DoesNotExist:
                return JsonResponse({"error": "Reference code not found"}, status=404)

        codes = list(ReferenceCodes.objects.values())
        return JsonResponse(codes, safe=False, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            code = ReferenceCodes.objects.create(
                type=data.get("type"),
                code_name=data.get("code_name"),
                description=data.get("description")
            )
            return JsonResponse(model_to_dict(code), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def patch(self, request, id=None):
        if not id:
            return JsonResponse({"error": "ID is required for update"}, status=400)
        try:
            code = ReferenceCodes.objects.get(id=id)
            data = json.loads(request.body)
            for field, value in data.items():
                setattr(code, field, value)
            code.save()
            return JsonResponse(model_to_dict(code), status=200)
        except ReferenceCodes.DoesNotExist:
            return JsonResponse({"error": "Reference code not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class PermitTypeView(ApiTokenValidityCheckMixin, View):
    def get(self, request, id=None):
        if id:
            try:
                permit = PermitType.objects.get(id=id)
                return JsonResponse(model_to_dict(permit), status=200)
            except PermitType.DoesNotExist:
                return JsonResponse({"error": "Permit type not found"}, status=404)

        permits = list(PermitType.objects.values())
        return JsonResponse(permits, safe=False, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            permit = PermitType.objects.create(
                type=data.get("type")
            )
            return JsonResponse(model_to_dict(permit), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def patch(self, request, id=None):
        if not id:
            return JsonResponse({"error": "ID is required for update"}, status=400)
        try:
            permit = PermitType.objects.get(id=id)
            data = json.loads(request.body)
            for field, value in data.items():
                setattr(permit, field, value)
            permit.save()
            return JsonResponse(model_to_dict(permit), status=200)
        except PermitType.DoesNotExist:
            return JsonResponse({"error": "Permit type not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class StandardLabelsView(ApiTokenValidityCheckMixin, View):
    def get(self, request, id=None):
        if id:
            try:
                label = StandardLabels.objects.get(id=id)
                return JsonResponse(model_to_dict(label), status=200)
            except StandardLabels.DoesNotExist:
                return JsonResponse({"error": "Standard label not found"}, status=404)

        labels = list(StandardLabels.objects.values())
        return JsonResponse(labels, safe=False, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            label = StandardLabels.objects.create(
                name=data.get("name"),
                always_required=data.get("always_required", False)
            )
            return JsonResponse(model_to_dict(label), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def patch(self, request, id=None):
        if not id:
            return JsonResponse({"error": "ID is required for update"}, status=400)
        try:
            label = StandardLabels.objects.get(id=id)
            data = json.loads(request.body)
            for field, value in data.items():
                setattr(label, field, value)
            label.save()
            return JsonResponse(model_to_dict(label), status=200)
        except StandardLabels.DoesNotExist:
            return JsonResponse({"error": "Standard label not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
