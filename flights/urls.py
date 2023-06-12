from django.urls import path
from .views import FlightListAPIView, FlightDetailAPIView, FlightSearchAPIView

urlpatterns = [
    path("", FlightListAPIView.as_view(), name="flight_list"),
    path("<int:flight_id>", FlightDetailAPIView.as_view(), name="flight_detail"),
    path("search/", FlightSearchAPIView.as_view(), name="flight_search"),
]
