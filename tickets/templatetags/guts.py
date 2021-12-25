from django import template


register = template.Library()


@register.filter()
def get_seats_list(seats):
    """
    Convert seats queryset to string of seats list
    :param seats: queryset of seats
    :return: comma separated sting of seat names
    """
    seats_list = ['{}{}'.format(seat.row.name, seat.seat_number) for seat in seats]
    return ', '.join(seats_list)
