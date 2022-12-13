from django.db.models import QuerySet
from typing import List


def unpack_values(queryset: QuerySet, headers: List[str]) -> List[List]:
    """Unpacks a queryset into a 2D array

    :param queryset: The queryset that will be unpacked
    :param headers: A list of the desired headers of the queryset
    :returns A 2D array of headers, then rows
    """

    data = []
    data.append(headers)
    for row in queryset:
        values = []
        for field in headers:
            value = getattr(row, field)
            if value is None:
                value = ''
            values.append(value)
        data.append(values)

    return data
