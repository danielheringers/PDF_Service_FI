from io import BytesIO
from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from app.utils.utils import (escrever_texto)

def adjust_font_size_for_text(canvas, text, max_width, font_name="Helvetica-Bold", initial_size=30, min_size=1):
    size = initial_size
    while size > min_size:
        canvas.setFont(font_name, size)
        text_width = canvas.stringWidth(text, font_name, size)
        if text_width <= max_width:
            return size
        size -= 0.5
    return min_size

def draw_table_lines(canvas, verticals, horizontals):
    for (x, y_start, y_end) in verticals:
        canvas.line(x * mm, y_start * mm, x * mm, y_end * mm)

    for (x_start, x_end, y) in horizontals:
        canvas.line(x_start * mm, y * mm, x_end * mm, y * mm)

def draw_bank_header(canvas, bank_name, bank_code, margin, width, top_y_mm=280):
    primeira_linha = margin
    segunda_linha = 70 * mm
    largura_total = (segunda_linha - primeira_linha) - 2 * mm

    tamanho_fonte = adjust_font_size_for_text(
        canvas, bank_name, largura_total,
        font_name="Helvetica-Bold", initial_size=30, min_size=1
    )

    texts_row_one = [
        (bank_code, 78, top_y_mm, 16, True, False),
        ("Recibo do Pagador", "right - 30", top_y_mm - 2, 9, True, False)
    ]
    escrever_texto(canvas, texts_row_one, margin, width)

    canvas.setFont("Helvetica-Bold", tamanho_fonte)
    canvas.drawCentredString((primeira_linha + segunda_linha) / 2, (top_y_mm - 0.5) * mm, bank_name)
    
    draw_table_lines(
        canvas,
        verticals=[
            ((margin / mm), 287, 277),
            (70, 287, 277),
            (100, 287, 277),
            ((width - margin) / mm, 287, 277),
        ],
        horizontals=[
            ((margin / mm), ((width - margin) / mm), 287),
            ((margin / mm), ((width - margin) / mm), 277)
        ]
    )


def template_boleto(canvas):
    width, height = A4
    margin = 15 * mm

    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 277, 267),
            (150, 277, 267),
            ((width - margin)/mm, 277, 267),
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 277), (margin/mm, (width - margin)/mm, 267)]
    )
    
    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 267, 257),
            (150, 267, 257),
            ((width - margin)/mm, 267, 257)
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 267), (margin/mm, (width - margin)/mm, 257)]
    )

    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 257, 247),
            (150, 257, 247),
            (125, 257, 247),
            (95, 257, 247),
            (75, 257, 247),
            (45, 257, 247),
            ((width - margin)/mm, 257, 247)
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 257), (margin/mm, (width - margin)/mm, 247)]
    )

    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 247, 237),
            (150, 247, 237),
            (125, 247, 237),
            (95, 247, 237),
            (75, 247, 237),
            (55, 247, 237),
            (40, 247, 237),
            ((width - margin)/mm, 247, 237),
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 247), (margin/mm, (width - margin)/mm, 237)]
    )

    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 237, 187),
            (150, 237, 187),
            ((width - margin)/mm, 237, 187),
        ],
        horizontals=[
            (margin/mm, (width - margin)/mm, 237),
            (margin/mm, (width - margin)/mm, 187)
        ]
    )
    
    draw_table_lines(
        canvas,
        verticals=[],
        horizontals=[
            ((165 * mm - margin) / mm, (width - margin)/mm, 227),
            ((165 * mm - margin) / mm, (width - margin)/mm, 217),
            ((165 * mm - margin) / mm, (width - margin)/mm, 207),
            ((165 * mm - margin) / mm, (width - margin)/mm, 197),
        ]
    )
    
    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 187, 167),
            ((width - margin)/mm, 187, 167),
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 187), (margin/mm, (width - margin)/mm, 167)]
    )
    
    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 157, 147),
            (70, 157, 147),
            (100, 157, 147),
            ((width - margin)/mm, 157, 147),
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 157), (margin/mm, (width - margin)/mm, 147)]
    )

    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 147, 137),
            (150, 147, 137),
            ((width - margin)/mm, 147, 137)
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 147), (margin/mm, (width - margin)/mm, 137)]
    )

    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 137, 127),
            (150, 137, 127),
            ((width - margin)/mm, 137, 127)
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 137), (margin/mm, (width - margin)/mm, 127)]
    )

    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 127, 117),
            (150, 127, 117),
            (125, 127, 117),
            (95, 127, 117),
            (75, 127, 117),
            (45, 127, 117),
            ((width - margin)/mm, 127, 117)
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 127), (margin/mm, (width - margin)/mm, 117)]
    )

    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 117, 107),
            (150, 117, 107),
            (125, 117, 107),
            (95, 117, 107),
            (75, 117, 107),
            (55, 117, 107),
            (40, 117, 107),
            ((width - margin)/mm, 117, 107),
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 117), (margin/mm, (width - margin)/mm, 107)]
    )

    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 117, 57),
            (150, 117, 57),
            ((width - margin)/mm, 117, 57)
        ],
        horizontals=[
            (margin/mm, (width - margin)/mm, 117),
            (margin/mm, (width - margin)/mm, 57)
        ]
    )
    draw_table_lines(
        canvas,
        verticals=[],
        horizontals=[
            ((165 * mm - margin)/mm, (width - margin)/mm, 97),
            ((165 * mm - margin)/mm, (width - margin)/mm, 87),
            ((165 * mm - margin)/mm, (width - margin)/mm, 77),
            ((165 * mm - margin)/mm, (width - margin)/mm, 67),
        ]
    )
    draw_table_lines(
        canvas,
        verticals=[
            (margin/mm, 57, 37),
            ((width - margin)/mm, 57, 37),
        ],
        horizontals=[(margin/mm, (width - margin)/mm, 57), (margin/mm, (width - margin)/mm, 37)]
    )
    # ========================= Textos =========================
    canvas.setFont("Helvetica-Bold", 6)
    canvas.drawString(margin + 2 * mm, 275 * mm, "Local de pagamento")
    canvas.drawString(152 * mm, 275 * mm, "Vencimento")
    canvas.drawString(margin + 2 * mm, 255 * mm, "Data do Doc.")
    canvas.drawString(47 * mm, 255 * mm, "Número Documento")
    canvas.drawString(77 * mm, 255 * mm, "Espécie Doc.")
    canvas.drawString(97 * mm, 255 * mm, "Aceite")
    canvas.drawString(127 * mm, 255 * mm, "Data Processamento")
    canvas.drawString(152 * mm, 255 * mm, "Nosso Número")
    canvas.drawString(margin + 2 * mm, 265 * mm, "Beneficiário")
    canvas.drawString(152 * mm, 265 * mm, "Agência / Código Beneficiário")
    canvas.drawString(margin + 2 * mm, 245 * mm, "Uso do Banco")
    canvas.drawString(41 * mm, 245 * mm, "CIP")
    canvas.drawString(56 * mm, 245 * mm, "Carteira")
    canvas.drawString(77 * mm, 245 * mm, "Esp. Moeda")
    canvas.drawString(97 * mm, 245 * mm, "Quantidade")
    canvas.drawString(127 * mm, 245 * mm, "Valor")
    canvas.drawString(152 * mm, 245 * mm, "(=) Valor do documento")
    canvas.drawString(152 * mm, 235 * mm, "(-) Desconto / Abatimento")
    canvas.drawString(152 * mm, 225 * mm, "(-) Outras Deduções")
    canvas.drawString(152 * mm, 215 * mm, "(+) Mora / Multa")
    canvas.drawString(152 * mm, 205 * mm, "(+) Outros Acréscimos")
    canvas.drawString(152 * mm, 195 * mm, "(=) Valor Cobrado")
    canvas.drawString(margin + 2 * mm, 184 * mm, "Pagador:")
    canvas.drawString(margin + 2 * mm, 168 * mm, "Sacador/Avalista")
    canvas.drawString(130 * mm, 165 * mm, "Autenticação Mecânica")
    instructionsText = ("Instruções (instruções de responsabilidade do beneficiário. Qualquer dúvida sobre este boleto, contate o beneficiário)")
    canvas.drawString(margin + 2 * mm, 237 * mm - 3 * mm, instructionsText)
    canvas.drawString(margin + 2 * mm, 145 * mm, "Local de pagamento")
    canvas.drawString(152 * mm, 145 * mm, "Vencimento")
    canvas.drawString(margin + 2 * mm, 135 * mm, "Beneficiário")
    canvas.drawString(152 * mm, 135 * mm, "Agência / Código Beneficiário")
    canvas.drawString(margin + 2 * mm, 125 * mm, "Data do Doc.")
    canvas.drawString(47 * mm, 125 * mm, "Número Documento")
    canvas.drawString(77 * mm, 125 * mm, "Espécie Doc.")
    canvas.drawString(97 * mm, 125 * mm, "Aceite")
    canvas.drawString(127 * mm, 125 * mm, "Data Processamento")
    canvas.drawString(152 * mm, 125 * mm, "Nosso Número")
    canvas.drawString(margin + 2 * mm, 115 * mm, "Uso do Banco")
    canvas.drawString(41 * mm, 115 * mm, "CIP")
    canvas.drawString(56 * mm, 115 * mm, "Carteira")
    canvas.drawString(77 * mm, 115 * mm, "Esp. Moeda")
    canvas.drawString(97 * mm, 115 * mm, "Quantidade")
    canvas.drawString(127 * mm, 115 * mm, "Valor")
    canvas.drawString(152 * mm, 115 * mm, "(=) Valor do documento")
    canvas.drawString(152 * mm, 105 * mm, "(-) Desconto / Abatimento")
    canvas.drawString(152 * mm, 95 * mm, "(-) Outras Deduções")
    canvas.drawString(152 * mm, 85 * mm, "(+) Mora / Multa")
    canvas.drawString(152 * mm, 75 * mm, "(+) Outros Acréscimos")
    canvas.drawString(152 * mm, 65 * mm, "(=) Valor Cobrado")
    canvas.drawString(margin + 2 * mm, 54 * mm, "Pagador:")
    canvas.drawString(margin + 2 * mm, 38 * mm, "Sacador/Avalista")
    canvas.drawString(130 * mm, 35 * mm, "Autenticação Mecânica")
    canvas.drawString(margin + 2 * mm, 107 * mm - 3 * mm, instructionsText)   
     
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(margin + 2 * mm, 269 * mm, "Pagável em qualquer banco")
    canvas.drawString(margin + 2 * mm, 240 * mm, "")
    canvas.drawString(41 * mm, 240 * mm, "")
    canvas.drawString(77 * mm, 240 * mm, "Real")
    canvas.drawString(97 * mm, 240 * mm, "")
    canvas.drawString(127 * mm, 240 * mm, "")
            
    canvas.drawString(margin + 2 * mm, 139 * mm, "Pagável em qualquer banco")
    canvas.drawString(margin + 2 * mm, 110 * mm, "")
    canvas.drawString(41 * mm, 110 * mm, "")
    canvas.drawString(77 * mm, 110 * mm, "Real")
    canvas.drawString(97 * mm, 110 * mm, "")
    canvas.drawString(127 * mm, 110 * mm, "")


def create_boleto_form_xobject(template_function):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.beginForm("boleto_form")
    
    template_function(c)
    
    c.endForm()
    c.save()
    buffer.seek(0)
    
    return buffer.read()