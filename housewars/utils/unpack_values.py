from django.db.models import QuerySet
from typing import List


def unpack_values(queryset: QuerySet) -> List[List]:
    """Unpacks a queryset into a 2D array

    :param queryset: The queryset that will be unpacked
    :returns A table headers, then rows
    """

    field_names = [field.name for field in queryset.model._meta.fields]
    data = []
    data.append(field_names)
    for row in queryset:
        values = []
        for field in field_names:
            value = getattr(row, field)
            if value is None:
                value = ''
            values.append(value)
        data.append(values)

    return data
