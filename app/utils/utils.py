import locale
import re
from datetime import datetime
from io import BytesIO

import qrcode
from brutils import format_cnpj, format_cpf, is_valid_cnpj, is_valid_cpf
from PIL import Image
import qrcode.constants
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

from app.modules.charges.bankslip.schemas import Boleto

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_cnpj_cpf(numero):
    numero_str = re.sub(r'\D', '', str(numero))
    if len(numero_str) == 11 and is_valid_cpf(numero_str):
        return format_cpf(numero_str)
    elif len(numero_str) == 14 and is_valid_cnpj(numero_str):
        return format_cnpj(numero_str)
    else:
        return None
    
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

def instrucoes_de_pagamento(canvas_draw, start_y, decrement_mm, data: Boleto, margin):
    instructions = []
    
    amount_details = data.billing.amount_details if data.billing else None
    bank_slip_config = (
        data.bank_account.bank_slip_config
        if data.bank_account and data.bank_account.bank_slip_config
        else None
    )
    amount_details_bank_slip_config = bank_slip_config.amount_details if bank_slip_config else None

    discount = (
        amount_details.discount
        if amount_details is not None
        else amount_details_bank_slip_config.discount
        if amount_details_bank_slip_config is not None
        else None
    )

    fine = (
        amount_details.fine
        if amount_details is not None
        else amount_details_bank_slip_config.fine
        if amount_details_bank_slip_config is not None
        else None
    )

    interest = (
        amount_details.interest
        if amount_details is not None
        else amount_details_bank_slip_config.interest
        if amount_details_bank_slip_config is not None
        else None
    )

    rebate = (
        amount_details.rebate
        if amount_details is not None
        else amount_details_bank_slip_config.rebate
        if amount_details_bank_slip_config is not None
        else None
    )

    days_after_due = bank_slip_config.days_valid_after_due if bank_slip_config else None
    calendar = data.billing.calendar if data.billing else None
    expiration_date = calendar.expiration_date if calendar else None


    if not discount and not fine and not interest and not rebate:
        instructions = [ 
            "Em caso de dúvidas, entre em contato com o beneficiário"
        ]
    else:
        if fine is not None and fine.value > 0:
            modality = fine.modality
            formated_fine = locale.currency(fine.value, grouping=True)
            if modality == 1:
                instructions.append(f"Após o vencimento cobrar multa de {formated_fine}.")
            elif modality == 2:
                instructions.append(f"Após o vencimento cobrar multa de {fine.value:.2f}%.")
        
        if interest is not None and interest.value > 0:
            modality = interest.modality
            formated_interest = locale.currency(interest.value, grouping=True)
            if modality == 1:
                instructions.append(f"Após o vencimento cobrar juros de {formated_interest} por dia.")
            elif modality == 2:
                instructions.append(f"Após o vencimento cobrar juros de {interest.value:.2f}% ao dia.")
            elif modality == 3:
                instructions.append(f"Após o vencimento cobrar juros de {interest.value:.2f}% ao mês.")
            elif modality == 4:
                instructions.append(f"Após o vencimento cobrar juros de {interest.value:.2f}% ao ano.")
            elif modality == 5:
                instructions.append(f"Após o vencimento cobrar juros de {formated_interest} por dia útil.")
            elif modality == 6:
                instructions.append(f"Após o vencimento cobrar juros de {interest.value:.2f}% por dia útil.")

        if discount is not None and "modality" in discount:
            modality = discount.modality
            formated_discount = locale.currency(discount.value, grouping=True)
            data_desconto = discount.get('fixed_date', [{}])[0].get('date', None)
            if data_desconto:
                data_desconto_formatada = datetime.strptime(data_desconto, "%Y-%m-%d").strftime("%d/%m/%Y")
            else:
                data_desconto_formatada = "N/A"
            if modality == 1:
                formated_discount_case = locale.currency(discount['fixed_date'][0].value, grouping=True)
                instructions.append(f"Desconto de {formated_discount_case} até {data_desconto_formatada}")
            elif modality == 2:
                instructions.append(f"Desconto de {discount.value:.2f}% até {data_desconto_formatada}.")
            elif modality == 3:
                instructions.append(f"Desconto de {formated_discount} por dia corrido para pagamento antecipado até o vencimento")
            elif modality == 4:
                instructions.append(f"Desconto de {formated_discount} por dia útil para pagamento antecipado até o vencimento")
            elif modality == 5:
                instructions.append(f"Desconto de {discount.value:.2f}% por dia corrido para pagamento antecipado até o vencimento")
            elif modality == 6:
                instructions.append(f"Desconto de {discount.value:.2f}% por dia útil para pagamento antecipado até o vencimento")

        if rebate is not None and rebate.value > 0:
            modality = rebate.modality
            formated_rebate = locale.currency(rebate.value, grouping=True)
            if modality == 1:
                instructions.append(f"Abatimento de {formated_rebate} no valor da cobrança.")
            elif modality == 2:
                instructions.append(f"Abatimento de {rebate.value:.2f}% no valor da cobrança")

        if days_after_due is not None and days_after_due > 0:
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
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB') # type: ignore

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

def safe_getattr(obj, attr, default=""):
    """
    Obtém um atributo de forma segura, retornando um valor padrão se:
    - O objeto é None
    - O atributo não existe
    - O valor do atributo é None
    """
    if obj is None:
        return default
    value = getattr(obj, attr, default)
    return value if value is not None else default

def calc_font_size_dynamic(default_size: float, limit_field: int, string_length: int) -> float:
    """
    Calcula dinamicamente o tamanho da fonte com base no comprimento do texto e no limite do campo.
    Evita aumentar o tamanho da fonte se o texto for menor que o limite para não quebrar o layout.
    """
    divisor = string_length if string_length > limit_field else limit_field
    return default_size * (limit_field / divisor)    