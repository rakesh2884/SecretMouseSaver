from rest_framework.views import APIView
from rest_framework import status
from events.models import Event, formdata
from rest_framework.response import Response
from events.serializers import FormSerializer


def is_date_in_range(date, start_date, end_date):
    return start_date <= date <= end_date


class userForm(APIView):
    serializer_class = FormSerializer

    def post(self, request):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.data['email']
            floridaResident = serializer.data['floridaResident']
            if floridaResident == "Yes":
                serializer.data['floridaResident'] = True
            else:
                serializer.data['floridaResident'] = False
            customer = formdata.objects.get(email=email)
            totalGuests = (
                customer.noOfGuestAges_10plus+customer.noOfGuestAges_3to9
            )
            events = Event.objects.all()
            for event in events:
                if is_date_in_range(
                    customer.visitStartDate,
                    event.validStartDate,
                    event.validEndDate
                ) and is_date_in_range(
                    customer.visitEndDate,
                    event.validStartDate,
                    event.validEndDate
                ):
                    if customer.noOfThemeParkDays >= 3 and totalGuests >= 2:
                        if customer.floridaResident is False:
                            return Response({
                                "message": "Congrats! You will get a discount coupon",
                                "code": 1,
                                "event_url": event.eventPageURL
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                "message": "Sorry, we couldn’t find any savings for your visit",
                                "code": 0
                            }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            "message": "Sorry, we couldn’t find any savings for your visit",
                            "code": 0}, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "Sorry, we couldn’t find any savings for your visit",
                        "code": 0}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)
