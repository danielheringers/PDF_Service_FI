# general_pdf_utils.py
import locale
import re
from datetime import datetime
from reportlab.lib.units import mm
from typing import Optional
from app.models.danfe.models import Danfe

def draw_messages(canvas, start_y, decrement_mm, messages, margin):
    start_y_position = start_y * mm
    decrement = decrement_mm * mm
    canvas.setFont("Times-Roman", 7)
    for i, message in enumerate(messages[:7]):
        y_pos = start_y_position - i * decrement
        canvas.drawString(margin + 2 * mm, y_pos, message)

def formatar_moeda(valor):
    try:
        valor_float = float(valor)
        valor_formatado = locale.currency(valor_float, grouping=True).replace('R$', '').strip()
        return valor_formatado
    except ValueError:
        return valor

def draw_wrapped_text(canvas, text, x, y, max_width, line_height):
    canvas.setFont("Times-Roman", 7)
    
    words = text.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width = canvas.stringWidth(word + ' ', "Times-Roman", 7)
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width

    lines.append(' '.join(current_line))
    for line in lines:
        canvas.drawString(x, y, line)
        y -= line_height

def formatar_celular(numero):
    numero = re.sub(r'\D', '', numero)
    if len(numero) == 11:
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    elif len(numero) == 10:
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    else:
        return "Número inválido"

def formatar_chave_acesso(chave):
    return ' '.join(chave[i:i+4] for i in range(0, len(chave), 4))


def get_emissao_details(dados: Danfe) -> Optional[str]:
    for evento in dados.eventos:
        if evento.type == "EMISSÃƒO":
            protocolo = evento.protocolo
            dh_evento = evento.dhEvento
            if protocolo and dh_evento:
                dt = datetime.fromisoformat(dh_evento)
                dh_evento_formatado = dt.strftime("%d/%m/%Y %H:%M:%S")
                return f'{protocolo} - {dh_evento_formatado}'
    return None


def formatar_cnpj_cpf(numero):
    numero_str = re.sub(r'\D', '', str(numero))
    if len(numero_str) == 14:
        return f'{numero_str[:2]}.{numero_str[2:5]}.{numero_str[5:8]}/{numero_str[8:12]}-{numero_str[12:]}'
    elif len(numero_str) == 11:
        return f'{numero_str[:3]}.{numero_str[3:6]}.{numero_str[6:9]}-{numero_str[9:]}'
    else:
        return numero
