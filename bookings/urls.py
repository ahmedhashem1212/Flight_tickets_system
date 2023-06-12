from django.urls import path
from .views import BookFlightAPIView, UpgradeBookingAPIView, CancelBookingAPIView

urlpatterns = [
    path("", BookFlightAPIView.as_view(), name="book-flight"),
    path(
        "upgrade/<int:booking_id>",
        UpgradeBookingAPIView.as_view(),
        name="upgrade-booking",
    ),
    path(
        "cancel/<int:booking_id>", CancelBookingAPIView.as_view(), name="cancel-booking"
    ),
]
