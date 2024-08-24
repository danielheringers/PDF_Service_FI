from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import black
from reportlab.platypus import SimpleDocTemplate
from io import BytesIO
from app.services.boletosV2.boleto_service import CustomTable

def create_pdf_teste():
    data = [
        [
            {'title': 'Banco Itaú S.A', 'title_font': 'Helvetica-Bold', 'title_size': 12,},
            {'title': 'Header 2', 'text': 'Subtext 2', 'title_font': 'Helvetica-Bold', 'title_size': 12, 'text_align': 'center', 'text_font': 'Helvetica', 'text_size': 10},
            {'title': 'Header 3', 'text': 'Subtext 3', 'title_font': 'Helvetica-Bold', 'title_size': 12, 'text_align': 'right', 'text_font': 'Helvetica', 'text_size': 10}
        ],
        [
            {'title': 'Row 2, Col 1', 'text': 'Description 1', 'title_font': 'Helvetica-Bold', 'title_size': 10, 'text_align': 'left', 'text_font': 'Helvetica', 'text_size': 9},
            {'title': 'Row 2, Col 2', 'text': 'Description 2', 'title_font': 'Helvetica-Bold', 'title_size': 10, 'text_align': 'center', 'text_font': 'Helvetica', 'text_size': 9}
        ],
        [
            {'title': 'Row 3, Col 1', 'text': 'Description 3', 'title_font': 'Helvetica-Bold', 'title_size': 8, 'text_align': 'left', 'text_font': 'Helvetica', 'text_size': 8},
            {'title': 'Row 3, Col 3', 'text': 'Description 5', 'title_font': 'Helvetica-Bold', 'title_size': 8, 'text_align': 'right', 'text_font': 'Helvetica', 'text_size': 8}
        ]
    ]

    col_widths = [
        [50 * mm, 30 * mm, 115 * mm],
        [150 * mm, 45 * mm],
        [150 * mm, 45 * mm],
    ]

    row_heights = [10 * mm, 10 * mm, 10 * mm]

    table = CustomTable(data, col_widths, row_heights, fillcolor=None, strokecolor=black)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=5*mm, rightMargin=5*mm,
                            topMargin=5*mm, bottomMargin=5*mm)
    elements = [table]
    doc.build(elements)

    buffer.seek(0)
    return buffer
