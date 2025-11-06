from django.urls import path
from .views import region_page, subregion_page

urlpatterns = [
    path("<str:region_name>/", region_page, name="region_page"),
    path("<str:region_name>/<str:sub_name>/", subregion_page, name="subregion_page"),
]
