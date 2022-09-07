import string
from django.db.models import QuerySet
from typing import List


def unpack_values(queryset: QuerySet, headers: List[str]) -> List[List]:
    """Unpacks a queryset into a 2D array

    :param queryset: The queryset that will be unpacked
    :param headers: The headers of the 
    :returns A table headers, then rows
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
