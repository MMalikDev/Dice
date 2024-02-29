from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("roll", views.RollDice.as_view(), name="roll"),
]
