from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Flight, Booking
from .serializers import BookingSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated


class BookFlightAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        flight_id = request.data.get("flight")
        ticket_class = request.data.get("ticket_class")

        if ticket_class not in [choice[0] for choice in Booking.TICKET_CLASS_CHOICES]:
            return Response(
                {"error": "Invalid ticket class."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            f = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            return Response(
                {"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpgradeBookingAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, booking_id):
        ticket_class = request.data.get("ticket_class")
        price = request.data.get("price")

        if not ticket_class or not price:
            return Response(
                {"error": "Ticket class and price are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if ticket_class not in [choice[0] for choice in Booking.TICKET_CLASS_CHOICES]:
            return Response(
                {"error": "Invalid ticket class."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
            )
        valid_fields = [
            "ticket_class",
            "price",
        ]
        invalid_fields = set(request.data.keys()) - set(valid_fields)
        if invalid_fields:
            return Response(
                {"error": f"Invalid parameter name(s): {', '.join(invalid_fields)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelBookingAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
            )

        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
