from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Row, Section, Seat, Customer
from .forms import (SectionCreateUpdateForm, SectionEqualSeatsCreateForm,
                    CustomerForm, BulkSeatingForm, SeatUpdateForm, SectionSeatsByRowsForm)
from .functions import row_name_generator, seating, bulk_seating


class PortalIndexTemplateView(generic.TemplateView):
    template_name = 'tickets/portal_index.html'

    def get_context_data(self, **kwargs):
        context = super(PortalIndexTemplateView, self).get_context_data(**kwargs)

        context['sections'] = Section.objects.exclude(rows__seats__isnull=True)

        return context


class PortalSectionCreateView(generic.CreateView):
    template_name = 'tickets/portal_section_create_update.html'
    form_class = SectionCreateUpdateForm
    context_object_name = 'section'

    def get_success_url(self):
        messages.success(self.request, 'Section is successfully created')
        return reverse_lazy('tickets:portal_sections_manage')


class PortalSectionUpdateView(generic.UpdateView):
    template_name = 'tickets/portal_section_create_update.html'
    form_class = SectionCreateUpdateForm
    context_object_name = 'section'

    def get_object(self, queryset=None):
        section_id = self.kwargs.get('section_id')
        obj = get_object_or_404(Section, id=section_id)
        return obj

    def get_success_url(self):
        messages.success(self.request,
                         '{} section is successfully updated'.format(self.object.name))
        return reverse_lazy('tickets:portal_sections_manage')


class PortalSectionSeatsFormView(generic.FormView):
    template_name = 'tickets/portal_section_equal_seats_create.html'
    form_class = SectionEqualSeatsCreateForm

    def form_valid(self, form):
        section = form.cleaned_data.get('section')
        rows = form.cleaned_data.get('rows')
        seats = form.cleaned_data.get('seats_in_rows')

        for row_index in range(rows):
            row = Row.objects.create(
                name=row_name_generator(row_index),
                section=section,
                order=row_index + 1,
                number_of_seats=seats
            )

            for seat_index in range(seats):
                Seat.objects.create(
                    row=row,
                    seat_number=seat_index + 1,
                )

        return super(PortalSectionSeatsFormView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Seats are successfully created')
        return reverse_lazy('tickets:portal_sections_manage')


class PortalCustomerCreateView(generic.CreateView):
    template_name = 'tickets/portal_customer_create.html'
    form_class = CustomerForm
    context_object_name = 'customer'

    def form_valid(self, form):
        customer = form.save()

        if form.cleaned_data.get('allocate_customers'):
            seating_process = seating(section_id=customer.section.id,
                                      customer=customer)

            if seating_process is None:
                messages.error(
                    self.request,
                    'No seats are available for '
                    'customer in {} section'.format(customer.section))
                customer.delete()
                return self.form_invalid(form)

        return super(PortalCustomerCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Seats successfully allocated')
        return reverse_lazy('tickets:portal_index')


class PortalCustomerBulkSeatingView(generic.FormView):
    template_name = 'tickets/portal_customer_bulk_seating.html'
    form_class = BulkSeatingForm

    def form_valid(self, form):
        section = form.cleaned_data.get('section')
        if section:
            customers = Customer.objects.filter(section_id=section.id)
            if customers.exists():
                bulk_seating(section_id=section.id, customers=list(customers))
                messages.success(self.request, 'Customers are successfully allocated')
            else:
                messages.error(self.request, 'There is no customer for this section')

        return super(PortalCustomerBulkSeatingView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tickets:portal_customer_bulk_seating')


class PortalSeatsManageListView(generic.ListView):
    template_name = 'tickets/portal_seats_manage_list.html'
    context_object_name = 'seats'

    def get_queryset(self):
        qs = Seat.objects.all().select_related('row__section').order_by('row__section', 'id')
        return qs


class PortalSeatUpdateView(generic.UpdateView):
    template_name = 'tickets/portal_seat_edit.html'
    context_object_name = 'seat'
    form_class = SeatUpdateForm

    def get_object(self, queryset=None):
        seat_id = self.kwargs.get('seat_id')
        seat = get_object_or_404(Seat, id=seat_id)
        return seat

    def get_success_url(self):
        messages.success(self.request, 'Seat is successfully edited')
        return reverse_lazy('tickets:portal_seats_manage')


class PortalSectionsManageListView(generic.ListView):
    template_name = 'tickets/portal_sections_manage_list.html'
    context_object_name = 'sections'

    def get_queryset(self):
        qs = Section.objects.all().order_by('-created_at')
        return qs


class PortalSectionDeleteView(generic.DeleteView):
    def get_object(self, queryset=None):
        section_id = self.kwargs.get('section_id')
        section = get_object_or_404(Section, id=section_id)
        return section

    def get_success_url(self):
        messages.success(self.request, 'Section is successfully deleted')
        return reverse_lazy('tickets:portal_sections_manage')


class PortalSectionSeatsByRowsFormView(generic.FormView):
    template_name = 'tickets/portal_section_seats_by_row.html'
    form_class = SectionSeatsByRowsForm

    def form_valid(self, form):
        section = form.cleaned_data.get('section')
        seats = form.cleaned_data.get('seats_in_row')

        if Row.objects.filter(section_id=section).exists():
            row_index = Row.objects.order_by('id').filter(section_id=section).last().order
        else:
            row_index = 0

        row = Row.objects.create(
            name=row_name_generator(row_index),
            section=section,
            order=row_index + 1,
            number_of_seats=seats
        )

        for seat_index in range(seats):
            Seat.objects.create(
                row=row,
                seat_number=seat_index + 1,
            )

        return super(PortalSectionSeatsByRowsFormView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Row is successfully created')
        return reverse_lazy('tickets:portal_section_seats_by_row')
