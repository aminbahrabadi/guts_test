from rest_framework import serializers


class SeatingSerializer(serializers.Serializer):
    """
    Serializer for seating Api.
    """
    section_id = serializers.IntegerField()
    customer_list = serializers.ListField()

    def validate(self, attrs):
        customer_list = attrs.get('customer_list')
        for customer in customer_list:
            try:
                reserve_name, properties, size_of_group = customer
                int(size_of_group)

            except ValueError:
                raise serializers.ValidationError(
                    {'customers': 'every customer should have a name, properties and size of group'})

        return super(SeatingSerializer, self).validate(attrs)


class SeatsRetrieveSerializer(serializers.Serializer):
    """
    Serializer for retrieving all seats statuses and information in a section
    """
    section_id = serializers.IntegerField()

    def validate(self, attrs):
        try:
            int(attrs.get('section_id'))

        except ValueError:
            raise serializers.ValidationError(
                {'section_id': 'section id must be integer'})

        return super(SeatsRetrieveSerializer, self).validate(attrs)


class SingleCustomerRetrieveSerializer(serializers.Serializer):
    """
    Serializer for retrieving seats that a customer's reserved
    """
    customer_name = serializers.CharField(max_length=255)
