from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tickets.models import Customer, Seat, Section
from tickets.functions import bulk_seating
from .serializers import (SeatingSerializer, SeatsRetrieveSerializer,
                          SingleCustomerRetrieveSerializer)


class BulkSeatingApiView(APIView):
    def post(self, request):
        serializer = SeatingSerializer(data=request.data)

        if serializer.is_valid():
            section_id = serializer.validated_data.get('section_id')
            customers = serializer.validated_data.get('customer_list')

            customer_objects_list = []
            for customer_list in customers:
                aisle = 'aisle' == customer_list[1]
                customer = Customer.objects.create(
                    reserve_name=customer_list[0],
                    section_id=section_id,
                    aisle_required=aisle,
                    size_of_group=int(customer_list[2])
                )
                customer_objects_list.append(customer)

            if customer_objects_list:
                bulk_seating(section_id, customer_objects_list)

            seats_dict = {}
            seats = Seat.objects.filter(row__section_id=section_id)

            for seat in seats:
                seats_dict[seat.__str__()] = {}
                seats_dict[seat.__str__()]['is_allocated'] = seat.is_allocated
                seats_dict[seat.__str__()]['row'] = seat.row.order

                if seat.customer:
                    seats_dict[seat.__str__()]['customer'] = seat.customer.reserve_name

                seats_dict[seat.__str__()]['is_aisle'] = seat.is_aisle_seat

                if seat.is_blocked:
                    seats_dict[seat.__str__()]['is_blocked'] = seat.is_blocked

            return Response(seats_dict, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeatsRetrieveApi(APIView):
    def post(self, request):
        serializer = SeatsRetrieveSerializer(data=request.data)

        if serializer.is_valid():
            section_id = serializer.validated_data.get('section_id')
            seats_dict = {}
            seats = Seat.objects.filter(row__section_id=section_id)

            for seat in seats:
                seats_dict[seat.__str__()] = {}
                seats_dict[seat.__str__()]['is_allocated'] = seat.is_allocated
                seats_dict[seat.__str__()]['row'] = seat.row.order

                if seat.customer:
                    seats_dict[seat.__str__()]['customer'] = seat.customer.reserve_name

                seats_dict[seat.__str__()]['is_aisle'] = seat.is_aisle_seat

                if seat.is_blocked:
                    seats_dict[seat.__str__()]['is_blocked'] = seat.is_blocked

            return Response(seats_dict, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleSeatRetrieveApi(APIView):
    def post(self, request):
        serializer = SingleCustomerRetrieveSerializer(data=request.data)

        if serializer.is_valid():
            customer_name = serializer.validated_data.get('customer_name')
            seats_dict = {}
            seats = Seat.objects.filter(customer__reserve_name=customer_name)

            for seat in seats:
                seats_dict[seat.__str__()] = {}
                seats_dict[seat.__str__()]['is_allocated'] = seat.is_allocated
                seats_dict[seat.__str__()]['row'] = seat.row.order
                seats_dict[seat.__str__()]['customer'] = seat.customer.reserve_name
                seats_dict[seat.__str__()]['is_aisle'] = seat.is_aisle_seat

            return Response(seats_dict, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionsRetrieveApi(APIView):
    def get(self, request):
        sections = Section.objects.all().order_by('id')

        sections_dict = {}
        for section in sections:
            sections_dict[section.name] = {}
            sections_dict[section.name]['id'] = section.id
            sections_dict[section.name]['number_of_rows'] = section.rows.count()
            sections_dict[section.name]['is_curved'] = section.is_curved

        return Response(sections_dict, status=status.HTTP_200_OK)
