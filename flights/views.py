from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Flight
from .serializers import FlightSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class FlightListAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, _):
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlightDetailAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, flight_id):
        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            return Response(
                {"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = FlightSerializer(flight)
        return Response(serializer.data)

    def put(self, request, flight_id):
        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            return Response(
                {"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND
            )
        valid_fields = [
            "departure_location",
            "arrival_location",
            "fare",
            "departure_time",
            "arrival_time",
        ]
        invalid_fields = set(request.data.keys()) - set(valid_fields)
        if invalid_fields:
            return Response(
                {"error": f"Invalid parameter name(s): {', '.join(invalid_fields)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = FlightSerializer(flight, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, _, flight_id):
        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            return Response(
                {"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND
            )
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FlightSearchAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        fare_min = request.query_params.get("fare_min")
        fare_max = request.query_params.get("fare_max")
        departure_location = request.query_params.get("from")
        arrival_location = request.query_params.get("to")
        if not departure_location or not arrival_location:
            return Response(
                {"error": "Please provide both departure and arrival locations."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        flights = Flight.objects.filter(
            departure_location=departure_location, arrival_location=arrival_location
        )

        if fare_min and fare_max:
            flights = flights.filter(fare__range=(fare_min, fare_max))
        elif fare_min:
            flights = flights.filter(fare__gte=fare_min)
        elif fare_max:
            flights = flights.filter(fare__lte=fare_max)
        flights = flights.order_by("fare")

        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)
