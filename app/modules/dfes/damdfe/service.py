import base64
import gc
from datetime import datetime
from io import BytesIO
from typing import Optional

import qrcode
from brutils import format_cep
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from app.modules.dfes.damdfe.schemas import DamdfePayload
from app.utils.utils import formatar_cnpj_cpf
from app.utils.utils import safe_getattr

def ensure_str(value: Optional[str], default: str = "") -> str:
    """
    Garante que o valor seja uma string. Substitui None por um valor padrão.
    """
    return value if isinstance(value, str) else default

def safe_format_datetime(dt_str):
    """Converte uma string de datetime no formato esperado do MDFe para um formato legível.
       Retorna uma string vazia se dt_str for inválida."""
    if not dt_str:
        return ""
    try:
        # Exemplo de formato: '2023-01-01T10:00:00-03:00'
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime('%d/%m/%Y %H:%M:%S')
    except ValueError:
        return ""

def safe_format_datetime_prot(dt_str):
    """Formata data/hora para o protocolo, retornando uma string no formato '%d/%m/%Y às %H:%M:%S'."""
    if not dt_str:
        return ""
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime('%d/%m/%Y às %H:%M:%S')
    except ValueError:
        return ""

def draw_base_layout(canvas_obj):
    """Desenha o layout base do documento no canvas."""
    canvas_obj.setFont("Helvetica-Bold", 9)
    canvas_obj.drawString(42 * mm, 267 * mm, "CNPJ:")
    canvas_obj.drawString(84 * mm, 267 * mm, "IE:")
    canvas_obj.drawString(111 * mm, 267 * mm, "RNTRC:")
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawString(10 * mm, 257 * mm, "DAMDFE")
    canvas_obj.setFont("Helvetica", 11)
    canvas_obj.drawString(30 * mm, 257 * mm, "- Documento Auxiliar de Manifesto Eletrônico de Documentos Fiscais")
    
    # Retângulos coloridos do cabeçalho
    canvas_obj.setFillColorRGB(0.7, 0.9, 1.0)
    canvas_obj.rect(10 * mm, 239 * mm, 40 * mm, 14 * mm, stroke=0, fill=1)
    canvas_obj.rect(52 * mm, 239 * mm, 20 * mm, 14 * mm, stroke=0, fill=1)
    canvas_obj.rect(74 * mm, 239 * mm, 42 * mm, 14 * mm, stroke=0, fill=1)
    canvas_obj.rect(119 * mm, 239 * mm, 20 * mm, 14 * mm, stroke=0, fill=1)
    canvas_obj.rect(141 * mm, 239 * mm, 21 * mm, 14 * mm, stroke=0, fill=1)
    
    canvas_obj.setFillColorRGB(0.9, 0.9, 0.9)
    canvas_obj.rect(10 * mm, 207 * mm, 20 * mm, 14 * mm, stroke=0, fill=1)
    canvas_obj.rect(32 * mm, 207 * mm, 20 * mm, 14 * mm, stroke=0, fill=1)
    canvas_obj.rect(54 * mm, 207 * mm, 30 * mm, 14 * mm, stroke=0, fill=1)
    
    canvas_obj.setFillColorRGB(0, 0, 0)
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(11 * mm, 249 * mm, "Modelo")
    canvas_obj.drawString(25 * mm, 249 * mm, "Série")
    canvas_obj.drawString(36 * mm, 249 * mm, "Número")
    canvas_obj.drawString(54 * mm, 249 * mm, "FL")
    canvas_obj.drawString(75 * mm, 249 * mm, "Data e hora de Emissão")
    canvas_obj.drawString(120 * mm, 249 * mm, "UF Carreg.")
    canvas_obj.drawString(142 * mm, 249 * mm, "UF Descarreg.")
    canvas_obj.drawString(11 * mm, 217 * mm, "Qtd. CTe")
    canvas_obj.drawString(33 * mm, 217 * mm, "Qtd. NFe")
    canvas_obj.drawString(55 * mm, 217 * mm, "Peso total (kg)") 
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawString(10 * mm, 227 * mm, "Modelo Rodóviário de Carga")
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(100 * mm, 227 * mm, "CONTROLE DO FISCO")
    canvas_obj.setFont("Helvetica-Bold", 10)
    canvas_obj.drawString(10 * mm, 200 * mm, "Protocolo de autorização")
    canvas_obj.drawString(100 * mm, 200 * mm, "Chave de Acesso")
    canvas_obj.drawString(10 * mm, 180 * mm, "Veículo")
    canvas_obj.drawString(100 * mm, 180 * mm, "Condutor")
    canvas_obj.drawString(10 * mm, 175 * mm, "Placa")
    canvas_obj.drawString(30 * mm, 175 * mm, "RNTRC")
    canvas_obj.drawString(100 * mm, 175 * mm, "CPF")
    canvas_obj.drawString(130 * mm, 175 * mm, "Nome")
    canvas_obj.setStrokeColorRGB(0.8, 0.8, 0.8)
    canvas_obj.line(10 * mm, 174 * mm, 90 * mm, 174 * mm)
    canvas_obj.line(100 * mm, 174 * mm, 200 * mm, 174 * mm)
    canvas_obj.setFont("Helvetica-Bold", 10)
    canvas_obj.drawString(10 * mm, 150 * mm, "Vale Pedágio")
    canvas_obj.setFont("Helvetica-Bold", 7)
    canvas_obj.drawString(10 * mm, 145 * mm, "Responsável CNPJ")
    canvas_obj.drawString(45 * mm, 145 * mm, "Fornecedor CNPJ")
    canvas_obj.drawString(79 * mm, 145 * mm, "Nº Comprovante")
    canvas_obj.setStrokeColorRGB(0.8, 0.8, 0.8)
    canvas_obj.line(10 * mm, 144 * mm, 99 * mm, 144 * mm)
    canvas_obj.setStrokeColorRGB(0, 0, 0)

def generate_damdfe_pdf_bytes(damdfe: DamdfePayload) -> BytesIO:
    # Obtenção segura dos dados
    MDFe = safe_getattr(damdfe, "MDFe")
    retMDFe = safe_getattr(damdfe, "retMDFe")
    infMDFeSupl = safe_getattr(MDFe, "infMDFeSupl")
    ide = safe_getattr(MDFe, "ide")
    emit = safe_getattr(MDFe, "emit")
    enderEmit = safe_getattr(emit, "enderEmit")
    infModal = safe_getattr(MDFe, "infModal")
    rodo = safe_getattr(infModal, "rodo")
    infANTT = safe_getattr(rodo, "infANTT")
    veicTracao = safe_getattr(rodo, "veicTracao")
    veicReboque = safe_getattr(rodo, "veicReboque", [])
    condutor = safe_getattr(veicTracao, "condutor")
    tot = safe_getattr(MDFe, "tot")
    protMDFe = safe_getattr(retMDFe, "protMDFe")
    infProt = safe_getattr(protMDFe, "infProt")

    # Datas formatadas
    emission_formatted_date = safe_format_datetime(safe_getattr(ide, "dhEmi"))
    nProt_formatted_date = safe_format_datetime_prot(safe_getattr(infProt, "dhRecbto"))

    buffer = BytesIO()
    canvas_draw = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    marginTOP = height - 15 * mm
    page_count = 1

    # Desenha layout base
    draw_base_layout(canvas_draw)

    # QRCode
    qr_data = safe_getattr(infMDFeSupl, "qrCodMDFe")
    if qr_data:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_code_image = qr.make_image(fill_color="black", back_color="white")
        buffer_qr = BytesIO()
        qr_code_image.save(buffer_qr, format="PNG")
        buffer_qr.seek(0)
        image_reader = ImageReader(buffer_qr)
        canvas_draw.drawImage(image_reader, 165 * mm, marginTOP - 30 * mm, width=117, height=117)

    # Código de barras
    chMDFe = safe_getattr(infProt, "chMDFe")
    if chMDFe:
        barcode_height = 15 * mm
        barcode_width = 0.3 * mm
        barcode = code128.Code128(chMDFe, barWidth=barcode_width, barHeight=barcode_height)
        barcode.drawOn(canvas_draw, 94 * mm, 207 * mm)

    # Logo
    canvas_draw.rect(10 * mm, marginTOP - 15 * mm, 30 * mm, 18 * mm, stroke=1, fill=0)
    logo = safe_getattr(MDFe, "logo")
    if logo:
        try:
            logo_data = base64.b64decode(logo)
            logo_image = ImageReader(BytesIO(logo_data))
            canvas_draw.drawImage(logo_image, 10 * mm, marginTOP - 15 * mm, width=30 * mm, height=18 * mm)
        except Exception as e:
            print(f"Erro ao decodificar o logo: {e}")

    # Dados Emitente
    xNome = ensure_str(safe_getattr(emit, "xNome"))
    xLgr = ensure_str(safe_getattr(enderEmit, "xLgr"))
    nro = ensure_str(safe_getattr(enderEmit, "nro"))
    xBairro = ensure_str(safe_getattr(enderEmit, "xBairro"))
    xCpl = ensure_str(safe_getattr(enderEmit, "xCpl"))
    xMun = ensure_str(safe_getattr(enderEmit, "xMun"))
    UF = ensure_str(safe_getattr(enderEmit, "UF"))
    CEP = ensure_str(safe_getattr(enderEmit, "CEP"))
    CNPJ_emit = ensure_str(safe_getattr(emit, "CNPJ"))
    IE_emit = ensure_str(safe_getattr(emit, "IE"))
    RNTRC = ensure_str(safe_getattr(infANTT, "RNTRC"))

    # Desenho dos dados
    canvas_draw.setFont("Helvetica-Bold", 12)
    canvas_draw.drawString(42 * mm, marginTOP, xNome)
    canvas_draw.setFont("Helvetica", 10)
    endereco_full = f'{xLgr}, {nro}, {xBairro}'
    if xCpl:
        endereco_full += f', {xCpl}'
    canvas_draw.drawString(42 * mm, marginTOP - 5 * mm, endereco_full + '.')
    canvas_draw.drawString(42 * mm, marginTOP - 10 * mm, f'{xMun} - {UF}')
    canvas_draw.drawString(75 * mm, marginTOP - 10 * mm, f'CEP: {format_cep(CEP)}')
    canvas_draw.setFont("Helvetica", 9)
    canvas_draw.drawString(52 * mm, marginTOP - 15 * mm, formatar_cnpj_cpf(CNPJ_emit))
    canvas_draw.drawString(89 * mm, marginTOP - 15 * mm, IE_emit)
    canvas_draw.drawString(124 * mm, marginTOP - 15 * mm, RNTRC)

    # Cabeçalho do documento
    mod = ensure_str(safe_getattr(ide, "mod"))
    serie = ensure_str(safe_getattr(ide, "serie"))
    nMDF = ensure_str(safe_getattr(ide, "nMDF"))
    UFIni = ensure_str(safe_getattr(ide, "UFIni"))
    UFFim = ensure_str(safe_getattr(ide, "UFFim"))
    tpEmis = ensure_str(safe_getattr(ide, "tpEmis"))

    canvas_draw.setFont("Helvetica-Bold", 12)
    canvas_draw.drawString(11 * mm, 242 * mm, mod)
    canvas_draw.drawString(25 * mm, 242 * mm, serie)
    canvas_draw.drawString(36 * mm, 242 * mm, nMDF)
    # Contador de páginas
    canvas_draw.drawString(54 * mm, 242 * mm, f'1/{page_count}')
    canvas_draw.drawString(75 * mm, 242 * mm, emission_formatted_date)
    canvas_draw.drawString(120 * mm, 242 * mm, UFIni)
    canvas_draw.drawString(142 * mm, 242 * mm, UFFim)

    qCTe = ensure_str(safe_getattr(tot, "qCTe"))
    qNFe = ensure_str(safe_getattr(tot, "qNFe"))
    qCarga = ensure_str(safe_getattr(tot, "qCarga"))

    if qCTe:
        canvas_draw.drawString(11 * mm, 210 * mm, qCTe)
    if qNFe:
        canvas_draw.drawString(33 * mm, 210 * mm, qNFe)
    if qCarga:
        canvas_draw.drawString(55 * mm, 210 * mm, qCarga)

    # Protocolo / Contingência
    canvas_draw.setFont("Helvetica", 9)
    nProt = ensure_str(safe_getattr(infProt, "nProt"))
    if tpEmis == "1" and nProt:
        canvas_draw.drawString(10 * mm, 195 * mm, f'{nProt} - {nProt_formatted_date}')
    else:
        # Contingência
        canvas_draw.setFillColorRGB(0, 0, 0)
        canvas_draw.rect(10 * mm, 189 * mm, 81 * mm, 10 * mm, stroke=0, fill=1)
        canvas_draw.setFillColorRGB(1, 1, 1)
        canvas_draw.setFont("Helvetica-Bold", 8)
        canvas_draw.drawString(12 * mm, 195 * mm, "EMITIDO EM CONTINGÊNCIA.")
        canvas_draw.setFont("Helvetica", 8)
        canvas_draw.drawString(53 * mm, 195 * mm, "Obrigatória a autorização em")
        canvas_draw.drawString(12 * mm, 191 * mm, f'168 horas após esta emissão {emission_formatted_date}')
        canvas_draw.setFillColorRGB(0, 0, 0)

    # Chave de Acesso e Consulta
    if chMDFe:
        canvas_draw.drawString(100 * mm, 195 * mm, chMDFe)
    canvas_draw.setFont("Helvetica", 8)
    canvas_draw.drawString(100 * mm, 190 * mm, "Consulte em https://dfe-portalsefazvirtual.rs.gov.br/MDFe/consulta")

    canvas_draw.setFont("Helvetica-Bold", 9)

    # Veículo e Condutor
    placa_veic = ensure_str(safe_getattr(veicTracao, "placa"))
    CPF_cond = ensure_str(safe_getattr(condutor, "CPF"))
    xNome_cond = ensure_str(safe_getattr(condutor, "xNome"))

    canvas_draw.drawString(10 * mm, 170 * mm, placa_veic)
    canvas_draw.drawString(30 * mm, 170 * mm, RNTRC)
    canvas_draw.drawString(100 * mm, 170 * mm, CPF_cond)
    canvas_draw.drawString(130 * mm, 170 * mm, xNome_cond)

    # Reboques
    y_position = 165 * mm
    for index, reboque in enumerate(veicReboque):
        placa_reb = ensure_str(safe_getattr(reboque, "placa"))
        canvas_draw.drawString(10 * mm, y_position, placa_reb)
        canvas_draw.drawString(30 * mm, y_position, RNTRC)
        y_position -= 5 * mm

    # Vale-Pedágio
    if infANTT and infANTT.valePed:
        valePed = safe_getattr(infANTT, "valePed")
        disp = safe_getattr(valePed, "disp", [])
        y_position = 140 * mm
        canvas_draw.setFont("Helvetica-Bold", 7)
        for vale_pedagio in disp:
            CNPJPg = ensure_str(formatar_cnpj_cpf(safe_getattr(vale_pedagio, "CNPJPg")))
            CNPJForn = ensure_str(formatar_cnpj_cpf(safe_getattr(vale_pedagio, "CNPJForn")))
            nCompra = ensure_str(safe_getattr(vale_pedagio, "nCompra"))

            # Checa se precisa de nova página
            if y_position < 20 * mm:
                canvas_draw.showPage()
                draw_base_layout(canvas_draw)
                y_position = height - 20 * mm
            
            canvas_draw.drawString(10 * mm, y_position, CNPJPg)
            canvas_draw.drawString(45 * mm, y_position, CNPJForn)
            canvas_draw.drawString(79 * mm, y_position, nCompra)
            y_position -= 5 * mm

    # Observações
    if y_position < 20 * mm:
        canvas_draw.showPage()
        draw_base_layout(canvas_draw)
        y_position = height - 20 * mm

    canvas_draw.drawString(10 * mm, y_position - 5 * mm, "Observações")
    canvas_draw.setStrokeColorRGB(0.8, 0.8, 0.8)
    canvas_draw.line(10 * mm, y_position - 6 * mm, 200 * mm, y_position - 6 * mm)
    canvas_draw.setStrokeColorRGB(0, 0, 0)

    # Próxima página (se necessário)
    canvas_draw.showPage()
    gc.collect()
    # Finaliza o PDF
    canvas_draw.save()
    buffer.seek(0)

    return buffer
