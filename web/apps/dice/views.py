from apps.api.lib import dice
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .form import DiceForm


# Create your views here.
class Index(TemplateView):
    template_name = "dice/index.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, self.template_name, {"form": DiceForm()})


class RollDiceView(TemplateView):
    template_name = "dice/index.html"

    def post(self, request: WSGIRequest) -> HttpResponse:
        form = DiceForm(request.POST)
        if form.is_valid():
            dies = form.cleaned_data["dies"]
            sides = form.cleaned_data["sides"]
            result = dice.roll_shuffle(dies, sides)
            context = {
                "form": form,
                "dies": dies,
                "sides": sides,
                "result": [f"{i:02d}" for i in result],
            }
            return render(request, self.template_name, context)
        return render(request, self.template_name, {"form": DiceForm()})

    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, self.template_name)


"""
# -------------------------- Second Draft View -------------------------- #
class RollDiceView(TemplateView):
    def post(self, request: WSGIRequest) -> HttpResponse:
        dies = int(request.POST.get("dies", DEFAULT_DIES))
        sides = int(request.POST.get("sides", DEFAULT_SIDES))
        result = self.roll_dice(abs(dies), abs(sides))
        context = {"result": result, "dies": dies, "sides": sides}
        return render(request, self.template_name, context)

"""

"""
# -------------------------- First Draft View -------------------------- #

def roll_dice(dies: int, sides: int) -> List[int]:
    nums = [i + 1 for i in range(sides)]
    random.shuffle(nums)

    return sorted(nums[:dies])


def get_result(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        dies = int(request.POST.get("dies", DEFAULT_DIES))
        sides = int(request.POST.get("sides", DEFAULT_SIDES))
        result = roll_dice(abs(dies), abs(sides))

        context = {"result": result, "dies": dies, "sides": sides}
        return render(request, "dice/index.html", context)

    return render(request, "dice/index.html")

# -------------------------- First Draft URL -------------------------- #
    path("roll", views.get_result, name="roll"),

"""
