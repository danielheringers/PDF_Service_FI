import re 
from reportlab.lib.units import mm
from io import BytesIO
import qrcode
from reportlab.lib.utils import ImageReader
from PIL import Image
from datetime import datetime


def formatar_cnpj_cpf(numero):
    numero_str = re.sub(r'\D', '', str(numero))
    if len(numero_str) == 14:
        return f'{numero_str[:2]}.{numero_str[2:5]}.{numero_str[5:8]}/{numero_str[8:12]}-{numero_str[12:]}'
    elif len(numero_str) == 11:
        return f'{numero_str[:3]}.{numero_str[3:6]}.{numero_str[6:9]}-{numero_str[9:]}'
    else:
        return numero
    
def escrever_mensagens(canvas_draw, start_y, decrement_mm, messages, margin):
    startYPosition = start_y * mm
    decrement = decrement_mm * mm 
    canvas_draw.setFont("Helvetica", 7)

    for i, message in enumerate(messages):
        if i >= 14:
            break
        y_pos = startYPosition - i * decrement
        canvas_draw.drawString(margin + 2 * mm, y_pos, message)

def escrever_texto(canvas, texts, margin, width):

    for text, x, y, font_size, bold, string_width in texts:
        font_name = "Helvetica-Bold" if bold else "Helvetica"
        canvas.setFont(font_name, font_size)
        if isinstance(x, str):
            if 'right' in x:
                offset = float(x.split('-')[1].strip()) * mm
                x_pos = width - margin - offset
            else:
                offset = float(x.split('+')[1].strip()) * mm
                x_pos = margin + offset
        else:
            x_pos = x * mm
        if string_width:
            y_pos = y * mm
            canvas.drawRightString(x_pos, y_pos, str(text))
        else:
            y_pos = y * mm
            canvas.drawString(x_pos, y_pos, str(text))

def formatar_para_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def quebrar_linhas(text, max_width, canvas_draw, font_name, font_size):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if canvas_draw.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines

def instrucoes_de_pagamento(canvas_draw, start_y, decrement_mm, data, margin):
    instructions = []
    
    amount_details = data.billing.amount_details
    discount = amount_details.discount
    fine = amount_details.fine
    interest = amount_details.interest
    rebate = getattr(amount_details, 'rebate', None)
    bank_slip_config = data.bank_account.bank_slip_config
    days_after_due = bank_slip_config.days_valid_after_due
    calendar = data.billing.calendar
    expiration_date = calendar.expiration_date

    if not discount and not fine and not interest and not rebate:
        instructions = [ 
            "Em caso de dúvidas, entre em contato com o beneficiário"
        ]
    else:
        if fine.value > 0:
            modality = fine.modality
            if modality == 1:
                instructions.append(f"Multa de {formatar_para_real(fine.value)} após data de vencimento")
            elif modality == 2:
                instructions.append(f"Multa de {fine.value}% após data de vencimento")
        
        if interest.value > 0:
            modality = interest.modality
            if modality == 1:
                instructions.append(f"Juros de {formatar_para_real(interest.value)} por dia corrido após o vencimento")
            elif modality == 2:
                instructions.append(f"Juros de {interest.value}% ao dia corrido após o vencimento")
            elif modality == 3:
                instructions.append(f"Juros de {interest.value}% ao mês após o vencimento")
            elif modality == 4:
                instructions.append(f"Juros de {interest.value}% ao ano após o vencimento")
            elif modality == 5:
                instructions.append(f"Juros de {formatar_para_real(interest.value)} por dia útil após o vencimento")
            elif modality == 6:
                instructions.append(f"Juros de {interest.value}% por dia útil após o vencimento")
            elif modality == 7:
                instructions.append(f"Juros de {interest.value}% ao mês após o vencimento")
            elif modality == 8:
                instructions.append(f"Juros de {interest.value}% ao ano após o vencimento")

        if discount.modality:
            modality = discount.modality
            data_desconto = discount.fixed_date[0].date if discount.fixed_date else None
            if data_desconto:
                data_desconto_formatada = datetime.strptime(data_desconto, "%Y-%m-%d").strftime("%d/%m/%Y")
            else:
                data_desconto_formatada = "N/A"
            if modality == 1:
                instructions.append(f"Desconto de {formatar_para_real(discount.fixed_date[0].value)} até {data_desconto_formatada}")
            elif modality == 2:
                instructions.append(f"Desconto de {discount.value}% até {data_desconto_formatada}.")
            elif modality == 3:
                instructions.append(f"Desconto de {formatar_para_real(discount.value)} por dia corrido para pagamento antecipado até o vencimento")
            elif modality == 4:
                instructions.append(f"Desconto de {formatar_para_real(discount.value)} por dia útil para pagamento antecipado até o vencimento")
            elif modality == 5:
                instructions.append(f"Desconto de {discount.value}% por dia corrido para pagamento antecipado até o vencimento")
            elif modality == 6:
                instructions.append(f"Desconto de {discount.value}% por dia útil para pagamento antecipado até o vencimento")

        if rebate and rebate.value > 0:
            modality = rebate.modality
            if modality == 1:
                instructions.append(f"Abatimento de {formatar_para_real(rebate.value)} no valor da cobrança.")
            elif modality == 2:
                instructions.append(f"Abatimento de {rebate.value}% no valor da cobrança")

        if days_after_due > 0:
            instructions.append(f"Não receber após {days_after_due} dias de vencimento.")

        instructions.append("Em caso de dúvidas, entre em contato com o beneficiário")

    startYPosition = start_y * mm
    decrement = decrement_mm * mm
    max_text_width = 100 * mm
    font_name = "Helvetica"
    font_size = 7

    canvas_draw.setFont(font_name, font_size)

    line_count = 0
    for instruction in instructions:
        if line_count >= 10:
            break

        wrapped_lines = quebrar_linhas(instruction, max_text_width, canvas_draw, font_name, font_size)
        for line in wrapped_lines:
            if line_count >= 10:
                break
            y_pos = startYPosition - line_count * decrement
            canvas_draw.drawString(margin + 2 * mm, y_pos, line)
            line_count += 1


# Logo No QR CODE NÃO UTILIZAR AINDA VAMOS DEFINIR NO FUTURO
def create_qr_with_logo(qr_data, logo_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Salvar logo na variavel
    logo = Image.open(logo_path)

    # Calcular Tamanho da logo
    qr_width, qr_height = qr_img.size
    logo_size = int(qr_width / 4)
    logo = logo.resize((logo_size, logo_size))
    logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

    # Colar Logo No Qr Code
    qr_img.paste(logo, logo_pos, mask=logo)

    # Salvar QR Code no buffer
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    return ImageReader(buffer)        