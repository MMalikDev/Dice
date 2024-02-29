from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.generic import TemplateView

from .lib import dice


# Create your views here.
class Index(TemplateView):
    template_name = "common/index.html"


class RollDice(TemplateView):
    DEFAULT_DIES, DEFAULT_SIDES = 7, 50

    def get(self, request: WSGIRequest) -> JsonResponse:
        try:
            dies = request.GET.get("dies", self.DEFAULT_DIES)
            sides = request.GET.get("sides", self.DEFAULT_SIDES)
            response = dice.roll_shuffle(abs(int(dies)), abs(int(sides)))
        except ValueError:
            msg = "Invalid input type. Please provide number as parameters"
            return JsonResponse({"ERROR": msg}, status=400)
        return JsonResponse(response, safe=False)


"""
# -------------------------- First Draft View -------------------------- #

@csrf_exempt
def roll_dice(request: WSGIRequest) -> HttpResponse:
    if request.method != "GET":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    try:
        dies = int(request.GET.get("dies", 7))
        sides = int(request.GET.get("sides", 50))
        response = dice.roll_shuffle(abs(dies), abs(sides))
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse(response, safe=False)

# -------------------------- First Draft URL -------------------------- #
    path("roll", views.roll_dice, name="roll"),

"""
