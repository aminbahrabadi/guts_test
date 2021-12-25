from django.db import models
from django.core.exceptions import ValidationError


class Section (models.Model):
    """
    Properties of a section is defined in Section model
    """
    created_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, null=True, blank=False,
                            verbose_name='Name')

    is_curved = models.BooleanField(default=False, verbose_name='Section is Curved')

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    User groups who reserve seats
    """
    reserve_name = models.CharField(max_length=255, null=True, blank=False,
                                    verbose_name='Reserve Name')
    section = models.ForeignKey(Section, null=True, blank=False, verbose_name='Section',
                                on_delete=models.CASCADE)
    size_of_group = models.IntegerField(default=1, verbose_name='Size of Group')

    aisle_required = models.BooleanField(default=False, verbose_name='Need Aisle seat')

    def __str__(self):
        return self.reserve_name


class Row(models.Model):
    """
    Properties of a row is defined in Row model
    """
    name = models.CharField(max_length=255, null=True, blank=False, verbose_name='Row Name')
    section = models.ForeignKey(Section, null=True, blank=False, verbose_name='Section',
                                on_delete=models.CASCADE, related_name='rows')
    order = models.PositiveIntegerField(default=1, verbose_name='Row Order')
    number_of_seats = models.IntegerField(default=1, verbose_name='Number of Seats')

    def __str__(self):
        return self.name


class SeatManager(models.Manager):
    """
    create custom manager to manage custom queries
    """
    def get_queryset(self):
        return super().get_queryset().all()

    def not_allocated_seats(self):
        return self.get_queryset().filter(customer__isnull=True)

    def allocated_seats(self):
        return self.get_queryset().filter(customer__isnull=False)

    def available_seats(self):
        return self.get_queryset().filter(customer__isnull=True, is_blocked=False)


class Seat(models.Model):
    """
    Properties of a seat is defined in Seat model
    """
    row = models.ForeignKey(Row, null=True, blank=False, verbose_name='Seat Row',
                            on_delete=models.CASCADE, related_name='seats')
    seat_number = models.IntegerField(null=True, blank=False, verbose_name='Seat Number')

    rank_choices = ((1, '1st rank'), (2, '2nd rank'), (3, '3rd rank'))
    rank = models.PositiveSmallIntegerField(choices=rank_choices, default=1,
                                            verbose_name='Rank')

    is_high_seat = models.BooleanField(default=False, verbose_name='Seat is a High Seat')
    is_blocked = models.BooleanField(default=False, verbose_name='Seat is Blocked')

    customer = models.ForeignKey(Customer, null=True, blank=True,
                                 verbose_name='Customer Reserved', on_delete=models.SET_NULL)

    objects = SeatManager()

    def __str__(self):
        return '{}{}'.format(self.row.name, self.seat_number)

    def clean(self):
        # handle row seats, avoid creating seats more than row capacity
        number_of_row_seats = self.row.number_of_seats
        number_of_current_seats = Seat.objects.filter(
            row_id=self.row.id).exclude(id=self.id).count()
        if number_of_current_seats == number_of_row_seats:
            raise ValidationError('This row has {} seats.'.format(self.row.number_of_seats))

        return super(Seat, self).clean()

    @ property
    def is_available(self):
        if not any([self.customer, self.is_blocked]):
            return True
        return False

    @property
    def is_allocated(self):
        if self.customer:
            return True
        return False

    @property
    def is_front_seat(self):
        if self.row.order == 1:
            return True
        return False

    @property
    def is_aisle_seat(self):
        seat_rows = list(self.row.seats.order_by('id').values_list('id', flat=True))
        if seat_rows:
            if self.id in [seat_rows[0], seat_rows[-1]]:
                return True

        return False

    class Meta:
        unique_together = ('row', 'seat_number')
