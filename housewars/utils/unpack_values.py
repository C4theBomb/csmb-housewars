def unpack_values(queryset):
    """Unpacks a queryset into a 2D array

    Parameters
    ----------
    queryset : int
        The queryset that will be unpacked

    Returns
    -------
    data : [list]
        A random string of length n
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
