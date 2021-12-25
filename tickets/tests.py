from django.test import TestCase, Client
from django.urls import reverse

from tickets.models import Section, Row, Customer, Seat


class TestTicketViews(TestCase):
    """
    Client tests of ticket views
    """
    def setUp(self) -> None:
        super(TestTicketViews, self).setUp()
        self.section_create_url = reverse('tickets:portal_section_create')
        self.test_section = Section.objects.create(name='Test')
        self.client = Client()

    def test_section_create(self):
        """
        Test of section creation
        """
        response = self.client.post(self.section_create_url, {
            'name': 'test section',
            'is_curved': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Section.objects.filter(name='test section').exists())

    def test_section_update(self):
        """
        Test of section update
        """
        section = Section.objects.create(name='test section')
        section_update_url = reverse('tickets:portal_section_update',
                                     kwargs={'section_id': section.id})

        response = self.client.post(section_update_url, {
            'name': 'new test section',
            'is_curved': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Section.objects.filter(name='new test section').exists())
        self.assertFalse(Section.objects.filter(is_curved=True).exists())

    def test_create_seats(self):
        """
        Test of seat creation
        """
        create_seats_url = reverse('tickets:portal_section_equal_seats_create')
        response = self.client.post(create_seats_url, {
            'section': self.test_section.id,
            'rows': 10,
            'seats_in_rows': 5
        })

        rows = Row.objects.filter(section=self.test_section)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(rows.count(), 10)
        self.assertEqual(rows[0].number_of_seats, 5)

    def test_create_seats_by_row(self):
        """
        Test of seat creation based on rows
        """
        create_seats_by_row_url = reverse('tickets:portal_section_seats_by_row')
        response = self.client.post(create_seats_by_row_url, {
            'section': self.test_section.id,
            'seats_in_row': 10
        })

        rows = Row.objects.filter(section=self.test_section)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(rows.count(), 1)
        self.assertEqual(rows[0].number_of_seats, 10)

    def test_customer_create(self):
        """
        Test of customer creation
        """
        customer_create_url = reverse('tickets:portal_customer_create')
        Row.objects.create(name='A',
                           section_id=self.test_section.id,
                           number_of_seats=10)

        response = self.client.post(customer_create_url, {
            'section': self.test_section.id,
            'reserve_name': 'test customer',
            'size_of_group': 3,
        })

        customers = Customer.objects.filter(section_id=self.test_section.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(customers.count(), 1)
        self.assertEqual(customers[0].size_of_group, 3)
        self.assertEqual(customers[0].reserve_name, 'test customer')

    def test_section_delete(self):
        """
        Test of section delete
        """
        section_delete_url = reverse('tickets:portal_section_delete',
                                     kwargs={'section_id': self.test_section.id})
        response = self.client.post(section_delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Section.objects.filter(id=self.test_section.id))

    def test_seating(self):
        """
        Test Seating process
        """
        number_of_test_rows = 3
        number_of_seats = 8
        row_letters = ['A', 'B', 'C']
        for i in range(number_of_test_rows):
            Row.objects.create(
                name=row_letters[i],
                section=self.test_section,
                number_of_seats=number_of_seats,
                order=i + 1
            )

        rows = Row.objects.filter(section_id=self.test_section.id)
        for row in rows:
            for i in range(row.number_of_seats):
                Seat.objects.create(
                    row=row,
                    seat_number=i,
                )

        test_customer_list = [1, 3, 4, 4, 5, 1, 2, 4]
        for i in range(len(test_customer_list)):
            Customer.objects.create(
                section=self.test_section,
                reserve_name='C{}'.format(i + 1),
                size_of_group=test_customer_list[i],
            )

        seating_url = reverse('tickets:portal_customer_bulk_seating')
        response = self.client.post(seating_url, {
            'section': self.test_section.id
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Seat.objects.get(row__order=2, seat_number=5).customer.reserve_name, 'C8')
        self.assertEqual(Seat.objects.get(row__order=3, seat_number=5).customer.reserve_name, 'C6')
