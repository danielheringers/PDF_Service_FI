from typing import List, TypedDict

from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from app.modules.dfes.dacte.schemas import DactePayload
from app.modules.dfes.dacte.template.header import add_header

class DocumentoOriginarioAnterior(TypedDict):
    tipo: str
    chave: str


class ComponentesOriginariosAnteriores(TypedDict):
    x_inicial: float
    y_inicial: float
    largura_total: float
    limite_por_quadrante: int
    documentos: List[DocumentoOriginarioAnterior]
    payload: DactePayload
    canvas_obj: canvas.Canvas

def preencher_quadrante(data_quad, x, y, canvas_obj: canvas.Canvas):
    for i, documento in enumerate(data_quad):
        # Dados
        cnpj_cpf = documento["chave"][6:20]
        inicio_chave = documento["chave"][0:25]
        serie = documento["chave"][22:25]
        numero = documento["chave"][25:34]
        final_chave = documento["chave"][34:]

        y_ref = y - ((i + 1) * 4 * mm)

        # Coluna Tipo
        canvas_obj.setFont("Helvetica", 6)
        canvas_obj.drawString(x, y_ref, documento["tipo"])
        x_gap_colunas = x + 12 * mm 

        # Coluna CNPJ/CPF
        canvas_obj.drawString(x_gap_colunas, y_ref, cnpj_cpf)
        x_gap_colunas = x_gap_colunas + 30 * mm

        # Coluna série/número
        canvas_obj.setFont("Helvetica", 5)
        canvas_obj.drawString(x_gap_colunas, y_ref, inicio_chave)
        canvas_obj.setFont("Helvetica-Bold", 6)
        x_gap_colunas = x_gap_colunas + 26 * mm
        canvas_obj.drawString(x_gap_colunas, y_ref, serie)
        x_gap_colunas = x_gap_colunas + 4 * mm
        canvas_obj.drawString(x_gap_colunas, y_ref, numero)
        canvas_obj.setFont("Helvetica", 5)
        x_gap_colunas = x_gap_colunas + 12 * mm
        canvas_obj.drawString(x_gap_colunas, y_ref, final_chave)

def componentes_originarios_anteriores(data: ComponentesOriginariosAnteriores):
    x_inicial = data["x_inicial"]
    y_inicial = data["y_inicial"]
    largura_total = data["largura_total"]
    limite_por_quadrante = data["limite_por_quadrante"]
    documentos = data["documentos"]
    payload = data["payload"]
    canvas_obj = data["canvas_obj"]

    canvas_obj.setFont("Helvetica-Bold", 6)

    metade_largura = x_inicial + largura_total / 2
    y_titulo = y_inicial - 3 * mm
    
    # Titulo e linha abaixo do titulo
    canvas_obj.drawCentredString(metade_largura, y_titulo, "DOCUMENTOS ORIGINÁRIOS / ANTERIORES:")
    y_linha_titulo = y_titulo - 1 * mm
    tamanho_titulo = y_inicial-y_linha_titulo
    canvas_obj.rect(x_inicial, y_linha_titulo, largura_total, tamanho_titulo)

    # Retangulo para preenchimento dos documentos originarios
    altura_por_documento = 4.5
    limite_por_quadrante = min(limite_por_quadrante, len(documentos)) if limite_por_quadrante == 50 else limite_por_quadrante
    altura_conteudo = limite_por_quadrante * altura_por_documento * mm
    y_conteudo = y_linha_titulo - altura_conteudo
    canvas_obj.rect(x_inicial, y_conteudo, largura_total, altura_conteudo)

    ## Divisão ao meio
    canvas_obj.rect(x_inicial, y_conteudo, largura_total / 2, altura_conteudo)

    ## Colunas
    y_colunas = y_linha_titulo - 3 * mm
    x_coluna = x_inicial + 2 * mm
    canvas_obj.drawString(x_coluna, y_colunas, "Tipo:")
    x_coluna = x_coluna + 18 * mm
    canvas_obj.drawString(x_coluna, y_colunas, "CNPJ/CPF Emitente:")
    x_coluna = x_coluna + 38 * mm
    canvas_obj.drawString(x_coluna, y_colunas, "Série / Nro. Documento:")

    x_coluna = metade_largura + x_inicial - 4 * mm  
    canvas_obj.drawString(x_coluna, y_colunas, "Tipo:")
    x_coluna = x_coluna + 18 * mm
    canvas_obj.drawString(x_coluna, y_colunas, "CNPJ/CPF Emitente:")
    x_coluna = x_coluna + 38 * mm
    canvas_obj.drawString(x_coluna, y_colunas, "Série / Nro. Documento:")

    ## Preenchendo os dados
    if(len(documentos)==0):
        return
    
    limite_maximo = limite_por_quadrante * 2
    data_primeiro_quadrante = documentos[:limite_por_quadrante]
    data_segundo_quadrante = documentos[limite_por_quadrante:limite_maximo]

    preencher_quadrante(data_primeiro_quadrante, x_inicial + 2 * mm, y_colunas, canvas_obj)
    preencher_quadrante(data_segundo_quadrante, metade_largura + x_inicial - 4 * mm, y_colunas, canvas_obj)

    data_restante = documentos[limite_maximo:]
    if len(data_restante) > 0:
        # Adiciona uma nova página
        canvas_obj.showPage()
        # Adiciona o cabeçalho novamente
        add_header(canvas_obj, payload)
        
        _, altura = A4
        topo = altura - 62 * mm  
        margem = 6 * mm
        limite_por_quadrante = 50
        componentes_originarios_anteriores({
            "x_inicial": margem,
            "y_inicial": topo,
            "largura_total": largura_total,
            "limite_por_quadrante": 50,
            "documentos": data_restante,
            "payload": payload,
            "canvas_obj": canvas_obj
        })