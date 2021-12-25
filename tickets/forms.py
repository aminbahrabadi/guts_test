from django import forms
from .models import Section, Row, Customer, Seat


class SectionCreateUpdateForm(forms.ModelForm):
    """
    Section Create or Update form
    """
    class Meta:
        model = Section
        fields = ['name', 'is_curved']


class SectionEqualSeatsCreateForm(forms.Form):
    """
    Section Create form when every rows have equal number of seats
    """
    section = forms.ModelChoiceField(queryset=Section.objects.filter(rows__seats__isnull=True))
    rows = forms.IntegerField(label='Number of rows', required=True)
    seats_in_rows = forms.IntegerField(label='Number of seats in a row', required=True)

    def clean(self):
        # clean section
        section = self.cleaned_data.get('section')
        if section:
            if Row.objects.filter(section=section).exists():
                raise forms.ValidationError('The section already has seats')

        return super(SectionEqualSeatsCreateForm, self).clean()


class CustomerForm(forms.ModelForm):
    """
    Form for creating customers
    """
    section = forms.ModelChoiceField(queryset=Section.objects.exclude(rows__isnull=True))
    allocate_customers = forms.BooleanField(label='Allocate customers', required=False)

    class Meta:
        model = Customer
        fields = ['section', 'reserve_name', 'size_of_group', 'aisle_required']


class BulkSeatingForm(forms.Form):
    """
    Form for seating all customers in a section
    """
    section = forms.ModelChoiceField(queryset=Section.objects.exclude(rows__isnull=True))


class SeatUpdateForm(forms.ModelForm):
    """
    Form for updating a seat properties
    """
    class Meta:
        model = Seat
        fields = ['seat_number', 'rank', 'is_high_seat', 'is_blocked']


class SectionSeatsByRowsForm(forms.Form):
    """
    Form for creating seats in a section that rows doesn't have equal seats
    """
    section = forms.ModelChoiceField(queryset=Section.objects.all())
    seats_in_row = forms.IntegerField(label='Number of seats in row', required=True)
