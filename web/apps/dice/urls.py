from django.urls import path

from . import views

app_name = "dice"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("roll", views.RollDiceView.as_view(), name="roll"),
]
