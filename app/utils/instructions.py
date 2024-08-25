from datetime import datetime
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from app.utils.general_pdf_utils import formatar_moeda

def payment_instructions(canvas_draw, x, y, data):
    styles = getSampleStyleSheet()
    instruction_style = styles['Normal']
    instruction_style.fontName = "Helvetica"
    instruction_style.fontSize = 7
    instruction_style.leading = 10

    instructions = []

    amount_details = data.billing.amount_details
    discount = amount_details.discount if amount_details else None
    fine = amount_details.fine if amount_details else None
    interest = amount_details.interest if amount_details else None
    rebate = amount_details.rebate if amount_details else None
    bank_slip_config = data.bank_account.bank_slip_config 
    days_after_due = bank_slip_config.days_valid_after_due if bank_slip_config else None

    if fine and fine.value > 0:
        modality = fine.modality
        if modality == 1:
            instructions.append(f"Multa de {formatar_moeda(fine.value)} após data de vencimento.")
        elif modality == 2:
            instructions.append(f"Multa de {fine.value}% após data de vencimento.")
    
    if interest and interest.value > 0:
        modality = interest.modality
        if modality == 1:
            instructions.append(f"Juros de {formatar_moeda(interest.value)} por dia corrido após o vencimento.")

    if discount and discount.modality:
        modality = discount.modality
        data_desconto = discount.fixed_date[0].date if discount.fixed_date else None
        if data_desconto:
            data_desconto_formatada = datetime.strptime(data_desconto, "%Y-%m-%d").strftime("%d/%m/%Y")
        else:
            data_desconto_formatada = "N/A"
        if modality == 1:
            instructions.append(f"Desconto de {formatar_moeda(discount.fixed_date[0].value)} até {data_desconto_formatada}.")
        elif modality == 2:
            instructions.append(f"Desconto de {discount.value}% até {data_desconto_formatada}.")

    if rebate and rebate.value > 0:
        modality = rebate.modality
        if modality == 1:
            instructions.append(f"Abatimento de {formatar_moeda(rebate.value)} no valor da cobrança.")
        elif modality == 2:
            instructions.append(f"Abatimento de {rebate.value}% no valor da cobrança.")

    if days_after_due and days_after_due > 0:
        instructions.append(f"Não receber após {days_after_due} dias de vencimento.")
    
    instructions.append("Em caso de dúvidas, entre em contato com o beneficiário.")

    # Converta as instruções em parágrafos
    instruction_paragraphs = [Paragraph(instr, instruction_style) for instr in instructions]

    # Desenhe os parágrafos nas coordenadas especificadas
    for paragraph in instruction_paragraphs:
        w, h = paragraph.wrap(0, 0)  # Calcular a largura e altura do parágrafo
        paragraph.drawOn(canvas_draw, x, y)  # Desenha o parágrafo no canvas
        y -= h + 5  # Mova o y para baixo para o próximo parágrafo
