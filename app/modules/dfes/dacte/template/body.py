from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from app.modules.dfes.dacte.schemas import DactePayload
from app.utils.utils import safe_getattr, calc_font_size_dynamic
from app.modules.dfes.dacte.schemas import TIPOS_CST

from app.modules.dfes.dacte.template.groups.documentos_originarios_anteriores import componentes_originarios_anteriores, DocumentoOriginarioAnterior

import locale

def add_body(canvas_obj: canvas.Canvas, data: DactePayload):
    #===============================================
    # INICIO CAPTURA DE DADOS - BODY
    #===============================================
    # Dados de Status do CTe
    status = safe_getattr(data, "status")
    status = "CANCELADO" if status == "CANCELADA" else "AUTORIZADO"
    
    # Dados do CTe
    cteProc = safe_getattr(data.data, "cteProc")
    CTe = safe_getattr(cteProc, "CTe")
    infCte = safe_getattr(CTe, "infCte")

     # Dados identificadores do CTe
    ide = safe_getattr(infCte, "ide")
    CFOP = safe_getattr(ide, "CFOP")
    natOp = safe_getattr(ide, "natOp")
    UFIni = safe_getattr(ide, "UFIni")
    xMunIni = safe_getattr(ide, "xMunIni")
    UFFim = safe_getattr(ide, "UFFim")
    xMunFim = safe_getattr(ide, "xMunFim")

    # Dados remetente
    rem = safe_getattr(infCte, "rem")
    xNome_remetente = safe_getattr(rem, "xNome")
    fone_remetente = safe_getattr(rem, "fone")
    IE_remetente = safe_getattr(rem, "IE")
    CNPJ_remetente = safe_getattr(rem, "CNPJ")
    enderReme = safe_getattr(rem, "enderReme")
    xLgr_remetente = safe_getattr(enderReme, "xLgr")
    nro_remetente = safe_getattr(enderReme, "nro")
    xCpl_remetente = safe_getattr(enderReme, "xCpl")
    xMun_remetente = safe_getattr(enderReme, "xMun")
    xPais_remetente = safe_getattr(enderReme, "xPais")
    xBairro_remetente = safe_getattr(enderReme, "xBairro")
    UF_remetente = safe_getattr(enderReme, "UF")

    #Dados destinatario
    dest = safe_getattr(infCte, "dest")
    CNPJ_destinatario = safe_getattr(dest, "CNPJ")
    xNome_destinatario = safe_getattr(dest, "xNome")
    IE_destinatario = safe_getattr(dest, "IE")
    fone_destinatario = safe_getattr(dest, "fone")
    enderDest = safe_getattr(dest, "enderDest")
    xLgr_destinatario = safe_getattr(enderDest, "xLgr")
    nro_destinatario = safe_getattr(enderDest, "nro")
    xCpl_destinatario = safe_getattr(enderDest, "xCpl")
    xMun_destinatario = safe_getattr(enderDest, "xMun")
    xPais_destinatario = safe_getattr(enderDest, "xPais")
    xBairro_destinatario = safe_getattr(enderDest, "xBairro")
    UF_destinatario = safe_getattr(enderDest, "UF")

    #Dados expedidor
    exped = safe_getattr(infCte, "exped")
    CNPJ_expedidor = safe_getattr(exped, "CNPJ")
    xNome_expedidor = safe_getattr(exped, "xNome")
    IE_expedidor = safe_getattr(exped, "IE")
    fone_expedidor = safe_getattr(exped, "fone")
    enderExped = safe_getattr(exped, "enderExped")
    xLgr_expedidor = safe_getattr(enderExped, "xLgr")
    nro_expedidor = safe_getattr(enderExped, "nro")
    xCpl_expedidor = safe_getattr(enderExped, "xCpl")
    xMun_expedidor = safe_getattr(enderExped, "xMun")
    xPais_expedidor = safe_getattr(enderExped, "xPais")
    xBairro_expedidor = safe_getattr(enderExped, "xBairro")
    UF_expedidor = safe_getattr(enderExped, "UF")

    # Dados recebedor
    receb = safe_getattr(infCte, "receb")
    CNPJ_recebedor = safe_getattr(receb, "CNPJ")
    xNome_recebedor = safe_getattr(receb, "xNome")
    IE_recebedor = safe_getattr(receb, "IE")
    fone_recebedor = safe_getattr(receb, "fone")
    enderReceb = safe_getattr(receb, "enderReceb")
    xLgr_recebedor = safe_getattr(enderReceb, "xLgr")
    nro_recebedor = safe_getattr(enderReceb, "nro")
    xCpl_recebedor = safe_getattr(enderReceb, "xCpl")
    xMun_recebedor = safe_getattr(enderReceb, "xMun")
    xPais_recebedor = safe_getattr(enderReceb, "xPais")
    xBairro_recebedor = safe_getattr(enderReceb, "xBairro")
    UF_recebedor = safe_getattr(enderReceb, "UF")

    # Dados de toma, toma3 ou toma4
    toma = safe_getattr(infCte, "toma")
    if safe_getattr(infCte, "toma"):
        toma = safe_getattr(infCte, "toma")
        enderToma = safe_getattr(toma, "enderToma")
    if safe_getattr(ide, "toma3"):
        toma3 = safe_getattr(ide, "toma3")
        if safe_getattr(toma3, "toma") == "0":
            toma = rem
            enderToma = enderReme
        if safe_getattr(toma3, "toma") == "1":
            toma = exped
            enderToma = enderExped
        if safe_getattr(toma3, "toma") == "2":
            toma = receb
            enderToma = enderReceb
        if safe_getattr(toma3, "toma") == "3":
            toma = dest
            enderToma = enderDest
    if safe_getattr(ide, "toma4"):
        toma = safe_getattr(ide, "toma4")
        enderToma = safe_getattr(toma, "enderToma")
    if safe_getattr(infCte, "toma") and safe_getattr(ide, "toma4"):
        toma = safe_getattr(infCte, "toma")
        enderToma = safe_getattr(toma, "enderToma")
    xNome_toma = safe_getattr(toma, "xNome")
    CNPJ_toma = safe_getattr(toma, "CNPJ")
    IE_toma = safe_getattr(toma, "IE")
    fone_toma = safe_getattr(toma, "fone")
    xLgr_toma = safe_getattr(enderToma, "xLgr")
    nro_toma = safe_getattr(enderToma, "nro")
    xMun_toma = safe_getattr(enderToma, "xMun")
    xPais_toma = safe_getattr(enderToma, "xPais")
    UF_toma = safe_getattr(enderToma, "UF")

    # Dados do imposto
    imp = safe_getattr(infCte, "imp")
    ICMS = safe_getattr(imp, "ICMS")
    if safe_getattr(imp, "ICMS"):
        if safe_getattr(ICMS, "ICMS00"):
            ICMS = safe_getattr(ICMS, "ICMS00")
        elif safe_getattr(ICMS, "ICMS20"):
            ICMS = safe_getattr(ICMS, "ICMS20")
        elif safe_getattr(ICMS, "ICMS45"):
            ICMS = safe_getattr(ICMS, "ICMS45")
        elif safe_getattr(ICMS, "ICMS60"):
            ICMS = safe_getattr(ICMS, "ICMS60")
        elif safe_getattr(ICMS, "ICMS90"):
            ICMS = safe_getattr(ICMS, "ICMS90")
        elif safe_getattr(ICMS, "ICMSOutraUF"):
            ICMS = safe_getattr(ICMS, "ICMSOutraUF")
        else:
            ICMS = None
    else:
        ICMS = None
    CST = safe_getattr(ICMS, "CST") if ICMS else ""
    if CST in TIPOS_CST:
        CST = TIPOS_CST[CST]
    vBC = safe_getattr(ICMS, "vBC") if ICMS else ""
    pICMS = safe_getattr(ICMS, "pICMS") if ICMS else ""
    vICMS = safe_getattr(ICMS, "vICMS") if ICMS else ""
    
    # Dados infCTeNorm
    infCTeNorm = safe_getattr(infCte, "infCTeNorm")
    infCarga = safe_getattr(infCTeNorm, "infCarga")
    proPred = safe_getattr(infCarga, "proPred")
    xOutCat = safe_getattr(infCarga, "xOutCat")
    vCarga = safe_getattr(infCarga, "vCarga")
    infQ = safe_getattr(infCarga, "infQ")
    infDoc = safe_getattr(infCTeNorm, "infDoc")
    infNFe = safe_getattr(infDoc, "infNFe")
    docAnt = safe_getattr(infCTeNorm, "docAnt")
    emiDocAnt = safe_getattr(docAnt, "emiDocAnt")
    idDocAnt = safe_getattr(emiDocAnt, "idDocAnt")
    idDocAntEle = safe_getattr(idDocAnt, "idDocAntEle")

    # Dados VPrest
    vPrest = safe_getattr(infCte, "vPrest")
    vTPrest = safe_getattr(vPrest, "vTPrest")
    vRec = safe_getattr(vPrest, "vRec")
    Comp = safe_getattr(vPrest, "Comp")

    #===============================================
    # INICIO LAYOUT - MONTAGEM DO BODY
    #===============================================
    # Definindo as dimensões da página
    largura, altura = A4
    topo = altura - 62 * mm  # margem superior
    margem = 6 * mm
    
    # Dimensões gerais do corpo
    altura_cabecalho = 156 * mm
    largura_total = largura - 2 * margem
    
    # Desenho do corpo total
    canvas_obj.rect(margem, topo - altura_cabecalho, largura_total, altura_cabecalho)
    
    # CTE - AUTORIZADO após o retângulo
    canvas_obj.setFillColorRGB(0.5, 0.5, 0.5)
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawCentredString(margem + largura_total / 2, topo - altura_cabecalho - 4 * mm, f"CT-E {status}")
    canvas_obj.setFillColorRGB(0, 0, 0)
    
    # [DEPRECIADO] 1ª linha - Dados do CTe
    # x_primeira_linha = margem
    # y_primeira_linha = topo
    # altura_primeira_linha = 8 * mm
    
    # labels = ["Tomador do serviço:", "Forma de pagamento:", "Protocolo de autorização de uso:", "INSC. SUFRAMA DO DESTINATÁRIO:"]
    # valores = ["Nome do Tomador", "Pagamento à vista", "123456789012345", "1234567890"]
    # primeira_largura_col = [ 40 * mm, 50 * mm, 60 * mm, 48 * mm]
    # x_primeira_largura_col = x_primeira_linha
    # for i, (label, valor) in enumerate(zip(labels, valores)):
    #     canvas_obj.rect(x_primeira_largura_col, y_primeira_linha - altura_primeira_linha, primeira_largura_col[i], altura_primeira_linha)
    #     canvas_obj.setFont("Helvetica", 6)
    #     canvas_obj.drawString(x_primeira_largura_col + 2 * mm, y_primeira_linha - 3 * mm, label)
    #     canvas_obj.setFont("Helvetica-Bold", 8)
    #     canvas_obj.drawString(x_primeira_largura_col + 2 * mm, y_primeira_linha - 6 * mm, valor)
    #     x_primeira_largura_col += primeira_largura_col[i]
        
    # 2ª linha - CFOP - NATUREZA DA PRESTAÇÃO
    x_segunda_linha = margem
    y_segunda_linha = topo
    altura_segunda_linha = 8 * mm
    
    canvas_obj.rect(x_segunda_linha, y_segunda_linha - altura_segunda_linha, largura_total, altura_segunda_linha)
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_segunda_linha + 2 * mm, y_segunda_linha - 3 * mm, "CFOP - NATUREZA DA PRESTAÇÃO:")
    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawString(x_segunda_linha + 2 * mm, y_segunda_linha - 6 * mm, f"{CFOP} - {natOp}")

    # 3ª linha - 1º bloco - ORIGEM DA PRESTAÇÃO

    x_terceira_linha = margem
    y_terceira_linha = y_segunda_linha - altura_segunda_linha
    altura_terceira_linha = 8 * mm
    
    canvas_obj.rect(x_terceira_linha, y_terceira_linha - altura_terceira_linha, largura_total / 2, altura_terceira_linha)
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_terceira_linha + 2 * mm, y_terceira_linha - 3 * mm, "ORIGEM DA PRESTAÇÃO:")
    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawString(x_terceira_linha + 2 * mm, y_terceira_linha - 6 * mm, f"{UFIni} - {xMunIni}")

    # 3ª linha - 2º bloco - DESTINO DA PRESTAÇÃO
    
    canvas_obj.rect(x_terceira_linha + largura_total / 2, y_terceira_linha - altura_terceira_linha, largura_total / 2, altura_terceira_linha)
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_terceira_linha + largura_total / 2 + 2 * mm, y_terceira_linha - 3 * mm, "DESTINO DA PRESTAÇÃO:")
    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawString(x_terceira_linha + largura_total / 2 + 2 * mm, y_terceira_linha - 6 * mm, f"{UFFim} - {xMunFim}")

    # 4ª linha - 1º bloco - Dados do remetente
    
    x_quarta_linha = margem
    y_quarta_linha = y_terceira_linha - altura_terceira_linha
    altura_quarta_linha = 20 * mm
    
    canvas_obj.rect(x_quarta_linha, y_quarta_linha - altura_quarta_linha, largura_total / 2, altura_quarta_linha)
    
    labels = ["REMETENTE:", "ENDEREÇO:", "COMPLEMENTO:", "BAIRRO:", "MUNICÍPIO:", "U.F:", "CNPJ/CPF:", "INSC. EST:", "PAÍS:", "TELEFONE:"]
    endereco = f"{xLgr_remetente}, {nro_remetente}" if xLgr_remetente and nro_remetente else ""
    values = [xNome_remetente, endereco, xCpl_remetente, xBairro_remetente, xMun_remetente, UF_remetente, CNPJ_remetente, IE_remetente, xPais_remetente, fone_remetente]

    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_quarta_linha + 2 * mm, y_quarta_linha - 3 * mm, labels[0])
    canvas_obj.drawString(x_quarta_linha + 2 * mm, y_quarta_linha - 6 * mm, labels[1])
    canvas_obj.drawString(x_quarta_linha + 2 * mm, y_quarta_linha - 9 * mm, labels[2])
    canvas_obj.drawString(x_quarta_linha + 2 * mm, y_quarta_linha - 12 * mm, labels[3])
    canvas_obj.drawString(x_quarta_linha + 2 * mm, y_quarta_linha - 15 * mm, labels[4])
    canvas_obj.drawString(x_quarta_linha + 2 * mm, y_quarta_linha - 18 * mm, labels[5])
    canvas_obj.drawString(x_quarta_linha + 40 * mm, y_quarta_linha - 9 * mm, labels[6])
    canvas_obj.drawString(x_quarta_linha + 40 * mm, y_quarta_linha - 12 * mm, labels[7])
    canvas_obj.drawString(x_quarta_linha + 40 * mm, y_quarta_linha - 15 * mm, labels[8])
    canvas_obj.drawString(x_quarta_linha + 40 * mm, y_quarta_linha - 18 * mm, labels[9])
    

    value_font_size = calc_font_size_dynamic(6, 60, len(values[0]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quarta_linha + 16 * mm, y_quarta_linha - 3 * mm, values[0])
    value_font_size = calc_font_size_dynamic(6, 30, len(values[1]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quarta_linha + 15 * mm, y_quarta_linha - 6 * mm, values[1])
    value_font_size = calc_font_size_dynamic(6, 12, len(values[2]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quarta_linha + 20 * mm, y_quarta_linha - 9 * mm, values[2])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[3]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quarta_linha + 12 * mm, y_quarta_linha - 12 * mm, values[3])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[4]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quarta_linha + 15 * mm, y_quarta_linha - 15 * mm, values[4])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[5]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quarta_linha + 7 * mm, y_quarta_linha - 18 * mm, values[5])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[6]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quarta_linha + 52 * mm, y_quarta_linha - 9 * mm, values[6])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[7]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quarta_linha + 52 * mm, y_quarta_linha - 12 * mm, values[7])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[8]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quarta_linha + 46 * mm, y_quarta_linha - 15 * mm, values[8])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[9]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quarta_linha + 53 * mm, y_quarta_linha - 18 * mm, values[9])
    
    # 4ª linha - 2º bloco - Dados do destinatário
    
    canvas_obj.rect(x_quarta_linha + largura_total / 2, y_quarta_linha - altura_quarta_linha, largura_total / 2, altura_quarta_linha)

    labels = ["DESTINATÁRIO:", "ENDEREÇO:", "COMPLEMENTO:", "BAIRRO:", "MUNICÍPIO:", "U.F:", "CNPJ/CPF:", "INSC. EST:", "PAÍS:", "TELEFONE:"]
    endereco = f"{xLgr_destinatario}, {nro_destinatario}" if xLgr_destinatario and nro_destinatario else ""
    values = [xNome_destinatario, endereco, xCpl_destinatario, xBairro_destinatario, xMun_destinatario, UF_destinatario, CNPJ_destinatario, IE_destinatario, xPais_destinatario, fone_destinatario]

    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 2 * mm, y_quarta_linha - 3 * mm, labels[0])
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 2 * mm, y_quarta_linha - 6 * mm, labels[1])
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 2 * mm, y_quarta_linha - 9 * mm, labels[2])
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 2 * mm, y_quarta_linha - 12 * mm, labels[3])
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 2 * mm, y_quarta_linha - 15 * mm, labels[4])
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 2 * mm, y_quarta_linha - 18 * mm, labels[5])
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 40 * mm, y_quarta_linha - 9 * mm, labels[6])
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 40 * mm, y_quarta_linha - 12 * mm, labels[7])
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 40 * mm, y_quarta_linha - 15 * mm, labels[8])
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 40 * mm, y_quarta_linha - 18 * mm, labels[9])
    
    
    value_font_size = calc_font_size_dynamic(6, 60, len(values[0]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 19 * mm, y_quarta_linha - 3 * mm, values[0])
    value_font_size = calc_font_size_dynamic(6, 30, len(values[1]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 15 * mm, y_quarta_linha - 6 * mm, values[1])
    value_font_size = calc_font_size_dynamic(6, 12, len(values[2]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 20 * mm, y_quarta_linha - 9 * mm, values[2])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[3]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 12 * mm, y_quarta_linha - 12 * mm, values[3])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[4]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 15 * mm, y_quarta_linha - 15 * mm, values[4])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[5]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 7 * mm, y_quarta_linha - 18 * mm, values[5])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[6]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 52 * mm, y_quarta_linha - 9 * mm, values[6])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[7]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 52 * mm, y_quarta_linha - 12 * mm, values[7])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[8]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 46 * mm, y_quarta_linha - 15 * mm, values[8])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[9]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quarta_linha + largura_total / 2) + 53 * mm, y_quarta_linha - 18 * mm, values[9])

    # 5ª linha - 1º bloco - Dados do EXPEDIDOR

    x_quinta_linha = margem
    y_quinta_linha = y_quarta_linha - altura_quarta_linha
    altura_quinta_linha = 20 * mm
    
    canvas_obj.rect(x_quinta_linha, y_quinta_linha - altura_quinta_linha, largura_total / 2, altura_quinta_linha)

    labels = ["EXPEDIDOR:", "ENDEREÇO:", "COMPLEMENTO:", "BAIRRO:", "MUNICÍPIO:", "U.F:", "CNPJ/CPF:", "INSC. EST:", "PAÍS:", "TELEFONE:"]
    endereco = f"{xLgr_expedidor}, {nro_expedidor}" if xLgr_expedidor and nro_expedidor else ""
    values = [xNome_expedidor, endereco, xCpl_expedidor, xBairro_expedidor, xMun_expedidor, UF_expedidor, CNPJ_expedidor, IE_expedidor, xPais_expedidor, fone_expedidor]

    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_quinta_linha + 2 * mm, y_quinta_linha - 3 * mm, labels[0])
    canvas_obj.drawString(x_quinta_linha + 2 * mm, y_quinta_linha - 6 * mm, labels[1])
    canvas_obj.drawString(x_quinta_linha + 2 * mm, y_quinta_linha - 9 * mm, labels[2])
    canvas_obj.drawString(x_quinta_linha + 2 * mm, y_quinta_linha - 12 * mm, labels[3])
    canvas_obj.drawString(x_quinta_linha + 2 * mm, y_quinta_linha - 15 * mm, labels[4])
    canvas_obj.drawString(x_quinta_linha + 2 * mm, y_quinta_linha - 18 * mm, labels[5])
    canvas_obj.drawString(x_quinta_linha + 40 * mm, y_quinta_linha - 9 * mm, labels[6])
    canvas_obj.drawString(x_quinta_linha + 40 * mm, y_quinta_linha - 12 * mm, labels[7])
    canvas_obj.drawString(x_quinta_linha + 40 * mm, y_quinta_linha - 15 * mm, labels[8])
    canvas_obj.drawString(x_quinta_linha + 40 * mm, y_quinta_linha - 18 * mm, labels[9])
    

    value_font_size = calc_font_size_dynamic(6, 60, len(values[0]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quinta_linha + 16 * mm, y_quinta_linha - 3 * mm, values[0])
    value_font_size = calc_font_size_dynamic(6, 30, len(values[1]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quinta_linha + 15 * mm, y_quinta_linha - 6 * mm, values[1])
    value_font_size = calc_font_size_dynamic(6, 12, len(values[2]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quinta_linha + 20 * mm, y_quinta_linha - 9 * mm, values[2])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[3]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quinta_linha + 12 * mm, y_quinta_linha - 12 * mm, values[3])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[4]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quinta_linha + 15 * mm, y_quinta_linha - 15 * mm, values[4])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[5]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quinta_linha + 7 * mm, y_quinta_linha - 18 * mm, values[5])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[6]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quinta_linha + 52 * mm, y_quinta_linha - 9 * mm, values[6])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[7]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quinta_linha + 52 * mm, y_quinta_linha - 12 * mm, values[7])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[8]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quinta_linha + 46 * mm, y_quinta_linha - 15 * mm, values[8])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[9]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString(x_quinta_linha + 53 * mm, y_quinta_linha - 18 * mm, values[9])

    # 5ª linha - 2º bloco - Dados do RECEBEDOR
    
    canvas_obj.rect(x_quarta_linha + largura_total / 2, y_quinta_linha - altura_quinta_linha, largura_total / 2, altura_quinta_linha)
    
    canvas_obj.setFont("Helvetica", 6)
    labels = ["RECEBEDOR:", "ENDEREÇO:", "COMPLEMENTO:", "BAIRRO:", "MUNICÍPIO:", "U.F:", "CNPJ/CPF:", "INSC. EST:", "PAÍS:", "TELEFONE:"]
    endereco = f"{xLgr_recebedor}, {nro_recebedor}" if xLgr_recebedor and nro_recebedor else ""
    values = [xNome_recebedor, endereco, xCpl_recebedor, xBairro_recebedor, xMun_recebedor, UF_recebedor, CNPJ_recebedor, IE_recebedor, xPais_recebedor, fone_recebedor]

    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 2 * mm, y_quinta_linha - 3 * mm, labels[0])
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 2 * mm, y_quinta_linha - 6 * mm, labels[1])
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 2 * mm, y_quinta_linha - 9 * mm, labels[2])
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 2 * mm, y_quinta_linha - 12 * mm, labels[3])
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 2 * mm, y_quinta_linha - 15 * mm, labels[4])
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 2 * mm, y_quinta_linha - 18 * mm, labels[5])
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 40 * mm, y_quinta_linha - 9 * mm, labels[6])
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 40 * mm, y_quinta_linha - 12 * mm, labels[7])
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 40 * mm, y_quinta_linha - 15 * mm, labels[8])
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 40 * mm, y_quinta_linha - 18 * mm, labels[9])
    
    value_font_size = calc_font_size_dynamic(6, 60, len(values[0]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 17 * mm, y_quinta_linha - 3 * mm, values[0])
    value_font_size = calc_font_size_dynamic(6, 30, len(values[1]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 16 * mm, y_quinta_linha - 6 * mm, values[1])
    value_font_size = calc_font_size_dynamic(6, 12, len(values[2]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 20 * mm, y_quinta_linha - 9 * mm, values[2])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[3]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 12 * mm, y_quinta_linha - 12 * mm, values[3])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[4]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 15 * mm, y_quinta_linha - 15 * mm, values[4])
    value_font_size = calc_font_size_dynamic(6, 18, len(values[5]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 7 * mm, y_quinta_linha - 18 * mm, values[5])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[6]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 52 * mm, y_quinta_linha - 9 * mm, values[6])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[7]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 52 * mm, y_quinta_linha - 12 * mm, values[7])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[8]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 46 * mm, y_quinta_linha - 15 * mm, values[8])
    value_font_size = calc_font_size_dynamic(6, 25, len(values[9]))
    canvas_obj.setFont("Helvetica-Bold", value_font_size)
    canvas_obj.drawString((x_quinta_linha + largura_total / 2) + 53 * mm, y_quinta_linha - 18 * mm, values[9])
    
    # 6ª linha - TOMADOR DO SERVIÇO:
    x_sexta_linha = margem
    y_sexta_linha = y_quinta_linha - altura_quinta_linha
    altura_sexta_linha = 12 * mm
    
    canvas_obj.rect(x_sexta_linha, y_sexta_linha - altura_sexta_linha, largura_total, altura_sexta_linha)
    labels = ["TOMADOR DO SERVIÇO:", "ENDEREÇO:", "CNPJ / CPF:", "MUNICÍPIO:", "INSC. EST:", "UF:", "PAÍS:", "TELEFONE:"]
    endereco = f"{xLgr_toma}, {nro_toma}" if xLgr_toma and nro_toma else ""
    values = [xNome_toma, endereco, CNPJ_toma, xMun_toma, IE_toma, UF_toma, xPais_toma, fone_toma]

    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_sexta_linha + 2 * mm, y_sexta_linha - 4 * mm, labels[0]) 
    canvas_obj.drawString(x_sexta_linha + 2 * mm, y_sexta_linha - 7 * mm, labels[1])
    canvas_obj.drawString(x_sexta_linha + 2 * mm, y_sexta_linha - 10 * mm, labels[2])
    canvas_obj.drawString(x_sexta_linha + 85 * mm, y_sexta_linha - 4 * mm, labels[3])
    canvas_obj.drawString(x_sexta_linha + 85 * mm, y_sexta_linha - 7 * mm, labels[4])
    canvas_obj.drawString(x_sexta_linha + 85 * mm, y_sexta_linha - 10 * mm, labels[5])
    canvas_obj.drawString(x_sexta_linha + 140 * mm, y_sexta_linha - 4 * mm, labels[6])
    canvas_obj.drawString(x_sexta_linha + 140 * mm, y_sexta_linha - 7 * mm, labels[7])
   
    label_font_size = calc_font_size_dynamic(6, 44, len(values[0]))
    canvas_obj.setFont("Helvetica-Bold", label_font_size)
    canvas_obj.drawString(x_sexta_linha + 28 * mm, y_sexta_linha - 4 * mm, values[0])
    label_font_size = calc_font_size_dynamic(6, 25, len(values[1]))
    canvas_obj.setFont("Helvetica-Bold", label_font_size)
    canvas_obj.drawString(x_sexta_linha + 15 * mm, y_sexta_linha - 7 * mm, values[1])
    label_font_size = calc_font_size_dynamic(6, 30, len(values[2]))
    canvas_obj.setFont("Helvetica-Bold", label_font_size)
    canvas_obj.drawString(x_sexta_linha + 15 * mm, y_sexta_linha - 10 * mm, values[2])
    label_font_size = calc_font_size_dynamic(6, 30, len(values[3]))
    canvas_obj.setFont("Helvetica-Bold", label_font_size)
    canvas_obj.drawString(x_sexta_linha + 97 * mm, y_sexta_linha - 4 * mm, values[3])
    label_font_size = calc_font_size_dynamic(6, 30, len(values[4]))
    canvas_obj.setFont("Helvetica-Bold", label_font_size)
    canvas_obj.drawString(x_sexta_linha + 96.5 * mm, y_sexta_linha - 7 * mm, values[4])
    label_font_size = calc_font_size_dynamic(6, 30, len(values[5]))
    canvas_obj.setFont("Helvetica-Bold", label_font_size)
    canvas_obj.drawString(x_sexta_linha + 89 * mm, y_sexta_linha - 10 * mm, values[5])
    label_font_size = calc_font_size_dynamic(6, 30, len(values[6]))
    canvas_obj.setFont("Helvetica-Bold", label_font_size)
    canvas_obj.drawString(x_sexta_linha + 146 * mm, y_sexta_linha - 4 * mm, values[6])
    label_font_size = calc_font_size_dynamic(6, 30, len(values[7]))
    canvas_obj.setFont("Helvetica-Bold", label_font_size)
    canvas_obj.drawString(x_sexta_linha + 152 * mm, y_sexta_linha - 7 * mm, values[7])

    # 7ª linha - 3x bloco - Dados do VOLUMES TRANSPORTADOS
    x_setima_linha = margem
    y_setima_linha = y_sexta_linha - altura_sexta_linha
    altura_setima_linha = 8 * mm
    
    labels = ["PRODUTO PREDOMINANTE:", "OUTRAS CARACTERÍSTICAS DA CARGA:", "VALOR TOTAL DA MERCADORIA:"]
    vCarga = locale.currency(float(vCarga), grouping=True) if vCarga else ""
    valores = [proPred, xOutCat, vCarga]
    x_setima_largura_col = largura_total / len(labels)
    
    for i, (label, valor) in enumerate(zip(labels, valores)):
        x = x_setima_linha + i * x_setima_largura_col
        canvas_obj.rect(x, y_setima_linha - altura_setima_linha, x_setima_largura_col, altura_setima_linha)
        canvas_obj.setFont("Helvetica", 6)
        canvas_obj.drawString(x + 2 * mm, y_setima_linha - 3 * mm, label)
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.drawString(x + 2 * mm, y_setima_linha - 6 * mm, valor)

    # 8ª linha - 4x bloco - Dados do VOLUMES TRANSPORTADOS
    x_oitava_linha = margem
    y_oitava_linha = y_setima_linha - altura_setima_linha
    altura_oitava_linha = 10 * mm

    quantidade = next((item.qCarga for item in infQ if not isinstance(item, str) and hasattr(item, "qCarga") and getattr(item, "tpMed", None) == "QUANTIDADE"), "")
    peso_bruto = next((item.qCarga for item in infQ if not isinstance(item, str) and hasattr(item, "qCarga") and getattr(item, "tpMed", None) == "PESO BRUTO"), "")
    qtd_vol = next((item.qCarga for item in infQ if not isinstance(item, str) and hasattr(item, "qCarga") and getattr(item, "tpMed", None) in ["QUANTIDADE VOL", "LITROS"]), "")
    cubagem = next((item.qCarga for item in infQ if not isinstance(item, str) and hasattr(item, "qCarga") and getattr(item, "tpMed", None) == "CUBAGEM"), "")

    labels = ["QUANTIDADE:", "PESO BRUTO (Kg):", "QTD. VOL. (Un):", "CUBAGEM (m³):"]
    valores = [quantidade, peso_bruto, qtd_vol, cubagem]
    x_oitava_largura_col = (largura_total - 110 * mm) / len(labels)
    
    for i, (label, valor) in enumerate(zip(labels, valores)):
        x = x_oitava_linha + i * x_oitava_largura_col
        canvas_obj.rect(x, y_oitava_linha - altura_oitava_linha, x_oitava_largura_col, altura_oitava_linha)
        canvas_obj.setFont("Helvetica", 6)
        canvas_obj.drawString(x + 2 * mm, y_oitava_linha - 3 * mm, label)
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.drawString(x + 2 * mm, y_oitava_linha - 8 * mm, valor)

    # 8ª linha - 5º bloco - Nome da Seguradora
    # TODO: Implementar a lógica para obter o nome da seguradora
    canvas_obj.rect(x_oitava_linha + 88 * mm, y_oitava_linha - altura_oitava_linha / 2.2, largura_total - 88 * mm, altura_oitava_linha / 2.2)
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_oitava_linha + 88 * mm + 2 * mm, y_oitava_linha - 3 * mm, "NOME DA SEGURADORA:")
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawString(x_oitava_linha + 115 * mm + 2 * mm, y_oitava_linha - 3 * mm, "")
    
    # 8ª linha - 3x bloco - Dados do VOLUMES TRANSPORTADOS
    labels = ["RESPONSÁVEL:", "NÚMERO DA APÓLICE", "NÚMERO DA AVERBAÇÃO:"]
    # TODO: Implementar a lógica para obter os valores correspondentes
    valores = ["", "", ""]
    x_oitava_largura_col = (largura_total - 88 * mm) / len(labels)
    
    for i, (label, valor) in enumerate(zip(labels, valores)):
        x = (x_oitava_linha + i * x_oitava_largura_col) + 88 * mm
        canvas_obj.rect(x, y_oitava_linha - altura_oitava_linha, x_oitava_largura_col, altura_oitava_linha - (altura_oitava_linha / 2.2))
        canvas_obj.setFont("Helvetica", 6)
        canvas_obj.drawString(x + 2 * mm, y_oitava_linha - 7 * mm, label)
        canvas_obj.setFont("Helvetica-Bold", 6)
        canvas_obj.drawString(x + 2 * mm, y_oitava_linha - 9 * mm, valor)
        
    # 9ª linha - 1º bloco - Titulo COMPONENTES DO VALOR DA PRESTAÇÃO DE SERVIÇO
    x_nona_linha = margem
    y_nona_linha = y_oitava_linha - altura_oitava_linha
    y_nona_linha_titulo = y_nona_linha - 4 * mm
    altura_nona_linha = 14 * mm
    
    canvas_obj.rect(x_nona_linha, y_nona_linha_titulo, largura_total, 4 * mm)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawCentredString(x_nona_linha + largura_total / 2, y_nona_linha - 3 * mm, "COMPONENTES DO VALOR DA PRESTAÇÃO DE SERVIÇO:")
    
    # 9ª linha - 2º bloco - Dados do COMPONENTES DO VALOR DA PRESTAÇÃO DE SERVIÇO

    labels = [["NOME:", "VALOR:"], ["NOME:", "VALOR:"], ["NOME:", "VALOR:"]]

    x_nona_largura_col = (largura_total - 50 * mm) / len(labels)
    for i, (label) in enumerate(labels):
        x = x_nona_linha + i * x_nona_largura_col
        canvas_obj.rect(x, y_nona_linha_titulo - altura_nona_linha, x_nona_largura_col, altura_nona_linha)
        canvas_obj.setFont("Helvetica-Bold", 5)
        canvas_obj.drawCentredString(x + x_nona_largura_col / 3, y_nona_linha_titulo - 3 * mm, label[0])
        canvas_obj.drawCentredString(x + x_nona_largura_col / 1.5, y_nona_linha_titulo - 3 * mm, label[1])

    # O espaçamento em X do bloco a baixo é montado a partir das dimensoes estipuladas a baixo
    # deve ser refatorado posteriormente para ser mais dinamico e resiliente
    # se forem informados muitos componentes irá sobrepor o grupo
    dimensoes_x = [16, 66, 116]
    y_conteudo_nona_linha = y_nona_linha_titulo - 5.5 * mm
    canvas_obj.setFont("Helvetica-Bold", 5)
    for i, comp in enumerate(Comp):
        if isinstance(comp, str) or not hasattr(comp, "xNome") or not hasattr(comp, "vComp"):
            continue
        index = i % 3
        x_conteudo_nona_linha = x_nona_linha + dimensoes_x[index] * mm
        nome, valor = comp.xNome, comp.vComp
        canvas_obj.drawCentredString(x_conteudo_nona_linha, y_conteudo_nona_linha, f"{nome}:")
        canvas_obj.drawCentredString(x_conteudo_nona_linha + 17 * mm, y_conteudo_nona_linha, valor)
        if(index == 2):
            y_conteudo_nona_linha -= 2 * mm

    # 9ª linha - 2x bloco - Dados do VALOR TOTAL DO SERVIÇO e VALOR TOTAL A RECEBER
    canvas_obj.rect(x_nona_linha + 3 * x_nona_largura_col, y_nona_linha_titulo - altura_nona_linha, (largura_total / 4) + 0.5 * mm, (altura_nona_linha / 2))

    labels = ["VALOR TOTAL DO SERVIÇO:", "VALOR TOTAL A RECEBER:"]
    vTPrest = locale.currency(float(vTPrest), grouping=True) if vTPrest else ""
    vRec = locale.currency(float(vRec), grouping=True) if vRec else ""
    values = [vTPrest, vRec]
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_nona_linha + 3 * x_nona_largura_col + 1 * mm, y_nona_linha_titulo - 3 * mm, labels[0])
    canvas_obj.drawString(x_nona_linha + 3 * x_nona_largura_col + 1 * mm, y_nona_linha_titulo - 10 * mm, labels[1])

    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawString(x_nona_linha + 3 * x_nona_largura_col + 16 * mm, y_nona_linha_titulo - 6 * mm, str(values[0]) if values[0] is not None else "")
    canvas_obj.drawString(x_nona_linha + 3 * x_nona_largura_col + 16 * mm, y_nona_linha_titulo - 13 * mm, str(values[1]) if values[1] is not None else "")
    
    # 10ª linha - 1º bloco - Titulo do INFORMAÇÕES RELATIVAS AO IMPOSTO
    canvas_obj.setFillColorRGB(0, 0, 0)
    x_decima_linha = margem
    y_decima_linha = y_nona_linha - (altura_nona_linha + 4 * mm)
    y_decima_linha_titulo = y_decima_linha - 4 * mm
    altura_decima_linha = 8 * mm

    canvas_obj.rect(x_decima_linha, y_decima_linha_titulo, largura_total, 4 * mm)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawCentredString(x_decima_linha + largura_total / 2, y_decima_linha - 3 * mm, "INFORMAÇÕES RELATIVAS AO IMPOSTO:")
    
    # 10ª linha - 2º bloco - Dados do INFORMAÇÕES RELATIVAS AO IMPOSTO
    labels = ["SITUAÇÃO TRIBUTÁRIA:", "BASE DE CÁLCULO:", "ALÍQ ICMS:", "VALOR ICMS:", "% RED.BC.CALC.:", "ICMS ST:"]
    values = [CST, vBC, pICMS, vICMS, "", ""]
    x_decima_largura_col = largura_total / len(labels)
    
    for i, (label, value) in enumerate(zip(labels, values)):
        x = x_decima_linha + i * x_decima_largura_col
        canvas_obj.rect(x, y_decima_linha_titulo - altura_decima_linha, x_decima_largura_col, altura_decima_linha)
        label_font_size = calc_font_size_dynamic(6, 25, len(label))
        canvas_obj.setFont("Helvetica", label_font_size)
        canvas_obj.drawString(x + 2 * mm, y_decima_linha_titulo - 3 * mm, label)
        if(not value):
            continue
        value_font_size = calc_font_size_dynamic(8, 20, len(value))
        canvas_obj.setFont("Helvetica-Bold", value_font_size)
        canvas_obj.drawString(x + 2 * mm, y_decima_linha_titulo - 6 * mm, value)
        
    # 11ª linha - 1º bloco - Dados do DOCUMENTOS ORIGINÁRIOS / ANTERIORES:
    documentos_originarios = [
        DocumentoOriginarioAnterior(tipo=f"{inf.chave[20:22]} - Dc.O.", chave=inf.chave)
        for inf in infNFe
        if not isinstance(inf, str) and hasattr(inf, "chave")
    ]
    documentos_anteriores = [
        DocumentoOriginarioAnterior(tipo=f"{doc.chCTe[20:22]} - Dc.A.", chave=doc.chCTe)
        for doc in idDocAntEle
        if not isinstance(doc, str) and hasattr(doc, "chCTe")
    ]
    componentes_originarios_anteriores({
        "x_inicial": margem,
        "y_inicial": y_decima_linha - (altura_decima_linha + 4 * mm),
        "largura_total": largura_total,
        "limite_por_quadrante": 8,
        "documentos": documentos_originarios + documentos_anteriores,
        "payload": data,
        "canvas_obj": canvas_obj,
    })