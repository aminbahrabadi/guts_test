from django.urls import reverse

from rest_framework.test import APITestCase

from tickets.models import Section, Row, Seat, Customer


class TestApi(APITestCase):
    def setUp(self) -> None:
        super(TestApi, self).setUp()
        self.test_section = Section.objects.create(name='Test')

        row_names = ['A', 'B', 'C']
        for i in range(3):
            Row.objects.create(
                section_id=self.test_section.id,
                name=row_names[i],
                number_of_seats=8,
                order=i + 1
            )

        rows = Row.objects.filter(section_id=self.test_section.id)
        for row in rows:
            for i in range(row.number_of_seats):
                Seat.objects.create(
                   row=row,
                   seat_number=i + 1
                )

        self.seats = Seat.objects.all()

    def test_sections_retrieve_api(self):
        sections_retrieve_url = reverse('api:api_retrieve_sections')
        response = self.client.get(sections_retrieve_url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Section.objects.get(name='Test').id, response.data.get('Test').get('id'))

    def test_seats_retrieve_api(self):
        seats_retrieve_url = reverse('api:api_retrieve_seats')
        response = self.client.post(seats_retrieve_url, {
            'section_id': self.test_section.id
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Seat.objects.first().row.order, response.data.get('A1').get('row'))

    def test_seating_api(self):
        seating_url = reverse('api:api_bulk_seating')
        data = {
            'section_id': self.test_section.id,
            'customer_list': [
                ['A', '', 1],
                ['B', '', 3],
                ['C', '', 4],
                ['D', '', 4],
                ['E', '', 5],
                ['F', '', 1],
                ['G', '', 2],
                ['H', '', 4]
            ]
        }

        response = self.client.post(seating_url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Seat.objects.get(row__order=2, seat_number=5).customer.reserve_name, 'H')
        self.assertEqual(Seat.objects.get(row__order=3, seat_number=6).customer.reserve_name, 'F')
