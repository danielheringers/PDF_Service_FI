from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.modules.dfes.dacte.schemas import DactePayload
from app.utils.utils import safe_getattr

def calcular_fonte_e_limite(
    tamanho_fonte_padrao: float,
    limite_padrao: int,
    total_caracteres: int,
    maximo_caracteres: int
) -> tuple[float, int]:
    """
    Calcula dinamicamente o tamanho da fonte e o número de caracteres por linha,
    mantendo a largura do container proporcional.
    """
    if total_caracteres <= maximo_caracteres:
        return tamanho_fonte_padrao, limite_padrao

    constante_largura = tamanho_fonte_padrao * limite_padrao

    tamanho_fonte = tamanho_fonte_padrao * (maximo_caracteres / total_caracteres)

    novo_limite = round(constante_largura / tamanho_fonte)

    return tamanho_fonte, novo_limite

def formatar_x_obs(text: str,limit: int) -> list[str]:
    """
    Formata o texto de x_obs em linhas de tamanho limitado.
    """
    return [text[i:i+limit] for i in range(0, len(text), limit)]

def add_footer(canvas_obj: canvas.Canvas, data: DactePayload):
    #===============================================
    # INICIO CAPTURA DE DADOS - FOOTER
    #===============================================
    cteProc = safe_getattr(data.data, "cteProc")
    CTe = safe_getattr(cteProc, "CTe")
    infCte = safe_getattr(CTe, "infCte")

    # Dados de complemento
    compl = safe_getattr(infCte, "compl")
    x_obs = safe_getattr(compl, "xObs")
    entrega = safe_getattr(compl, "Entrega")
    com_data = safe_getattr(entrega, "comData")
    d_prog = safe_getattr(com_data, "dProg")

    # Dados identificadores do CTe
    ide = safe_getattr(infCte, "ide")
    serie = safe_getattr(ide, "serie")
    n_cte = safe_getattr(ide, "nCT")

    # Dados Modal
    inf_cte_norm = safe_getattr(infCte, "infCTeNorm")
    inf_modal = safe_getattr(inf_cte_norm, "infModal")
    rntrc = ""
    if isinstance(inf_modal, dict) and "rodo" in inf_modal:
        rntrc = inf_modal["rodo"].get("RNTRC", "")

    # Dados imposto
    imp = safe_getattr(infCte, "imp")
    infAdFisco = safe_getattr(imp, "infAdFisco")
    
    #===============================================
    # INICIO LAYOUT - MONTAGEM DO FOOTER
    #===============================================
    # Inicio montagem do rodapé
    largura, altura = A4
    topo = altura - (altura - 4 * mm - 70 * mm)  # margem superior
    margem = 6 * mm

    # Dimensões gerais do rodapé
    largura_total = largura - 2 * margem
    altura_rodape = 70 * mm
    
    # Desenho do retângulo do rodapé
    canvas_obj.setFillColorRGB(0, 0, 0)
    canvas_obj.rect(margem, topo -  altura_rodape, largura_total, altura_rodape)

    # 1ª linha - 1º bloco - Titulo OBSERVAÇÃO
    x_primeira_linha = margem
    y_primeira_linha = topo
    y_primeira_linha_titulo = y_primeira_linha - 4 * mm
    altura_primeira_linha = 18 * mm
    
    canvas_obj.rect(x_primeira_linha, y_primeira_linha_titulo, largura_total, 4 * mm)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawCentredString(x_primeira_linha + largura_total / 2, y_primeira_linha - 3 * mm, "OBSERVAÇÃO:")
    
    # 1ª linha - 2º bloco - Bloco de OBSERVAÇÃO
    canvas_obj.rect(x_primeira_linha, y_primeira_linha - altura_primeira_linha, largura_total, altura_primeira_linha)
    
    x_obs = f"{x_obs} - {infAdFisco}" if infAdFisco else x_obs
    
    tamanho_fonte, limite = calcular_fonte_e_limite(
        6, # tamanho da fonte padrão
        150, # limite de caracteres padrão para o componente
        len(x_obs), # total de caracteres
        600 # limite máximo de caracteres para o componente
    )

    x_obs_list = formatar_x_obs(x_obs, limite)
    canvas_obj.setFont("Helvetica", tamanho_fonte)
    y_obs = y_primeira_linha - 7 * mm
    for obs_line in x_obs_list:
        canvas_obj.drawString(x_primeira_linha + 2 * mm, y_obs, obs_line)
        y_obs -= 3 * mm
    
    #2ª linha - 1º bloco - Titulo INFORMAÇÕES ESPECÍFICAS DO MODAL RODOVIÁRIO - CARGA FRACIONADA
    x_segunda_linha = margem
    y_segunda_linha = y_primeira_linha - altura_primeira_linha
    y_segunda_linha_titulo = y_segunda_linha - 4 * mm
    altura_segunda_linha = 8 * mm
    
    canvas_obj.rect(x_primeira_linha, y_segunda_linha_titulo, largura_total, 4 * mm)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawCentredString(x_primeira_linha + largura_total / 2, y_segunda_linha - 3 * mm, "INFORMAÇÕES ESPECÍFICAS DO MODAL RODOVIÁRIO - CARGA FRACIONADA")
    
    # 2ª linha - 2º bloco - Bloco de INFORMAÇÕES ESPECÍFICAS DO MODAL RODOVIÁRIO - CARGA FRACIONADA
    labels = ["RNTRC DA EMPRESA:", "Conta Frete / CIOT:", "LOTAÇÃO:", "DATA PREVISTA DE ENTREGA:", "ESSE CONHECIMENTO ATENDE A LEGISLAÇÃO DE TRANSPORTE"]
    valores = [rntrc, " ", " ", d_prog, " "]
    largura_col = [ 
        30 * mm,  # RNTRC DA EMPRESA
        25 * mm,  # Conta Frete / CIOT
        25 * mm,  # LOTAÇÃO
        35 * mm,  # DATA PREVISTA DE ENTREGA
        largura_total - (30 + 25 + 25 + 35) * mm,  # ESSE CONHECIMENTO ATENDE A LEGISLAÇÃO DE TRANSPORTE RODOVIÁRIO EM VIGOR
    ]
    x_primeira_largura_col = x_segunda_linha
    for i, (label, valor) in enumerate(zip(labels, valores)):
        canvas_obj.rect(x_primeira_largura_col, y_segunda_linha_titulo - altura_segunda_linha, largura_col[i], altura_segunda_linha)
        if i == 4:
            canvas_obj.setFont("Helvetica-Bold", 6)
            canvas_obj.drawCentredString(x_primeira_largura_col + largura_col[i] / 2, y_segunda_linha_titulo - 3 * mm, label)
            canvas_obj.drawCentredString(x_primeira_largura_col + largura_col[i] / 2, y_segunda_linha_titulo - 6 * mm, valor)
        else:
            canvas_obj.setFont("Helvetica", 6)
            canvas_obj.drawString(x_primeira_largura_col + 2 * mm, y_segunda_linha_titulo - 3 * mm, label)
            canvas_obj.setFont("Helvetica-Bold", 8)
            canvas_obj.drawString(x_primeira_largura_col + 2 * mm, y_segunda_linha_titulo - 6 * mm, valor)
        x_primeira_largura_col += largura_col[i]
        
    # 3ª linha - 1º bloco - Titulo USO EXCLUSIVO DO EMISSOR DO CT-E:
    x_terceira_linha = margem
    y_terceira_linha = y_segunda_linha - (altura_segunda_linha + 4 * mm)
    y_terceira_linha_titulo = y_terceira_linha - 4 * mm
    altura_terceira_linha = 8 * mm
    
    canvas_obj.rect(x_terceira_linha, y_terceira_linha_titulo, largura_total, 4 * mm)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawCentredString(x_terceira_linha + largura_total / 2, y_terceira_linha - 3 * mm, "USO EXCLUSIVO DO EMISSOR DO CT-E:")
    
    # 3ª linha - 2º bloco - Bloco de USO EXCLUSIVO DO EMISSOR DO CT-E
    labels = ["CALCULADO ATÉ:", "", "Nº TABELA:", "EMITIDO POR:"]
    valores = [" ", " ", " ", " "]
    largura_col = [ 
        30 * mm,  # CALCULADO ATÉ
        70 * mm,  # ""
        25 * mm,  # Nº TABELA
        largura_total - (30 + 70 + 25) * mm,  # EMITIDO POR
    ]
    x_primeira_largura_col = x_terceira_linha
    for i, (label, valor) in enumerate(zip(labels, valores)):
        canvas_obj.rect(x_primeira_largura_col, y_terceira_linha_titulo - altura_terceira_linha, largura_col[i], altura_terceira_linha)
        if i == 4:
            canvas_obj.setFont("Helvetica-Bold", 6)
            canvas_obj.drawCentredString(x_primeira_largura_col + largura_col[i] / 2, y_terceira_linha_titulo - 3 * mm, label)
            canvas_obj.drawCentredString(x_primeira_largura_col + largura_col[i] / 2, y_terceira_linha_titulo - 6 * mm, valor)
        else:
            canvas_obj.setFont("Helvetica", 6)
            canvas_obj.drawString(x_primeira_largura_col + 2 * mm, y_terceira_linha_titulo - 3 * mm, label)
            canvas_obj.setFont("Helvetica-Bold", 8)
            canvas_obj.drawString(x_primeira_largura_col + 2 * mm, y_terceira_linha_titulo - 6 * mm, valor)
        x_primeira_largura_col += largura_col[i]
    
    # 4ª linha - 1º bloco e 2º bloco - 30% da largura - Em branco
    x_quarta_linha = margem
    y_quarta_linha = y_terceira_linha - (altura_terceira_linha + 4 * mm)
    altura_quarta_linha = 10 * mm
    
    labels = ["", ""]
    valores = ["", ""]
    largura_col = [ 
        30 * mm,  # ""
        30 * mm,  # ""
    ]
    x_primeira_largura_col = x_quarta_linha
    for i, (label, valor) in enumerate(zip(labels, valores)):
        canvas_obj.rect(x_primeira_largura_col, y_quarta_linha - altura_quarta_linha, largura_col[i], altura_quarta_linha)
        canvas_obj.setFont("Helvetica", 6)
        canvas_obj.drawString(x_primeira_largura_col + 2 * mm, y_quarta_linha - 3 * mm, label)
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.drawString(x_primeira_largura_col + 2 * mm, y_quarta_linha - 6 * mm, valor)
        x_primeira_largura_col += largura_col[i]
    
    # 4ª linha - 3º bloco - Horizontal - 70% da largura - 35% da altura
    x_quarta_linha_horizontal = margem + 60 * mm
    y_quarta_linha_horizontal = y_quarta_linha
    altura_quarta_linha_horizontal = 3 * mm
    largura_quarta_linha_horizontal = largura_total - 60 * mm
    
    canvas_obj.rect(x_quarta_linha_horizontal, y_quarta_linha_horizontal - altura_quarta_linha_horizontal, largura_quarta_linha_horizontal, altura_quarta_linha_horizontal)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawString(x_quarta_linha_horizontal + 2 * mm, y_quarta_linha_horizontal - 2.25 * mm, "MOTORISTA:")
    canvas_obj.drawString(x_quarta_linha_horizontal + 80 * mm, y_quarta_linha_horizontal - 2.25 * mm, "CPF:")
    
    # 4ª linha - 4º bloco - Vertical - 70% da largura - 65% da altura
    x_quarta_linha_vertical = margem + 60 * mm
    y_quarta_linha_vertical = y_quarta_linha - altura_quarta_linha_horizontal
    altura_quarta_linha_vertical = altura_quarta_linha - altura_quarta_linha_horizontal
    largura_quarta_linha_vertical = largura_total - 60 * mm
    
    labels = [["D.I. / D.T.A. / G.E:", "Avião / Navio:", "Lote:", "Lotação:"], ["CONTAINER:", "MARCA:", "Nº:"]]
    largura_col = largura_quarta_linha_vertical / len(labels)
    x_primeira_largura_col = x_quarta_linha_vertical

    for i, (label) in enumerate(labels):
        canvas_obj.rect(x_primeira_largura_col, y_quarta_linha_vertical - altura_quarta_linha_vertical, largura_col, altura_quarta_linha_vertical)
        canvas_obj.setFont("Helvetica-Bold", 6)
        for j, (label) in enumerate(label):
            if j <= 1:
                canvas_obj.drawString(x_primeira_largura_col + 2 * mm, y_quarta_linha_vertical - 3 * mm - j * 3 * mm, label)
            if j == 2:
                canvas_obj.drawString(x_primeira_largura_col + 37 * mm, y_quarta_linha_vertical - 3 * mm, label)
            if j == 3:
                canvas_obj.drawString(x_primeira_largura_col + 37 * mm, y_quarta_linha_vertical - 6 * mm, label)
        x_primeira_largura_col += largura_col
    
    # 5ª linha - 1º bloco - Titulo DECLARAÇÃO
    x_quinta_linha = margem
    y_quinta_linha = y_quarta_linha - altura_quarta_linha
    y_quinta_linha_titulo = y_quinta_linha - 4 * mm
    altura_quinta_linha = 14 * mm

    canvas_obj.rect(x_quinta_linha, y_quinta_linha_titulo, largura_total, 4 * mm)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawCentredString(x_quinta_linha + largura_total / 2, y_quinta_linha - 3 * mm, "DECLARO QUE RECEBI OS VOLUMES DESTE CONHECIMENTO EM PERFEITO ESTADO PELO QUE DOU POR CUMPRIDO O PRESENTE CONTRATO DE TRANSPORTE")
    
    # 5ª linha - 1º bloco - 2 blocos horizontais - 30% da largura - 50% da altura
    labels = ["NOME LEGÍVEL:", "RG:"]
    canvas_obj.rect(x_quinta_linha, y_quinta_linha_titulo - (altura_quinta_linha / 2), largura_total / 5, altura_quinta_linha / 2)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawString(x_quinta_linha + 2 * mm, y_quinta_linha_titulo - 3 * mm, labels[0])
    canvas_obj.rect(x_quinta_linha, y_quinta_linha_titulo - (altura_quinta_linha / 2) - 7 * mm, largura_total / 5, altura_quinta_linha / 2)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawString(x_quinta_linha + 2 * mm, y_quinta_linha_titulo - 10 * mm, labels[1])
    
    # 5ª linha - 2º bloco - 1 blocos horizontal - SERIE e NÚMERO
    x_quinta_linha_vertical = margem + (largura_total / 5)
    y_quinta_linha_vertical = y_quinta_linha_titulo
    altura_quinta_linha_vertical = altura_quarta_linha_horizontal
    largura_quinta_linha_vertical = largura_total / 2
    
    canvas_obj.rect(x_quinta_linha_vertical, y_quinta_linha_vertical - altura_quinta_linha_vertical, largura_quinta_linha_vertical, altura_quarta_linha_horizontal)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawString(x_quinta_linha_vertical + 2 * mm, y_quinta_linha_vertical - 2.25 * mm, "SÉRIE:")
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_quinta_linha_vertical + 11 * mm, y_quinta_linha_vertical - 2.25 * mm, serie)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawString(x_quinta_linha_vertical + 60 * mm, y_quinta_linha_vertical - 2.25 * mm, "Nº:")
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(x_quinta_linha_vertical + 65 * mm, y_quinta_linha_vertical - 2.25 * mm, n_cte)
    
    # 5ª linha - 3º bloco - 1 blocos horizontal - ESPAÇO PARA O CARIMBO DO TRANSPORTADOR
    canvas_obj.rect(x_quinta_linha_vertical, y_quinta_linha_vertical - altura_quinta_linha, largura_quinta_linha_vertical, altura_quinta_linha - altura_quarta_linha_horizontal)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawCentredString(x_quinta_linha_vertical + largura_quinta_linha_vertical / 2, altura_quarta_linha_horizontal + 1.5 * mm, "ASSINATURA / CARIMBO")
    
    # 5ª linha - 4º bloco - 1 blocos horizontal - DATA / HORA - CHEGADA E SAÍDA
    canvas_obj.rect(x_quinta_linha_vertical + largura_quinta_linha_vertical, y_quinta_linha_titulo - (altura_quinta_linha), 59.5 * mm, altura_quinta_linha)
    canvas_obj.setFont("Helvetica-Bold", 6)
    canvas_obj.drawCentredString(x_quinta_linha_vertical + largura_quinta_linha_vertical + 30 * mm, y_quinta_linha_titulo - 3 * mm, "CHEGADA - DATA / HORA")
    canvas_obj.drawString(x_quinta_linha_vertical + largura_quinta_linha_vertical + 20 * mm, y_quinta_linha_titulo - 5.6 * mm, "/")
    canvas_obj.drawString(x_quinta_linha_vertical + largura_quinta_linha_vertical + 24 * mm, y_quinta_linha_titulo - 5.6 * mm, "/")
    canvas_obj.drawString(x_quinta_linha_vertical + largura_quinta_linha_vertical + 37 * mm, y_quinta_linha_titulo - 5.6 * mm, ":")
    canvas_obj.drawCentredString(x_quinta_linha_vertical + largura_quinta_linha_vertical + 30 * mm, y_quinta_linha_titulo - 6 * mm, "____________    ____________")
    canvas_obj.drawCentredString(x_quinta_linha_vertical + largura_quinta_linha_vertical + 30 * mm, y_quinta_linha_titulo - 9 * mm, "SAÍDA - DATA / HORA")
    canvas_obj.drawString(x_quinta_linha_vertical + largura_quinta_linha_vertical + 20 * mm, y_quinta_linha_titulo - 11.6 * mm, "/")
    canvas_obj.drawString(x_quinta_linha_vertical + largura_quinta_linha_vertical + 24 * mm, y_quinta_linha_titulo - 11.6 * mm, "/")
    canvas_obj.drawString(x_quinta_linha_vertical + largura_quinta_linha_vertical + 37 * mm, y_quinta_linha_titulo - 11.6 * mm, ":")
    canvas_obj.drawCentredString(x_quinta_linha_vertical + largura_quinta_linha_vertical + 30 * mm, y_quinta_linha_titulo - 12 * mm, "____________    ____________")