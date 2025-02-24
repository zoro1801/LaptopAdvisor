from django.urls import path
from .views import select_model,predict,home

urlpatterns = [
    path("", home, name="home"),
    path("select_model/<str:model_name>/", select_model, name="select_model"),
    path("predict/", predict, name="predict"),
]