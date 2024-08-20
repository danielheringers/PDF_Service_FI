import time
import sys
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from reportlab.lib.utils import ImageReader
from io import BytesIO
from app.Models.Boleto.models import Boleto
from app.Utils.Boleto.banks import bank_names
from app.Utils.Boleto.utils import (
    formatar_cnpj_cpf,
    escrever_texto,
    instrucoes_de_pagamento
)


def create_pdf_boleto(data: Boleto)-> BytesIO:
    start_time = time.time()
    buffer = BytesIO()
    canvas_draw = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 15 * mm
    page_number = 0
    if page_number > 0:
        canvas_draw.showPage()
    page_number += 1
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data.payment_info.qr_code_pix)

    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer_qr = BytesIO()
    img.save(buffer_qr, format="PNG")
    buffer_qr.seek(0)
    image_reader = ImageReader(buffer_qr)


    canvas_draw.drawImage(image_reader, 115 * mm, 56 * mm, width=100, height=100)

    bank = data.bank_account.bank
    bank_name = bank_names.get(bank, "Banco desconhecido")
    bank_code = data.bank_code

    texts_row_one = [
        (bank_code, 78, 280, 16, True, False),
        ("Recibo do Pagador", "right - 30", 278, 9, True, False)
    ]
    escrever_texto(canvas_draw, texts_row_one, margin, width)

    primeira_linha = margin
    segunda_linha = 70 * mm
    largura_total = (segunda_linha - primeira_linha) - 2 * mm

    font_name = "Helvetica-Bold"
    tamanho_max_font = 30
    tamanho_min_font = 1

    while tamanho_max_font > tamanho_min_font:
        canvas_draw.setFont(font_name, tamanho_max_font)
        text_width = canvas_draw.stringWidth(bank_name, font_name, tamanho_max_font)
        
        if text_width <= largura_total:
            break
        
        tamanho_max_font -= 0.5

    canvas_draw.setFont(font_name, tamanho_max_font)
    canvas_draw.drawCentredString((primeira_linha + segunda_linha) / 2, 279.5 * mm, bank_name)

    canvas_draw.line(margin, 287 * mm, width - margin, 287 * mm) 
    canvas_draw.line(margin, 287 * mm, margin, 277 * mm) 
    canvas_draw.line(70 * mm, 287 * mm, 70 * mm, 277 * mm) 
    canvas_draw.line(100 * mm, 287 * mm, 100 * mm, 277 * mm) 
    canvas_draw.line(width - margin, 287 * mm, width - margin, 277 * mm) 
    canvas_draw.line(margin, 277 * mm, width - margin, 277 * mm) 

    # Row 2
    texts_row_two = [
        ("Local de pagamento", "margin + 2", 275, 6, True, False),
        ("Pagável em qualquer banco", "margin + 2", 269, 8, True, False),
        ("Vencimento", 152, 275, 6, True, False), 
        (data.billing.calendar.due_date, "right - 4", 269, 8, True, True)
    ]
    escrever_texto(canvas_draw, texts_row_two, margin, width)

    canvas_draw.line(margin, 277 * mm, margin, 267 * mm) 
    canvas_draw.line(150 * mm, 277 * mm, 150 * mm, 267 * mm) 
    canvas_draw.line(width - margin, 277 * mm, width - margin, 267 * mm) 
    canvas_draw.line(margin, 267 * mm, width - margin, 267 * mm) 

    # Row 3
    cpf_cnpj_beneficiario = formatar_cnpj_cpf(data.bank_account.document_number)
    texts_row_three = [
        ("Beneficiário", "margin + 2", 265, 6, True, False),
        (f"{data.bank_account.name} - {cpf_cnpj_beneficiario}", "margin + 2", 259, 8, True, False),
        ("Agência / Código Beneficiário", 152, 265, 6, True, False),  
        (f"{data.bank_account.agency}/{data.bank_account.account_number}-{data.bank_account.account_digit}", "right - 4", 259, 8, True, True)
    ]
    escrever_texto(canvas_draw, texts_row_three, margin, width)

    canvas_draw.line(margin, 267 * mm, margin, 257 * mm) 
    canvas_draw.line(150 * mm, 267 * mm, 150 * mm, 257 * mm) 
    canvas_draw.line(width - margin, 267 * mm, width - margin, 257 * mm) 
    canvas_draw.line(margin, 257 * mm, width - margin, 257 * mm) 

    # Row 4
    texts_row_four = [
        ("Data do Doc.", "margin + 2", 255, 6, True, False),
        (data.billing.calendar.expedition_date, "margin + 2", 250, 8, True, False),
        ("Número Documento", 47, 255, 6, True, False),
        (data.billing.billing_internal_number, 47, 250, 8, True, False),
        ("Espécie Doc.", 77, 255, 6, True, False),
        (data.billing.bank_slip_type, 77, 250, 8, True, False),
        ("Aceite", 97, 255, 6, True, False),
        (data.billing.buyer.knowledgment_of_debt, 97, 250, 8, True, False),
        ("Data Processamento", 127, 255, 6, True, False),
        (data.billing.calendar.expedition_date, 127, 250, 8, True, False),
        ("Nosso Número", 152, 255, 6, True, False),
        (data.billing.billing_provider_number, "right - 4", 250, 8, True, True)
    ]
    escrever_texto(canvas_draw, texts_row_four, margin, width)
    # Row 4 Layout
    canvas_draw.line(margin, 257 * mm, margin, 247 * mm) 
    canvas_draw.line(150 * mm, 257 * mm, 150 * mm, 247 * mm) 
    canvas_draw.line(125 * mm, 257 * mm, 125 * mm, 247 * mm) 
    canvas_draw.line(95 * mm, 257 * mm, 95 * mm, 247 * mm) 
    canvas_draw.line(75 * mm, 257 * mm, 75 * mm, 247 * mm) 
    canvas_draw.line(45 * mm, 257 * mm, 45 * mm, 247 * mm) 
    canvas_draw.line(width - margin, 257 * mm, width - margin, 247 * mm) 
    canvas_draw.line(margin, 247 * mm, width - margin, 247 * mm) 

    # Row 5
    texts_row_five = [
        ("Uso do Banco", "margin + 2", 245, 6, True, False),
        ("", "margin + 2", 240, 8, True, False),
        ("CIP", 41, 245, 6, True, False),
        ("", 41, 240, 8, True, False),
        ("Carteira", 56, 245, 6, True, False),
        (data.bank_account.convenant_code, 56, 240, 8, True, False),
        ("Esp. Moeda", 77, 245, 6, True, False),
        ("Real", 77, 240, 8, True, False),
        ("Quantidade", 97, 245, 6, True, False),
        ("", 97, 240, 8, True, False),
        ("Valor", 127, 245, 6, True, False),
        ("", 127, 240, 8, True, False),
        ("(=) Valor do documento", 152, 245, 6, True, False),
        (f"{data.billing.total}", "right - 4", 240, 8, True, True)
    ]
    escrever_texto(canvas_draw, texts_row_five, margin, width)

    canvas_draw.line(margin, 247 * mm, margin, 237 * mm) 
    canvas_draw.line(150 * mm, 247 * mm, 150 * mm, 237 * mm) 
    canvas_draw.line(125 * mm, 247 * mm, 125 * mm, 237 * mm) 
    canvas_draw.line(95 * mm, 247 * mm, 95 * mm, 237 * mm) 
    canvas_draw.line(75 * mm, 247 * mm, 75 * mm, 237 * mm) 
    canvas_draw.line(55 * mm, 247 * mm, 55 * mm, 237 * mm) 
    canvas_draw.line(40 * mm, 247 * mm, 40 * mm, 237 * mm) 
    canvas_draw.line(width - margin, 247 * mm, width - margin, 237 * mm) 
    canvas_draw.line(margin, 237 * mm, width - margin, 237 * mm)    

    # Row 6
    canvas_draw.setFont('Helvetica-Bold', 6)
    instructionsText = "Instruções (instruções de responsabilidade do beneficiário. Qualquer dúvida sobre este boleto, contate o beneficiário)"
    canvas_draw.drawString(margin + 2 * mm, 237 * mm - 3 * mm, instructionsText)
    texts_row_six = [
        ("(-) Desconto / Abatimento", 152, 235, 6, True, False),  
        ("(-) Outras Deduções", 152, 225, 6, True, False),        
        ("(+) Mora / Multa", 152, 215, 6, True, False),           
        ("(+) Outros Acréscimos", 152, 205, 6, True, False),      
        ("(=) Valor Cobrado", 152, 195, 6, True, False)           
    ]
    escrever_texto(canvas_draw, texts_row_six, margin, width)

    instrucoes_de_pagamento(canvas_draw, 228, 4, data, margin)

    canvas_draw.line(margin, 237 * mm, margin, 187 * mm) 
    canvas_draw.line(150 * mm, 237 * mm, 150 * mm, 187 * mm) 
    canvas_draw.line(width - margin, 237 * mm, width - margin, 187 * mm) 
    canvas_draw.line(165 * mm - margin, 227 * mm, width - margin, 227 * mm) 
    canvas_draw.line(165 * mm - margin, 217 * mm, width - margin, 217 * mm) 
    canvas_draw.line(165 * mm - margin, 207 * mm, width - margin, 207 * mm) 
    canvas_draw.line(165 * mm - margin, 197 * mm, width - margin, 197 * mm) 
    canvas_draw.line(margin, 187 * mm, width - margin, 187 * mm) 

    pagador = f'{data.billing.buyer.name.upper()} - CNPJ/CPF: {formatar_cnpj_cpf(data.billing.buyer.cpf_cnpj)}'
    endereco = f'{data.billing.buyer.address.street_name.upper()}, {data.billing.buyer.address.number} - {data.billing.buyer.address.neighborhood.upper()}'
    cep_cidade_estado = f'{data.billing.buyer.address.postal_code.upper()} - {data.billing.buyer.address.city.upper()} - {data.billing.buyer.address.state.upper()}'
    # Row 7
    texts_row_seven = [
        ("Pagador:", "margin + 2", 184, 6, True, False),
        ("Sacador/Avalista", "margin + 2", 168, 6, True, False),
        ("Autenticação Mecânica", 130, 165, 6, True, False),
        (pagador, "margin + 12", 184, 8, False, False),
        (endereco, "margin + 2", 180.5, 8, False, False),
        (cep_cidade_estado, "margin + 2", 177, 8, False, False)
    ]

    escrever_texto(canvas_draw, texts_row_seven, margin, width)
    # Row 7 Layout
    canvas_draw.line(margin, 187 * mm, margin, 167 * mm)
    canvas_draw.line(width - margin, 187 * mm, width - margin, 167 * mm) 
    canvas_draw.line(margin, 167 * mm, width - margin, 167 * mm)    

    # Segunda parte do boleto
    # Gerador de Código de Barras
    barcode_height = 15 * mm
    barcode = code128.Code128(data.payment_info.bar_code, barWidth=(0.495*mm), barHeight=barcode_height)
    barcode.drawOn(canvas_draw, margin - 6 * mm, 50)

    numero = data.payment_info.bar_code
    campo1 = numero[0:4] + numero[19:24]  # 3419 + 21076
    campo2 = numero[24:34]  # 2107760361
    campo3 = numero[34:43]  # 7338191000
    campo4 = numero[43]  # 2 (DV do código de barras)
    campo5 = numero[5:19]  # 97050000551682 (fator de vencimento e valor)

    digitableLine = f"{campo1[0:5]}.{campo1[5:]} {campo2[0:5]}.{campo2[5:]} {campo3[0:5]}.{campo3[5:]} {campo4} {campo5}"

    text_row_one_p2 = [
        (data.bank_code, 78, 150, 16, True, False),
        (digitableLine, "right - 4", 148, 9.7, True, True)
    ]
    escrever_texto(canvas_draw, text_row_one_p2, margin, width)

    canvas_draw.setFont(font_name, tamanho_max_font)
    canvas_draw.drawCentredString((primeira_linha + segunda_linha) / 2, 149.5 * mm, bank_name)

    canvas_draw.line(margin, 157 * mm, width - margin, 157 * mm) 
    canvas_draw.line(margin, 157 * mm, margin, 147 * mm) 
    canvas_draw.line(70 * mm, 157 * mm, 70 * mm, 147 * mm) 
    canvas_draw.line(100 * mm, 157 * mm, 100 * mm, 147 * mm) 
    canvas_draw.line(width - margin, 157 * mm, width - margin, 147 * mm) 
    canvas_draw.line(margin, 147 * mm, width - margin, 147 * mm) 

    # Row 2
    text_row_two_p2 = [
        ("Local de pagamento", "margin + 2", 145, 6, True, False),
        ("Pagável em qualquer banco", "margin + 2", 139, 8, True, False),
        ("Vencimento", 152, 145, 6, True, False), 
        (data.billing.calendar.due_date, "right - 4", 139, 8, True, True)
    ]

    escrever_texto(canvas_draw, text_row_two_p2, margin, width)

    canvas_draw.line(margin, 147 * mm, margin, 137 * mm) 
    canvas_draw.line(150 * mm, 147 * mm, 150 * mm, 137 * mm) 
    canvas_draw.line(width - margin, 147 * mm, width - margin, 137 * mm) 
    canvas_draw.line(margin, 137 * mm, width - margin, 137 * mm) 

    # Row 3
    text_row_three_p2 = [
        ("Beneficiário", "margin + 2", 135, 6, True, False),
        (f"{data.bank_account.name} - {cpf_cnpj_beneficiario}", "margin + 2", 129, 8, True, False),
        ("Agência / Código Beneficiário", 152, 135, 6, True, False),  
        (f"{data.bank_account.agency}/{data.bank_account.account_number}-{data.bank_account.account_digit}", "right - 4", 129, 8, True, True)
    ]
    escrever_texto(canvas_draw, text_row_three_p2, margin, width)

    canvas_draw.line(margin, 137 * mm, margin, 127 * mm) 
    canvas_draw.line(150 * mm, 137 * mm, 150 * mm, 127 * mm) 
    canvas_draw.line(width - margin, 137 * mm, width - margin, 127 * mm) 
    canvas_draw.line(margin, 127 * mm, width - margin, 127 * mm) 

    # Row 4
    text_row_four_p2 = [
        ("Data do Doc.", "margin + 2", 125, 6, True, False),
        (data.billing.calendar.expedition_date, "margin + 2", 120, 8, True, False),
        ("Número Documento", 47, 125, 6, True, False),
        (data.billing.billing_internal_number, 47, 120, 8, True, False),
        ("Espécie Doc.", 77, 125, 6, True, False),
        (data.billing.bank_slip_type, 77, 120, 8, True, False),
        ("Aceite", 97, 125, 6, True, False),
        (data.billing.buyer.knowledgment_of_debt, 97, 120, 8, True, False),
        ("Data Processamento", 127, 125, 6, True, False),
        (data.billing.calendar.expedition_date, 127, 120, 8, True, False),
        ("Nosso Número", 152, 125, 6, True, False),
        (data.billing.billing_provider_number, "right - 4", 120, 8, True, True)
    ]
    escrever_texto(canvas_draw, text_row_four_p2, margin, width)
    # Row 4 Layout
    canvas_draw.line(margin, 127 * mm, margin, 117 * mm) 
    canvas_draw.line(150 * mm, 127 * mm, 150 * mm, 117 * mm) 
    canvas_draw.line(125 * mm, 127 * mm, 125 * mm, 117 * mm) 
    canvas_draw.line(95 * mm, 127 * mm, 95 * mm, 117 * mm) 
    canvas_draw.line(75 * mm, 127 * mm, 75 * mm, 117 * mm) 
    canvas_draw.line(45 * mm, 127 * mm, 45 * mm, 117 * mm) 
    canvas_draw.line(width - margin, 127 * mm, width - margin, 117 * mm) 
    canvas_draw.line(margin, 117 * mm, width - margin, 117 * mm) 

    # Row 5
    text_row_five_p2 = [
        ("Uso do Banco", "margin + 2", 115, 6, True, False),
        ("", "margin + 2", 110, 8, True, False),
        ("CIP", 41, 115, 6, True, False),
        ("", 41, 110, 8, True, False),
        ("Carteira", 56, 115, 6, True, False),
        (data.bank_account.convenant_code, 56, 110, 8, True, False),
        ("Esp. Moeda", 77, 115, 6, True, False),
        ("Real", 77, 110, 8, True, False),
        ("Quantidade", 97, 115, 6, True, False),
        ("", 97, 110, 8, True, False),
        ("Valor", 127, 115, 6, True, False),
        ("", 127, 110, 8, True, False),
        ("(=) Valor do documento", 152, 115, 6, True, False),
        (f"{data.billing.total}", "right - 4", 110, 8, True, True)
    ]
    escrever_texto(canvas_draw, text_row_five_p2, margin, width)

    canvas_draw.line(margin, 117 * mm, margin, 107 * mm) 
    canvas_draw.line(150 * mm, 117 * mm, 150 * mm, 107 * mm) 
    canvas_draw.line(125 * mm, 117 * mm, 125 * mm, 107 * mm) 
    canvas_draw.line(95 * mm, 117 * mm, 95 * mm, 107 * mm) 
    canvas_draw.line(75 * mm, 117 * mm, 75 * mm, 107 * mm) 
    canvas_draw.line(55 * mm, 117 * mm, 55 * mm, 107 * mm) 
    canvas_draw.line(40 * mm, 117 * mm, 40 * mm, 107 * mm) 
    canvas_draw.line(width - margin, 117 * mm, width - margin, 107 * mm) 
    canvas_draw.line(margin, 107 * mm, width - margin, 107 * mm) 


    # Row 6
    canvas_draw.setFont('Helvetica-Bold', 6)
    instructionsText = "Instruções"
    canvas_draw.drawString(margin + 2 * mm, 107 * mm - 3 * mm, instructionsText)
    text_row_six_p2 = [
        ("(-) Desconto / Abatimento", 152, 105, 6, True, False),  
        ("(-) Outras Deduções", 152, 95, 6, True, False),        
        ("(+) Mora / Multa", 152, 85, 6, True, False),           
        ("(+) Outros Acréscimos", 152, 75, 6, True, False),      
        ("(=) Valor Cobrado", 152, 65, 6, True, False)           
    ]
    escrever_texto(canvas_draw, text_row_six_p2, margin, width)

    canvas_draw.line(margin, 117 * mm, margin, 57 * mm) 
    canvas_draw.line(150 * mm, 117 * mm, 150 * mm, 57 * mm) 
    canvas_draw.line(width - margin, 117 * mm, width - margin, 57 * mm) 
    canvas_draw.line(165 * mm - margin, 97 * mm, width - margin, 97 * mm) 
    canvas_draw.line(165 * mm - margin, 87 * mm, width - margin, 87 * mm) 
    canvas_draw.line(165 * mm - margin, 77 * mm, width - margin, 77 * mm) 
    canvas_draw.line(165 * mm - margin, 67 * mm, width - margin, 67 * mm) 
    canvas_draw.line(margin, 57 * mm, width - margin, 57 * mm) 

    # Row 7
    text_row_seven_p2 = [
        ("Pagador:", "margin + 2", 54, 6, True, False),  
        ("Sacador/Avalista", "margin + 2", 38, 6, True, False),
        ("Autenticação Mecânica", 130, 35, 6, True, False),
        (pagador, "margin + 12", 54, 8, False, False),
        (endereco, "margin + 2", 50.5, 8, False, False),
        (cep_cidade_estado, "margin + 2", 47, 8, False, False),
    ]
    escrever_texto(canvas_draw, text_row_seven_p2, margin, width)
    # Row 7 Layout
    canvas_draw.line(margin, 57 * mm, margin, 37 * mm) 
    canvas_draw.line(width - margin, 57 * mm, width - margin, 37 * mm) 
    canvas_draw.line(margin, 37 * mm, width - margin, 37 * mm)    

    canvas_draw.save()

    buffer.seek(0)

    sys.stdout.buffer.write(buffer.read())
    sys.stdout.buffer.flush()
    end_time = time.time()
    return buffer

