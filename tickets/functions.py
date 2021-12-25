from .models import Seat, Row


def allocate_seats(seats, customer):
    """
    allocate target seats for target customer
    :param seats: list of target seats
    :param customer: customer object from Customer model
    """
    if seats:
        for seat in seats:
            seat.customer = customer
            seat.save()

        return True

    else:
        return None


def create_available_blocks(section_id, target_row):
    """
    create available seats blocks
    :param section_id:
    :param target_row: the row_order of first available seat
    :return: a dictionary containing row and available seats blocks
    """
    seats_group_dict = {}
    for row in Row.objects.filter(order__gte=target_row, section_id=section_id):

        sub_group = []
        for seat in row.seats.all():
            if seat.is_available:
                sub_group.append(seat)

                if seat.id == row.seats.all().last().id:
                    if sub_group:
                        try:
                            seats_group_dict[row.order].append(sub_group)

                        except KeyError:
                            seats_group_dict[row.order] = [sub_group]

                    sub_group = []

            else:
                if sub_group:
                    try:
                        seats_group_dict[row.order].append(sub_group)

                    except KeyError:
                        seats_group_dict[row.order] = [sub_group]

                sub_group = []

    return seats_group_dict


def seating(section_id, customer):
    """
    seating process for target customer
    :param section_id: the id of target section
    :param customer: the customer object of Customer model
    :return: allocates seats
    """
    # get group size of customer
    group_size = customer.size_of_group
    aisle = customer.aisle_required

    # get seats of target section
    seats = Seat.objects.not_allocated_seats().filter(row__section_id=section_id)

    # get row of first available seat
    if not seats.first():
        return True

    # the row that we use for iteration
    target_row = 1

    # create available seats blocks
    seats_group_dict = create_available_blocks(section_id, target_row)

    # result list containing target seats for customer
    result = []
    for row, blocks in seats_group_dict.items():

        for block in blocks:

            # check there are sufficient available seats in block
            if len(block) >= group_size:

                # handle aisle seats if user has requested
                if aisle:
                    block_has_aisle = [seat for seat in block if seat.is_aisle_seat]

                    if not block_has_aisle:
                        continue

                if aisle:
                    if not block[0].is_aisle_seat:
                        block.reverse()

                # get target seats
                for seat in block:
                    if len(result) != group_size:
                        result.append(seat)

    if result:
        return allocate_seats(result, customer)


def bulk_seating(section_id, customers, loop=0):
    """
    Recursive function for optimize seating of multiple customers
    :param section_id: id of target section
    :param customers: list of customers objects
    :param loop: indicator of number of retries
    """
    for customer in customers:
        s = seating(section_id, customer)

        if s is None:
            the_loop = loop + 1
            Seat.objects.filter(row__section_id=section_id).update(customer=None)
            customers.insert(-loop, customers.pop(-loop))
            bulk_seating(section_id, customers, the_loop)


def row_name_generator(row_index):
    """
    Generate name of rows based on alphabets
    :param row_index: index of the target row in all rows
    :return: string name of the row
    """
    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z']

    if row_index <= len(alphabets):
        return alphabets[row_index]

    else:
        row_name = []
        number_of_iterations = row_index // len(alphabets)
        for _ in range(number_of_iterations):
            row_name.append(alphabets[-1])

        row_name.append(alphabets[row_index % len(alphabets)])

        return ''.join(row_name)
