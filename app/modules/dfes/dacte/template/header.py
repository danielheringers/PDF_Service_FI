from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from app.modules.dfes.dacte.template.utils import generate_qrcode
from app.modules.dfes.dacte.template.utils import generate_barcode
from app.modules.dfes.dacte.template.utils import generate_logo
from app.modules.dfes.dacte.schemas import DactePayload

from app.modules.dfes.dacte.schemas import TIPOS_CTE
from app.modules.dfes.dacte.schemas import TIPOS_SERVICO

from app.utils.utils import safe_getattr
from app.utils.utils import calc_font_size_dynamic

MODAIS_MAP = {
    "rodo": "RODOVIÁRIO",
    "aereo": "AÉREO",
    "ferrov": "FERROVIÁRIO",
    "fluvial": "FLUVIAL",
    "duto": "DUTOVIÁRIO",
    "multimodal": "MULTIMODAL"
}

def obter_titulo_modal(inf_modal: dict) -> str:
    if not isinstance(inf_modal, dict) or not inf_modal:
        return "DESCONHECIDO"
    
    primeira_tag_filha = next(iter(inf_modal.keys()), None)
    if isinstance(primeira_tag_filha, str):
        return MODAIS_MAP.get(primeira_tag_filha, "DESCONHECIDO")
    return "DESCONHECIDO"

def formatar_chave_cte(chave: str) -> str:
    return ' '.join(chave[i:i+4] for i in range(0, len(chave), 4))

def add_header(canvas_obj: canvas.Canvas, data: DactePayload):
    #===============================================
    # INICIO CAPTURA DE DADOS - HEADER
    #===============================================
    cteProc = safe_getattr(data.data, "cteProc")
    CTe = safe_getattr(cteProc, "CTe")
    infCte = safe_getattr(CTe, "infCte")
    infCTeSupl = safe_getattr(CTe, "infCTeSupl")
    
    # Dados do emitente
    emit = safe_getattr(infCte, "emit")
    nome_emitente = safe_getattr(emit, "xNome")
    CNPJ_emitente = safe_getattr(emit, "CNPJ")
    IE_emitente = safe_getattr(emit, "IE")

    # Dados do endereço do emitente
    endereco_emitente = safe_getattr(emit, "enderEmit")
    bairro_emitente = safe_getattr(endereco_emitente, "xBairro")
    CEP_emitente = safe_getattr(endereco_emitente, "CEP")
    lgr_emitente = safe_getattr(endereco_emitente, "xLgr")
    nro_emitente = safe_getattr(endereco_emitente, "nro")
    endereco_completo = f"{lgr_emitente}, {nro_emitente}" if nro_emitente else lgr_emitente
    telefone_emitente = safe_getattr(endereco_emitente, "fone")

    # Dados identificadores do CTe
    ide = safe_getattr(infCte, "ide")
    tp_cte = safe_getattr(ide, "tpCTe")  
    descricao_tp_cte = TIPOS_CTE.get(str(tp_cte), "TIPO DESCONHECIDO")
    tp_serv = safe_getattr(ide, "tpServ") 
    descricao_tp_serv = TIPOS_SERVICO.get(str(tp_serv), "TIPO DESCONHECIDO")
    mod = safe_getattr(ide, "mod")
    serie = safe_getattr(ide, "serie")
    n_cte = safe_getattr(ide, "nCT")
    n_folha = f"0{canvas_obj.getPageNumber()}/01"
    data_emissao = safe_getattr(ide, "dhEmi")
    data_emissao = datetime.strptime(data_emissao, "%Y-%m-%dT%H:%M:%S%z")
    data_emissao = data_emissao.strftime("%d/%m/%Y %H:%M:%S")

    # Dados Modal
    inf_cte_norm = safe_getattr(infCte, "infCTeNorm")
    inf_modal = safe_getattr(inf_cte_norm, "infModal")
    titulo_modal = obter_titulo_modal(inf_modal if isinstance(inf_modal, dict) else {})

    # Dados destinatário
    dest = safe_getattr(infCte, "dest")
    CNPJ_destinatario = safe_getattr(dest, "CNPJ")
    IE_destinatario = safe_getattr(dest, "IE")
    ISUF_destinatario = safe_getattr(dest, "ISUF")
    xNome_destinatario = safe_getattr(dest, "xNome")
    endereco_destinatario = safe_getattr(dest, "enderDest")
    bairro_destinatario = safe_getattr(endereco_destinatario, "xBairro")
    CEP_destinatario = safe_getattr(endereco_destinatario, "CEP")
    lgr_destinatario = safe_getattr(endereco_destinatario, "xLgr")
    nro_destinatario = safe_getattr(endereco_destinatario, "nro")
    endereco_completo_destinatario = f"{lgr_destinatario}, {nro_destinatario}" if nro_destinatario else lgr_destinatario

    # Dados da emissão do CTe
    prot_cte = safe_getattr(cteProc, "protCTe")
    inf_prot = safe_getattr(prot_cte, "infProt")
    n_prot = safe_getattr(inf_prot, "nProt")
    chave_acesso = safe_getattr(inf_prot, "chCTe")
    chave_acesso = formatar_chave_cte(chave_acesso)
    dh_recbto = safe_getattr(inf_prot, "dhRecbto")
    dh_recbto = datetime.strptime(dh_recbto, "%Y-%m-%dT%H:%M:%S%z")
    dh_recbto = dh_recbto.strftime("%d/%m/%Y %H:%M:%S")

    # Dados qr code
    qr_cod_cte = safe_getattr(infCTeSupl, "qrCodCTe")

    #===============================================
    # INICIO LAYOUT - MONTAGEM DO HEADER
    #===============================================
    # Inicio montagem do cabeçalho
    largura, altura = A4
    topo = altura - 4 * mm  # margem superior
    margem = 6 * mm

    # Dimensões gerais do cabeçalho
    altura_cabecalho = 58 * mm
    largura_total = largura - 2 * margem

    # Divisão em 3 colunas (aproximadas)
    largura_esquerda = 80 * mm
    largura_direita = 35 * mm
    largura_centro = largura_total - (largura_esquerda + largura_direita)

    # Bloco esquerdo: 1ªa linha - Logo e dados da empresa
    x_esquerda = margem
    y_cabecalho = topo
    canvas_obj.rect(x_esquerda, y_cabecalho - altura_cabecalho, largura_esquerda, altura_cabecalho)

    logo_base64 = safe_getattr(data, "logo_base64")     
    logo = generate_logo(logo_base64)
    canvas_obj.drawImage(logo, (x_esquerda - 9) * mm, y_cabecalho - 28 * mm, width=28*mm, height=14*mm,preserveAspectRatio=True, mask='auto')

    tamanho_fonte = calc_font_size_dynamic(12, 25, len(nome_emitente))
    canvas_obj.setFont("Helvetica-Bold", tamanho_fonte)
    canvas_obj.drawCentredString(x_esquerda + largura_esquerda / 2, y_cabecalho - 5 * mm, nome_emitente)

    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_esquerda + 34 * mm, y_cabecalho - 13 * mm, endereco_completo)
    canvas_obj.drawString(x_esquerda + 34 * mm, y_cabecalho - 17 * mm, bairro_emitente)
    canvas_obj.drawString(x_esquerda + 34 * mm, y_cabecalho - 21 * mm, f"CEP: {CEP_emitente}")
    canvas_obj.drawString(x_esquerda + 34 * mm, y_cabecalho - 25 * mm, f"CNPJ: {CNPJ_emitente}")
    canvas_obj.drawString(x_esquerda + 34 * mm, y_cabecalho - 29 * mm, f"INSCRIÇÃO ESTADUAL: {IE_emitente}")
    canvas_obj.drawString(x_esquerda + 34 * mm, y_cabecalho - 33 * mm, f"TELEFONE: {telefone_emitente}")
    
    # Bloco esquerdo: 2ª linha 1ª fileira - Tipo CTe
    canvas_obj.line(x_esquerda, y_cabecalho - 40 * mm, largura_centro + 3 * mm, y_cabecalho - 40 * mm)
    canvas_obj.setFont("Helvetica", 5)
    canvas_obj.drawString(x_esquerda + 1 * mm, y_cabecalho - 42 * mm, "TIPO DO CT-E:")
    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawString(x_esquerda + 1 * mm, y_cabecalho - 46 * mm, descricao_tp_cte)

    # Bloco esquerdo: 2ª linha 2ª fileira - Tipo Serviço
    canvas_obj.line(x_esquerda + largura_centro / 2, y_cabecalho - 40 * mm, x_esquerda + largura_centro / 2, y_cabecalho - 48 * mm)
    canvas_obj.setFont("Helvetica", 5)
    canvas_obj.drawString(x_esquerda + largura_centro / 2 + 1 * mm, y_cabecalho - 42 * mm, "TIPO DO SERVIÇO:")
    tamanho_fonte = calc_font_size_dynamic(8, 21, len(descricao_tp_serv))
    canvas_obj.setFont("Helvetica-Bold", tamanho_fonte)
    canvas_obj.drawString(x_esquerda + largura_centro / 2 + 1 * mm, y_cabecalho - 46 * mm, descricao_tp_serv)
    
    # Bloco esquerdo: 3ª linha 1ª fileira - Indicador CTe
    canvas_obj.line(x_esquerda, y_cabecalho - 48 * mm, largura_centro + 3 * mm, y_cabecalho - 48 * mm)
    canvas_obj.setFont("Helvetica", 5)
    canvas_obj.drawString(x_esquerda + 1 * mm, y_cabecalho - 50 * mm, "INDICADOR DO CT-E GLOBALIZADO:")
    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawString(x_esquerda + 1 * mm, y_cabecalho - 55 * mm, "NÃO")
    
    # Bloco esquerdo: 3ª linha 2ª fileira - Informações CTe
    canvas_obj.line(x_esquerda + largura_centro / 2, y_cabecalho - 48 * mm, x_esquerda + largura_centro / 2, y_cabecalho - 58 * mm)
    canvas_obj.setFont("Helvetica", 5)
    canvas_obj.drawString(x_esquerda + largura_centro / 2 + 1 * mm, y_cabecalho - 50 * mm, "INFO DE CT-E GLOBALIZADO:")
    
    # Bloco central: DACTE + código de barras + chave
    x_centro = x_esquerda + largura_esquerda
    canvas_obj.rect(x_centro, y_cabecalho - altura_cabecalho, largura_centro, altura_cabecalho)

    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawCentredString(x_centro + largura_centro / 2, y_cabecalho - 5 * mm, "DACTE")
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawCentredString(x_centro + largura_centro / 2, y_cabecalho - 8 * mm, "Documento Auxiliar do Conhecimento de Transporte Eletrônico")

    # Bloco central: 1º linha - Cabeçalho tabela (modelo, série, número etc)
    labels = ["MODELO", "SÉRIE", "NÚMERO", "FOLHA", "DATA E HORA DE EMISSÃO"]
    valores = [mod, serie, n_cte, n_folha, data_emissao]
    largura_col = [12 * mm, 10 * mm, 20 * mm, 10 * mm, 31 * mm]
    x = x_centro
    for i, (label, valor) in enumerate(zip(labels, valores)):
        canvas_obj.rect(x, y_cabecalho - 18 * mm, largura_col[i], 8 * mm)
        canvas_obj.setFont("Helvetica", 6)
        canvas_obj.drawCentredString(x + largura_col[i] / 2, y_cabecalho - 13 * mm, label)
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.drawCentredString(x + largura_col[i] / 2, y_cabecalho - 16 * mm, valor)
        x += largura_col[i]

    # Bloco central: 2º linha - Código de barras (exemplo com barcode_value)
    barcode_value = chave_acesso
    barcode = generate_barcode(barcode_value)
    barcode.drawOn(canvas_obj, x_centro - 4.2 * mm, y_cabecalho - 28 * mm)

    # Bloco central: 3º linha - Chave de acesso 
    canvas_obj.line(x_centro, y_cabecalho - 30 * mm, x_centro + largura_centro, y_cabecalho - 30 * mm)
    
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_centro + 2 * mm, y_cabecalho - 33 * mm, "Chave de acesso")
    canvas_obj.setFont("Helvetica-Bold", 8.25)
    canvas_obj.drawString(x_centro + 2 * mm, y_cabecalho - 37 * mm, chave_acesso)

    # Bloco central: 4º linha - Consulta de auteticidade 
    canvas_obj.line(x_centro, y_cabecalho - 40 * mm, x_centro + largura_centro, y_cabecalho - 40 * mm)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawCentredString(x_centro + largura_centro / 2, y_cabecalho - 44 * mm, "Consulta de autenticidade no portal nacional do CT-e, e no site da Sefaz")
    canvas_obj.drawCentredString(x_centro + largura_centro / 2, y_cabecalho - 46 * mm, "Autorizadora, ou em http://www.cte.fazenda.gov.br/portal")
    
    # Bloco central: 5º linha - Protocolo de autorização
    x_direita = x_centro + largura_centro
    
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.setFillColorRGB(255, 255, 255)
    canvas_obj.rect(x_centro, y_cabecalho - 58 * mm, largura_centro + largura_direita, 10 * mm, fill=1)
    canvas_obj.setFillColorRGB(0, 0, 0)
    canvas_obj.drawString(x_centro + 5, y_cabecalho - 51 * mm, "PROTOCOLO DE AUTORIZAÇÃO DE USO")
    canvas_obj.setFont("Helvetica-Bold", 11)
    canvas_obj.drawString(x_centro + 17 * mm, y_cabecalho - 56 * mm, f"{n_prot}     {dh_recbto}")

    # Bloco direito: 1ª linha - Titulo
    canvas_obj.rect(x_direita, y_cabecalho - (altura_cabecalho - 10 * mm), largura_direita, (altura_cabecalho - 10 * mm))

    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawCentredString(x_direita + largura_direita / 2, y_cabecalho - 4 * mm, "MODAL")
    canvas_obj.drawCentredString(x_direita + largura_direita / 2, y_cabecalho - 7 * mm, titulo_modal)
    
    # Bloco direito: 2ª linha - Dados do destinatário
    canvas_obj.line(x_direita, y_cabecalho - 10 * mm, x_direita + largura_direita, y_cabecalho - 10 * mm)
    canvas_obj.setFont("Helvetica", 5)
    canvas_obj.drawString(x_direita + 1 * mm, y_cabecalho - 12.5 * mm, "ISCR. SUFRAMA DO DESTINATÁRIO:")
    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawString(x_direita + 1 * mm, y_cabecalho - 16.5 * mm, ISUF_destinatario)
    canvas_obj.line(x_direita, y_cabecalho - 18 * mm, x_direita + largura_direita, y_cabecalho - 18 * mm)


    # Bloco direito: 3ª linha - QR code
    qrcode_img = generate_qrcode(qr_cod_cte)
    canvas_obj.drawImage(qrcode_img, x_direita + 3.2 * mm, y_cabecalho - 47 * mm, width=28*mm, height=28*mm)

