from io import BytesIO
from typing import List

import qrcode
import qrcode.constants
from reportlab.graphics.barcode.common import I2of5
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from app.modules.charges.bankslip.schemas import Boleto
from app.modules.charges.bankslip.template import (draw_bank_header,
                                                   template_boleto)
from app.utils.banks import bank_names
from app.utils.utils import (escrever_texto, formatar_cnpj_cpf,
                             instrucoes_de_pagamento)

def adjust_font_size_for_text(canvas_draw, text, max_width, font_name="Helvetica-Bold", initial_size=30, min_size=1):
    size = initial_size
    while size > min_size:
        canvas_draw.setFont(font_name, size)
        text_width = canvas_draw.stringWidth(text, font_name, size)
        if text_width <= max_width:
            return size
        size -= 0.5
    return min_size

def draw_qr_code(canvas_draw, qr_data, x=114*mm, y=58*mm, w=100, h=100, box_size=10):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer_qr = BytesIO()
    img.save(buffer_qr, format="PNG") # type: ignore
    buffer_qr.seek(0)
    image_reader = ImageReader(buffer_qr)
    canvas_draw.drawImage(image_reader, x, y, width=w, height=h)

def create_pdf_boleto(bankslip: List[Boleto]) -> BytesIO:
    buffer = BytesIO()
    canvas_draw = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 15 * mm
    page_number = 0
    font_name = "Helvetica-Bold"
    canvas_draw.beginForm("boleto_form")
    template_boleto(canvas_draw)  # desenha o layout fixo no form
    canvas_draw.endForm()

    for data in bankslip:
        if page_number > 0:
            canvas_draw.showPage()
        page_number += 1
        
        canvas_draw.doForm("boleto_form")

        draw_qr_code(canvas_draw, data.payment_info.qr_code_pix, box_size=6)

        bank = data.bank_account.bank
        bank_name = bank_names.get(bank, "Banco desconhecido")
        bank_code = data.bank_code
        draw_bank_header(canvas_draw, bank_name, bank_code, margin, width, top_y_mm=280)

        primeira_linha = margin
        segunda_linha = 70 * mm
        largura_total = (segunda_linha - primeira_linha) - 2 * mm
        tamanho_max_font = adjust_font_size_for_text(
            canvas_draw, bank_name, largura_total, font_name=font_name, initial_size=30, min_size=1
        )

        texts_row_two = [
            (data.billing.calendar.due_date, "right - 4", 269, 8, True, True)
        ]
        escrever_texto(canvas_draw, texts_row_two, margin, width)

        razao_social = data.branch_name or "Não informado"
        cpf_cnpj_beneficiario = formatar_cnpj_cpf(data.bank_account.document_number)
        texts_row_three = [
            (f"{razao_social} - {cpf_cnpj_beneficiario}", "margin + 2", 259, 8, True, False),
            (f"{data.bank_account.agency}/{data.bank_account.account_number}-{data.bank_account.account_digit}", "right - 4", 259, 8, True, True)
        ]
        escrever_texto(canvas_draw, texts_row_three, margin, width)

        texts_row_four = [
            (data.billing.calendar.expedition_date, "margin + 2", 250, 8, True, False),
            (data.billing.billing_internal_number, 47, 250, 8, True, False),
            (data.billing.bank_slip_type, 77, 250, 8, True, False),
            (data.billing.buyer.knowledgment_of_debt, 97, 250, 8, True, False),
            (data.billing.calendar.expedition_date, 127, 250, 8, True, False),
            (data.billing.billing_provider_number, "right - 4", 250, 8, True, True)
        ]
        escrever_texto(canvas_draw, texts_row_four, margin, width)

        texts_row_five = [
            (data.bank_account.convenant_code, 56, 240, 8, True, False),
            (f"{data.billing.total}", "right - 4", 240, 8, True, True)
        ]
        escrever_texto(canvas_draw, texts_row_five, margin, width)
        instrucoes_de_pagamento(canvas_draw, 228, 4, data, margin)

        pagador = f'{data.billing.buyer.name.upper()} - CNPJ/CPF: {formatar_cnpj_cpf(data.billing.buyer.cpf_cnpj)}'
        endereco = f'{data.billing.buyer.address.street_name.upper()}, {data.billing.buyer.address.number} - {data.billing.buyer.address.neighborhood.upper()}'
        cep_cidade_estado = f'{data.billing.buyer.address.postal_code.upper()} - {data.billing.buyer.address.city.upper()} - {data.billing.buyer.address.state.upper()}'
        
        texts_row_seven = [
            (pagador, "margin + 12", 184, 8, False, False),
            (endereco, "margin + 2", 180.5, 8, False, False),
            (cep_cidade_estado, "margin + 2", 177, 8, False, False)
        ]
        escrever_texto(canvas_draw, texts_row_seven, margin, width)
        
        altura = 13 * mm
        comprimento = 103 * mm
        thin_bar = 0.254320987654 * mm
        barcode = I2of5(
            data.payment_info.bar_code,
            barWidth=thin_bar,
            ratio=3,
            barHeight=altura,
            bearers=0,
            quiet=0,
            checksum=0)
        thin_bar = (thin_bar * comprimento) / barcode.width
        barcode.drawOn(canvas_draw, margin + 2 * mm, 60)
        
        numero = data.payment_info.digitable_line
        campo1 = numero[0:5] + '.' + numero[5:10]
        campo2 = numero[10:15] + '.' + numero[15:21]
        campo3 = numero[21:26] + '.' + numero[26:32]
        campo4 = numero[32]
        campo5 = numero[33:]
        digitableLine = f"{campo1} {campo2} {campo3} {campo4} {campo5}"

        text_row_one_p2 = [
            (bank_code, 78, 150, 16, True, False),
            (digitableLine, "right - 3", 148, 8.5, True, True)
        ]
        escrever_texto(canvas_draw, text_row_one_p2, margin, width)
        canvas_draw.setFont(font_name, tamanho_max_font)
        canvas_draw.drawCentredString((primeira_linha + segunda_linha) / 2, 149.5 * mm, bank_name)

        text_row_two_p2 = [
            (data.billing.calendar.due_date, "right - 4", 139, 8, True, True)
        ]
        escrever_texto(canvas_draw, text_row_two_p2, margin, width)

        text_row_three_p2 = [
            (f"{razao_social} - {cpf_cnpj_beneficiario}", "margin + 2", 129, 8, True, False),
            (f"{data.bank_account.agency}/{data.bank_account.account_number}-{data.bank_account.account_digit}", "right - 4", 129, 8, True, True)
        ]
        escrever_texto(canvas_draw, text_row_three_p2, margin, width)

        text_row_four_p2 = [
            (data.billing.calendar.expedition_date, "margin + 2", 120, 8, True, False),
            (data.billing.billing_internal_number, 47, 120, 8, True, False),
            (data.billing.bank_slip_type, 77, 120, 8, True, False),
            (data.billing.buyer.knowledgment_of_debt, 97, 120, 8, True, False),
            (data.billing.calendar.expedition_date, 127, 120, 8, True, False),
            (data.billing.billing_provider_number, "right - 4", 120, 8, True, True)
        ]
        escrever_texto(canvas_draw, text_row_four_p2, margin, width)

        text_row_five_p2 = [
            (data.bank_account.convenant_code, 56, 110, 8, True, False),
            (f"{data.billing.total}", "right - 4", 110, 8, True, True)
        ]
        escrever_texto(canvas_draw, text_row_five_p2, margin, width)
        
        instrucoes_de_pagamento(canvas_draw, 98, 4, data, margin)
        text_row_seven_p2 = [
            (pagador, "margin + 12", 54, 8, False, False),
            (endereco, "margin + 2", 50.5, 8, False, False),
            (cep_cidade_estado, "margin + 2", 47, 8, False, False),
        ]
        escrever_texto(canvas_draw, text_row_seven_p2, margin, width)

    canvas_draw.save()
    buffer.seek(0)

    return buffer
