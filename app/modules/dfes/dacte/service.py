import gc
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

from app.modules.dfes.dacte.schemas import DactePayload
from app.modules.dfes.dacte.template.header import add_header
from app.modules.dfes.dacte.template.body import add_body
from app.modules.dfes.dacte.template.footer import add_footer
from app.modules.dfes.dacte.template.watermark import add_watermark

def draw_base_layout(canvas_obj, data: DactePayload):
    add_header(canvas_obj, data)
    add_footer(canvas_obj, data)
    add_body(canvas_obj, data)
    add_watermark(canvas_obj, data)

def generate_dacte_pdf_bytes(dacte: DactePayload) -> BytesIO:    
    # Obtenção do buffer
    buffer = BytesIO()
    canvas_draw = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    marginTOP = height - 15 * mm
    page_count = 1
    
    draw_base_layout(canvas_draw, dacte)
     # Próxima página (se necessário)
    canvas_draw.showPage()
    gc.collect()
    # Finaliza o PDF
    canvas_draw.save()
    buffer.seek(0)

    return buffer