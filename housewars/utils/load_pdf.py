from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black

import io

from housewars.utils import unpack_values


def load_pdf(data, headers, title=""):
    """Loads data from queryset into a pdf file

    :param queryset: The queryset that will be unpacked
    :param headers: A list of the desired headers of the queryset
    :returns A bytestream of a pdf file
    """

    # Initialize pdf object
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Create the page title
    title = Paragraph(title)

    # Load title into PDF file
    elements.append(title)

    # Unpack queryset data
    data = unpack_values(data, headers)

    # Load data into table and set styles
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle(
        [('INNERGRID', (0, 0), (-1, -1), 0.25, black), ('BOX', (0, 0), (-1, -1), 0.25, black)]))

    # Load table into PDF file
    elements.append(table)

    # Build document
    doc.build(elements)
    buffer.seek(0)

    return buffer
