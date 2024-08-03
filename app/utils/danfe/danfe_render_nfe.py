import requests
from datetime import datetime
import locale
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from app.models.danfe.models import Danfe
from app.utils.general_pdf_utils import (
    formatar_moeda,
    draw_wrapped_text,
    formatar_celular,
    formatar_chave_acesso,
    get_emissao_details,
    formatar_cnpj_cpf
)



locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def render_first_page(canvas_draw, data: Danfe, data_formatada, serie_formatada, numero_nota_formatado, width, height, margin):
    # Formatações
    modFrete_descricao = {
        "0": "0 - Por conta do Emitente",
        "1": "1 - Por conta do destinatário",
        "2": "2 - Por conta de terceiros",
        "9": "9 - Sem frete (v2.0)"
    }
    x_position = margin + 165 * mm
    y_position = 241 * mm
    dt_emissao = datetime.fromisoformat(data.identificacao.dataHoraEmissao)
    dt_entrada_saida = datetime.fromisoformat(data.identificacao.dataHoraSaidaOuEntrada)
    valor = float(data.dadosCobranca)
    valor_formatado_canhoto = locale.currency(valor, grouping=True)
    serie_formatada = data.identificacao.serie.zfill(3)
    numero_nota = data.identificacao.numeroDocFiscal.zfill(9)
    numero_nota_formatado = '.'.join([numero_nota[i:i+3] for i in range(0, 9, 3)])
    chave_acesso_formatada = formatar_chave_acesso(data.key)
    cep_formatado = data.emitente.endereco.cep[:5] + '-' + data.emitente.endereco.cep[5:]
    dest_municipio = data.destinatario.endereco.codigoMunicipio
    nome_municipio_dest = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{dest_municipio}').json()
    emit_municipio = data.emitente.endereco.codigoMunicipio
    nome_municipio_emit = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{emit_municipio}').json()
    cnpj_cpf_dest = formatar_cnpj_cpf(data.destinatario.cnpj)
    dhEmissao_formatado = dt_emissao.strftime("%d/%m/%Y")
    dhSaida_formatado = dt_entrada_saida.strftime("%d/%m/%Y")
    hdSaida_formatada = dt_entrada_saida.strftime("%H:%M:%S")
    cep_emitente_formatado = data.destinatario.endereco.cep[:5] + '-' + data.destinatario.endereco.cep[5:]
    dest_cel = formatar_celular(data.destinatario.endereco.fone)
    modFrete_desc = modFrete_descricao.get(data.transp.modFrete, "Valor inválido")
    transportadora = data.transp.transporta.nome if data.transp.transporta else ""
    cnpj_cpf_transp = ""
    if data.transp.transporta:
        cnpj_cpf_transp = formatar_cnpj_cpf(data.transp.transporta.cnpj if data.transp.transporta.cnpj else data.transp.transporta.cpf)
    cnpj_cpf_transp = formatar_cnpj_cpf(data.transp.transporta.cnpj if data.transp.transporta and data.transp.transporta.cnpj else data.transp.transporta.cpf)
    inscricao_estadual = data.transp.transporta.inscricaoEstadual if data.transp.transporta else ""
    endereco_completo = data.transp.transporta.enderecoCompleto if data.transp.transporta else ""
    nome_municipio = data.transp.transporta.nomeMunicipio if data.transp.transporta else ""
    uf_transporta = data.transp.transporta.uf if data.transp.transporta else ""
    placa_veiculo = data.transp.veicTransp.placa if data.transp.veicTransp else ""
    uf_veiculo = data.transp.veicTransp.uf if data.transp.veicTransp else ""
    rntc = data.transp.veicTransp.veic.rntc if data.transp.veicTransp and data.transp.veicTransp.veic else ""
    quantidade_vol = data.transp.vol.quantidade if data.transp.vol else ""
    especie_vol = data.transp.vol.especie if data.transp.vol else ""
    peso_liquido_vol = data.transp.vol.pesoLiquido if data.transp.vol else ""
    peso_bruto_vol = data.transp.vol.pesoBruto if data.transp.vol else ""
    marca_vol = data.transp.vol.marca if data.transp.vol else ""
    numeracao_vol = data.transp.vol.nVol if data.transp.vol else ""
    text_link = "www.nfe.fazenda.gov.br/portal ou no site da Sefaz Autorizadora"

    # Textos
    long_text = (f'RECEBEMOS DE {data.emitente.nome} OS PRODUTOS E/OU SERVIÇOS CONSTANTES DA NOTA FISCAL ELETRÔNICA INDICADA '
                 f'ABAIXO. EMISSÃO: {data_formatada} - VALOR TOTAL: {valor_formatado_canhoto} - DESTINATÁRIO: {data.destinatario.nome} - '
                 f'ENDEREÇO: {data.destinatario.endereco.logradouro} {data.destinatario.endereco.numero} {data.destinatario.endereco.complemento}')
    x = 5 * mm
    y = height - 7 * mm
    max_width = 170 * mm
    line_height = 8

    canvas_draw.setFont("Times-Roman", 5)
    canvas_draw.drawString(margin, 238 * mm, "NATUREZA DA OPERAÇÃO")
    canvas_draw.drawString(margin + 131 * mm, 238 * mm, "PROTOCOLO DE AUTORIZAÇÃO DE USO")
    canvas_draw.drawString(margin, 231 * mm, "INSCRIÇÃO ESTADUAL")
    canvas_draw.drawString(margin + 76 * mm, 231 * mm, "INSCRIÇÃO ESTADUAL DO SUBST. TRIBUT.")
    canvas_draw.drawString(margin + 146 * mm, 231 * mm, "CNPJ")
    canvas_draw.drawString(margin, 220 * mm, "NOME / RAZÃO SOCIAL")
    canvas_draw.drawString(margin + 129 * mm, 220 * mm, "CNPJ / CPF")
    canvas_draw.drawString(margin + 176 * mm, 220 * mm, "DATA DA EMISSÃO")
    canvas_draw.drawString(margin, 213 * mm, "ENDEREÇO")
    canvas_draw.drawString(margin, 206 * mm, "MUNICÍPIO")
    canvas_draw.drawString(margin + 95 * mm, 213 * mm, "BAIRRO / DISTRITO")
    canvas_draw.drawString(margin + 141 * mm, 213 * mm, "CEP")
    canvas_draw.drawString(margin + 176 * mm, 213 * mm, "DATA DA SAÍDA")
    canvas_draw.drawString(margin + 95 * mm, 206 * mm, "UF")
    canvas_draw.drawString(margin + 105 * mm, 206 * mm, "FONE / FAX")
    canvas_draw.drawString(margin + 141 * mm, 206 * mm, "INSCRIÇÃO ESTADUAL")
    canvas_draw.drawString(margin + 176 * mm, 206 * mm, "HORA DA SAÍDA")
    canvas_draw.drawString(margin, 195 * mm, "BASE DE CÁLCULO DO ICMS")
    canvas_draw.drawString(margin, 188 * mm, "VALOR DO FRETE")
    canvas_draw.drawString(margin + 31 * mm, 195 * mm, "VALOR DO ICMS")
    canvas_draw.drawString(margin + 31 * mm, 188 * mm, "VALOR DO SEGURO")
    canvas_draw.drawString(margin + 61 * mm, 195 * mm, "BASE DE CÁLC. ICMS S.T")
    canvas_draw.drawString(margin + 61 * mm, 188 * mm, "DESCONTO")
    canvas_draw.drawString(margin + 91 * mm, 195 * mm, "VALOR DO ICMS SUBST.")
    canvas_draw.drawString(margin + 91 * mm, 188 * mm, "OUTRAS DESPESAS")    
    canvas_draw.drawString(margin + 121 * mm, 195 * mm, "VALOR IMP. IMPORTAÇÃO")
    canvas_draw.drawString(margin + 121 * mm, 188 * mm, "VALOR TOTAL DO IPI")
    canvas_draw.drawString(margin + 156 * mm, 195 * mm, "VALOR DO PIS")
    canvas_draw.drawString(margin + 156 * mm, 188 * mm, "VALOR DA COFINS")
    canvas_draw.drawString(margin + 173.5 * mm, 195 * mm, "VALOR TOTAL DOS PRODUTOS")
    canvas_draw.drawString(margin + 173.5 * mm, 188 * mm, "VALOR TOTAL DA NOTA")
    canvas_draw.drawString(margin, 177 * mm, "NOME / RAZÃO SOCIAL")
    canvas_draw.drawString(margin + 59 * mm, 177 * mm, "FRETE POR CONTA")
    canvas_draw.drawString(margin + 89 * mm, 177 * mm, "CÓDIGO ANTT")
    canvas_draw.drawString(margin + 124 * mm, 177 * mm, "PLACA DO VEÍCULO") 
    canvas_draw.drawString(margin + 154 * mm, 177 * mm, "UF")
    canvas_draw.drawString(margin + 163 * mm, 177 * mm, "CNPJ / CPF")
    canvas_draw.drawString(margin, 170 * mm, "ENDEREÇO")
    canvas_draw.drawString(margin + 89 * mm, 170 * mm, "MUNICÍPIO")
    canvas_draw.drawString(margin + 154 * mm, 170 * mm, "UF")
    canvas_draw.drawString(margin + 163 * mm, 170 * mm, "INSCRIÇÃO ESTADUAL")
    canvas_draw.drawString(margin, 163 * mm, "QUANIDADE")
    canvas_draw.drawString(margin + 21 * mm, 163 * mm, "ESPÉCIE")
    canvas_draw.drawString(margin + 56 * mm, 163 * mm, "MARCA")
    canvas_draw.drawString(margin + 89 * mm, 163 * mm, "NUMERAÇÃO") 
    canvas_draw.drawString(margin + 127 * mm, 163 * mm, "PESO BRUTO")
    canvas_draw.drawString(margin + 171 * mm, 163 * mm, "PESO LÍQUIDO")
    canvas_draw.drawString(margin + 4.8 * mm, 149.9 * mm, "CÓDIGO")
    canvas_draw.drawString(margin + 33 * mm, 149.9 * mm, "DESCRIÇÃO DO PRODUTO / SERVIÇO")
    canvas_draw.drawString(margin + 84 * mm, 149.9 * mm, "NCM/SH")
    canvas_draw.drawString(margin + 97.5 * mm, 149.9 * mm, "O/CST")
    canvas_draw.drawString(margin + 107.5 * mm, 149.9 * mm, "CFOP")
    canvas_draw.drawString(margin + 116 * mm, 149.9 * mm, "UN.")
    canvas_draw.drawString(margin + 122 * mm, 149.9 * mm, "QUANT.")
    canvas_draw.drawString(margin + 132 * mm, 151 * mm, "VALOR")
    canvas_draw.drawString(margin + 133 * mm, 149 * mm, "UNIT.")
    canvas_draw.drawString(margin + 142 * mm, 151 * mm, "VALOR")
    canvas_draw.drawString(margin + 142 * mm, 149 * mm, "TOTAL")
    canvas_draw.drawString(margin + 151.5 * mm, 151 * mm, "B. CÁLC.")
    canvas_draw.drawString(margin + 152.5 * mm, 149 * mm, "ICMS")
    canvas_draw.drawString(margin + 161.5 * mm, 151 * mm, "VALOR")
    canvas_draw.drawString(margin + 162.5 * mm, 149 * mm, "ICMS")
    canvas_draw.drawString(margin + 171.5 * mm, 151 * mm, "VALOR")
    canvas_draw.drawString(margin + 173.5 * mm, 149 * mm, "IPI")
    canvas_draw.drawString(margin + 182.2 * mm, 151 * mm, "ALÍQ.")
    canvas_draw.drawString(margin + 182.5 * mm, 149 * mm, "ICMS")
    canvas_draw.drawString(margin + 192 * mm, 151 * mm, "ALÍQ.")
    canvas_draw.drawString(margin + 193 * mm, 149 * mm, "IPI")
    canvas_draw.drawString(margin, 15 * mm, "INFORMAÇÕES COMPLEMENTARES ")
    canvas_draw.drawString(margin + 151 * mm, 15 * mm, "RESERVADO AO FISCO")

    canvas_draw.setFont("Times-Roman", 6)
    canvas_draw.drawString(margin, 280.5 * mm, "DATA DE RECEBIMENTO")
    canvas_draw.drawString(margin + 46 * mm, 280.5 * mm, "IDENTIFICAÇÃO E ASSINATURA DO RECEBEDOR")
    canvas_draw.drawString(margin + 131 * mm, 254.5 * mm, "CHAVE DE ACESSO")

    canvas_draw.setFont("Times-Bold", 6)
    canvas_draw.drawString(margin, 222.5 * mm, "DESTINATÁRIO / REMETENTE")
    canvas_draw.drawString(margin, 197.5 * mm, "CÁLCULO DO IMPOSTO")
    canvas_draw.drawString(margin, 179.5 * mm, "TRANSPORTADOR / VOLUMES TRANSPORTADOS")
    canvas_draw.drawString(margin, 154.5 * mm, "DADOS DOS PRODUTOS / SERVIÇOS")
    canvas_draw.drawString(margin, 17.5 * mm, "DADOS ADICIONAIS")
    canvas_draw.setFont("Times-Roman", 7)
    draw_wrapped_text(canvas_draw, long_text, x, y, max_width, line_height)
    canvas_draw.drawCentredString(margin + 45 * mm, 252 * mm, f'{data.emitente.endereco.logradouro} {data.emitente.endereco.numero}')
    canvas_draw.drawCentredString(margin + 45 * mm, 249 * mm, f'{data.emitente.endereco.bairro}, {nome_municipio_emit["nome"]}/{data.emitente.endereco.uf} - {cep_formatado}')
    canvas_draw.drawCentredString(margin + 45 * mm, 246 * mm, f'Telefone: {formatar_celular(data.emitente.endereco.fone)}')
    canvas_draw.drawCentredString(margin + 165 * mm, 245 * mm, "Consulta de autenticidade no portal nacional da NF-e")
    canvas_draw.drawCentredString(x_position, y_position + 1 * mm, text_link)

    canvas_draw.setFont("Times-Bold", 7)
    canvas_draw.drawCentredString(margin + 112.5 * mm, 264 * mm, "Documento Auxiliar da Nota")
    canvas_draw.drawString(margin + 59 * mm, 173 * mm, modFrete_desc)

    canvas_draw.setFont("Times-Bold", 7.9)
    canvas_draw.drawCentredString(margin + 165 * mm, 250.5 * mm, f'{chave_acesso_formatada}')

    canvas_draw.setFont("Times-Bold", 8)
    protocolo = get_emissao_details(data)
    canvas_draw.drawCentredString(margin + 165 * mm, 234 * mm, f'{protocolo}')
    canvas_draw.drawCentredString(margin + 45 * mm, 255 * mm, f'{data.emitente.nome}')
    canvas_draw.drawCentredString(margin + 112.5 * mm, 261 * mm, "Fiscal Eletrônica")
    canvas_draw.drawString(margin + 98 * mm, 256 * mm, "0 - ENTRADA")
    canvas_draw.drawString(margin + 98 * mm, 252.5 * mm, "1 - SAÍDA")
    canvas_draw.drawString(margin, 216 * mm, f'{data.destinatario.nome}')
    canvas_draw.drawCentredString(margin + 150 * mm, 216 * mm, cnpj_cpf_dest)
    canvas_draw.drawString(margin, 209 * mm, f'{data.destinatario.endereco.logradouro} {data.destinatario.endereco.numero} {data.destinatario.endereco.complemento}')
    canvas_draw.drawString(margin + 102 * mm, 209 * mm, f'{data.destinatario.endereco.bairro}')
    canvas_draw.drawString(margin + 150 * mm, 209 * mm, f'{cep_emitente_formatado}')
    canvas_draw.drawString(margin, 202 * mm, f'{nome_municipio_dest["nome"]}')
    canvas_draw.drawCentredString(margin + 188 * mm, 216 * mm, f'{dhEmissao_formatado}')
    canvas_draw.drawCentredString(margin + 188 * mm, 209 * mm, f'{dhSaida_formatado}')
    canvas_draw.drawCentredString(margin + 188 * mm, 202 * mm, f'{hdSaida_formatada}')
    canvas_draw.drawCentredString(margin + 155 * mm, 202 * mm, f'{data.destinatario.ie}')
    canvas_draw.drawCentredString(margin + 99 * mm, 202 * mm, f'{data.destinatario.endereco.uf}')
    canvas_draw.drawCentredString(margin + 120 * mm, 202 * mm, f'{dest_cel}')
    canvas_draw.drawRightString(margin + 29 * mm, 191 * mm, f'{formatar_moeda(data.total.icmsTot.vBc)}')
    canvas_draw.drawRightString(margin + 29 * mm, 184 * mm, f'{formatar_moeda(data.total.icmsTot.vFrete)}')
    canvas_draw.drawRightString(margin + 59 * mm, 191 * mm, f'{formatar_moeda(data.total.icmsTot.vIcms)}')
    canvas_draw.drawRightString(margin + 59 * mm, 184 * mm, f'{formatar_moeda(data.total.icmsTot.vSeg)}')
    canvas_draw.drawRightString(margin + 89 * mm, 191 * mm, f'{formatar_moeda(data.total.icmsTot.vBcSt)}')
    canvas_draw.drawRightString(margin + 89 * mm, 184 * mm, f'{formatar_moeda(data.total.icmsTot.vDesc)}')
    canvas_draw.drawRightString(margin + 119 * mm, 191 * mm, f'{formatar_moeda(data.total.icmsTot.vSt)}')
    canvas_draw.drawRightString(margin + 119 * mm, 184 * mm, f'{formatar_moeda(data.total.icmsTot.vOutro)}')
    canvas_draw.drawRightString(margin + 154 * mm, 191 * mm, f'{formatar_moeda(data.total.icmsTot.vIi)}')
    canvas_draw.drawRightString(margin + 154 * mm, 184 * mm, f'{formatar_moeda(data.total.icmsTot.vIpi)}')
    canvas_draw.drawRightString(margin + 171.5 * mm, 184 * mm, f'{formatar_moeda(data.total.icmsTot.vPis)}')
    canvas_draw.drawRightString(margin + 171.5 * mm, 191 * mm, f'{formatar_moeda(data.total.icmsTot.vCofins)}')
    canvas_draw.drawRightString(margin + 199 * mm, 191 * mm, f'{formatar_moeda(data.total.icmsTot.vProd)}')
    canvas_draw.drawRightString(margin + 199 * mm, 184 * mm, f'{formatar_moeda(data.total.icmsTot.vNf)}')
    canvas_draw.drawString(margin, 173 * mm, transportadora)
    canvas_draw.drawString(margin + 89 * mm, 173 * mm, rntc)
    canvas_draw.drawString(margin + 124 * mm, 173 * mm, placa_veiculo)
    canvas_draw.drawString(margin + 154 * mm, 173 * mm, uf_veiculo)
    canvas_draw.drawString(margin + 163 * mm, 173 * mm, cnpj_cpf_transp)
    canvas_draw.drawString(margin, 166 * mm, endereco_completo)
    canvas_draw.drawString(margin + 89 * mm, 166 * mm, nome_municipio)
    canvas_draw.drawString(margin + 154 * mm, 166 * mm, uf_transporta)
    canvas_draw.drawString(margin + 163 * mm, 166 * mm, inscricao_estadual)
    canvas_draw.drawString(margin, 159 * mm, quantidade_vol)
    canvas_draw.drawString(margin + 21 * mm, 159 * mm, especie_vol)
    canvas_draw.drawString(margin + 56 * mm, 159 * mm, marca_vol)
    canvas_draw.drawString(margin + 89 * mm, 159 * mm, numeracao_vol)
    canvas_draw.drawString(margin + 127 * mm, 159 * mm, peso_bruto_vol)
    canvas_draw.drawString(margin + 171 * mm, 159 * mm, peso_liquido_vol)


    canvas_draw.setFont("Times-Roman", 10)
    canvas_draw.drawCentredString(margin + 112.5 * mm, 248.5 * mm, f'Nº. {numero_nota_formatado}')
    canvas_draw.drawCentredString(margin + 112.5 * mm, 245 * mm, f'SÉRIE {serie_formatada}')
    canvas_draw.drawString(width - 32 * mm, 283 * mm, f'Nº. {numero_nota_formatado}')
    canvas_draw.drawString(width - 27.5 * mm, 279 * mm, f'SÉRIE {serie_formatada}')

    canvas_draw.setFont("Times-Bold", 10)
    canvas_draw.drawCentredString(margin + 60 * mm, 234 * mm, f'{data.identificacao.naturezaOperacao}')
    canvas_draw.drawCentredString(margin + 35 * mm, 227 * mm, f'{data.emitente.inscricaoEstadual}')  
    canvas_draw.drawCentredString(margin + 110 * mm, 227 * mm, f'{data.emitente.cnpj}')
    canvas_draw.drawCentredString(margin + 170 * mm, 227 * mm, f'{formatar_cnpj_cpf(data.emitente.cnpj)}')

    canvas_draw.setFont("Times-Roman", 12)
    canvas_draw.drawCentredString(margin + 112 * mm, 267 * mm, "DANFE")

    canvas_draw.setFont("Times-Bold", 16)
    canvas_draw.drawString(width - 26 * mm, 288 * mm, "NF-e")
    
    canvas_draw.setFont("Times-Bold", 22)
    canvas_draw.drawCentredString(margin + 125 * mm, 252.5 * mm, f'{data.identificacao.tpNf}')
    
    # Logo
    largura_imagem = 100 
    altura_imagem = 23
    linha_esquerda_x = margin - 1 * mm
    linha_direita_x = margin + 95 * mm
    x_centralizado = linha_esquerda_x + ((linha_direita_x - linha_esquerda_x) / 2) - (largura_imagem / 2)
    y_imagem = 260 * mm   
    logoCliente = "logo-outbound.jpg"
    canvas_draw.drawImage(logoCliente, x_centralizado, y_imagem, largura_imagem, altura_imagem)
    
    # Codigo de Barras
    chave_acesso = data.key
    codigo_barras = code128.Code128(chave_acesso, barHeight=10.5 * mm, barWidth=0.68)
    codigo_barras.drawOn(canvas_draw, margin + 125.5 * mm, 259.5 * mm)
    
    # Link
    link = "http://www.nfe.fazenda.gov.br/portal"
    text_width = canvas_draw.stringWidth(text_link, "Times-Bold", 7)
    link_x1 = x_position - (text_width / 2)
    link_y1 = y_position
    link_x2 = x_position + (text_width / 2)
    link_y2 = y_position + 10 
    canvas_draw.linkURL(link, (link_x1, link_y1, link_x2, link_y2), relative=1)

    # Linhas
#--------------------------------------------------------------------CANHOTO----------------------------------------------------------------------#
    # Horizontais - Ordem de Cima Pra Baixo
    canvas_draw.line(margin - 1 * mm, 293 * mm, width - margin, 293 * mm) 
    canvas_draw.line(margin - 1 * mm, 283 * mm, width - 35 * mm, 283 * mm)
    canvas_draw.line(margin - 1 * mm, 275 * mm, width - margin, 275 * mm)  
    # Verticais - Esquerda Pra Direita
    canvas_draw.line(margin - 1 * mm, 293 * mm, margin - 1 * mm, 275 * mm) 
    canvas_draw.line(margin + 45 * mm, 283 * mm, margin + 45 * mm, 275 * mm) 
    canvas_draw.line(width - 35 * mm, 293 * mm, width - 35 * mm, 275 * mm) 
    canvas_draw.line(width - margin, 293 * mm, width - margin, 275 * mm) 
    # Tracejada
    canvas_draw.setDash(4, 2)
    canvas_draw.line(margin - 1 * mm, 273.5 * mm, width - margin, 273.5 * mm) 
    canvas_draw.setDash()
#--------------------------------------------------------------------HEADER----------------------------------------------------------------------#
    # Horizontais - Ordem de Cima Pra Baixo
    canvas_draw.line(margin - 1 * mm, 272 * mm, width - margin, 272 * mm) 
    canvas_draw.line(margin + 130 * mm, 257 * mm, width - margin, 257 * mm) 
    canvas_draw.line(margin + 130 * mm, 248.5 * mm, width - margin, 248.5 * mm) 
    canvas_draw.line(margin - 1 * mm, 240 * mm, width - margin, 240 * mm)
    canvas_draw.line(margin - 1 * mm, 233 * mm, width - margin, 233 * mm) 
    canvas_draw.line(margin - 1 * mm, 226 * mm, width - margin, 226 * mm)
    # Verticais - Esquerda Pra Direita
    canvas_draw.line(margin - 1 * mm, 272 * mm, margin - 1 * mm, 226 * mm)
    canvas_draw.line(margin + 75 * mm, 233 * mm, margin + 75 * mm, 226 * mm) 
    canvas_draw.line(margin + 95 * mm, 272 * mm, margin + 95 * mm, 240 * mm)
    canvas_draw.line(margin + 130 * mm, 272 * mm, margin + 130 * mm, 233 * mm)
    canvas_draw.line(margin + 145 * mm, 233 * mm, margin + 145 * mm, 226 * mm) 
    canvas_draw.line(width - margin, 272 * mm, width - margin, 226 * mm)
#--------------------------------------------------------------------DESTINATÁRIO/REMETENTE------------------------------------------------------#
    # Horizontais - Ordem de Cima Pra Baixo
    canvas_draw.line(margin - 1 * mm, 222 * mm, width - margin, 222 * mm)
    canvas_draw.line(margin - 1 * mm, 215 * mm, width - margin, 215 * mm)
    canvas_draw.line(margin - 1 * mm, 208 * mm, width - margin, 208 * mm)
    canvas_draw.line(margin - 1 * mm, 201 * mm, width - margin, 201 * mm)
    # Verticais - Esquerda Pra Direita
    canvas_draw.line(margin - 1 * mm, 222 * mm, margin - 1 * mm, 201 * mm)
    canvas_draw.line(margin + 94 * mm, 215 * mm, margin + 94 * mm, 201 * mm)
    canvas_draw.line(margin + 104 * mm, 208 * mm,margin + 104 * mm, 201 * mm)
    canvas_draw.line(margin + 128 * mm, 222 * mm, margin + 128 * mm, 215 * mm)
    canvas_draw.line(margin + 140 * mm, 215 * mm, margin + 140 * mm, 201 * mm)
    canvas_draw.line(margin + 175 * mm, 222 * mm, margin + 175 * mm, 201 * mm)
    canvas_draw.line(width - margin, 222 * mm, width - margin, 201 * mm)
#--------------------------------------------------------------------CÁLCULO DO IMPOSTO------------------------------------------------------#
    # Horizontais - Ordem de Cima Pra Baixo
    canvas_draw.line(margin - 1 * mm, 197 * mm, width - margin, 197 * mm)
    canvas_draw.line(margin - 1 * mm, 190 * mm, width - margin, 190 * mm)
    canvas_draw.line(margin - 1 * mm, 183 * mm, width - margin, 183 * mm)
    # Verticais - Esquerda Pra Direita
    canvas_draw.line(margin - 1 * mm, 197 * mm, margin - 1 * mm, 183 * mm)
    canvas_draw.line(margin + 30 * mm, 197 * mm, margin + 30 * mm, 183 * mm)
    canvas_draw.line(margin + 60 * mm, 197 * mm, margin + 60 * mm, 183 * mm)
    canvas_draw.line(margin + 90 * mm, 197 * mm, margin + 90 * mm, 183 * mm)
    canvas_draw.line(margin + 120 * mm, 197 * mm, margin + 120 * mm, 183 * mm)
    canvas_draw.line(margin + 155 * mm, 197 * mm, margin + 155 * mm, 183 * mm)
    canvas_draw.line(margin + 173 * mm, 197 * mm, margin + 173 * mm, 183 * mm)
    canvas_draw.line(width - margin, 197 * mm, width - margin, 183 * mm)
#--------------------------------------------------------------------TRANSPORTADOR / VOLUMES TRANSPORTADOS---------------------------------------#
    # Horizontais - Ordem de Cima Pra Baixo
    canvas_draw.line(margin - 1 * mm, 179 * mm, width - margin, 179 * mm)
    canvas_draw.line(margin - 1 * mm, 172 * mm, width - margin, 172 * mm)
    canvas_draw.line(margin - 1 * mm, 165 * mm, width - margin, 165 * mm)
    canvas_draw.line(margin - 1 * mm, 158 * mm, width - margin, 158 * mm)
    # Verticais - Esquerda Pra Direita
    canvas_draw.line(margin - 1 * mm, 179 * mm, margin - 1 * mm, 158 * mm)
    canvas_draw.line(margin + 20 * mm, 165 * mm, margin + 20 * mm, 158 * mm)
    canvas_draw.line(margin + 55 * mm, 165 * mm, margin + 55 * mm, 158 * mm)
    canvas_draw.line(margin + 58 * mm, 179 * mm, margin + 58 * mm, 172 * mm)
    canvas_draw.line(margin + 88 * mm, 179 * mm, margin + 88 * mm, 158 * mm)
    canvas_draw.line(margin + 123 * mm, 179 * mm, margin + 123 * mm, 172 * mm)
    canvas_draw.line(margin + 126 * mm, 165 * mm, margin + 126 * mm, 158 * mm)
    canvas_draw.line(margin + 153 * mm, 179 * mm, margin + 153 * mm, 165 * mm)
    canvas_draw.line(margin + 162 * mm, 179 * mm, margin + 162 * mm, 165 * mm)
    canvas_draw.line(margin + 170 * mm, 165 * mm, margin + 170 * mm, 158 * mm)
    canvas_draw.line(width - margin, 179 * mm, width - margin, 158 * mm)

#--------------------------------------------------------------------DADOS DOS PRODUTOS / SERVIÇOS----------------------------------------------------------------------#
    # Horizontais - Ordem de Cima Pra Baixo
    canvas_draw.line(margin - 1 * mm, 154 * mm, width - margin, 154 * mm)
    canvas_draw.line(margin - 1 * mm, 147 * mm, width - margin, 147 * mm)
    # Verticais - Esquerda Pra Direita
    canvas_draw.line(margin - 1 * mm, 154 * mm, margin - 1 * mm, 147 * mm)
    canvas_draw.line(margin + 18 * mm, 154 * mm, margin + 18 * mm, 147 * mm)
    canvas_draw.line(margin + 80 * mm, 154 * mm, margin + 80 * mm, 147 * mm)
    canvas_draw.line(margin + 95 * mm, 154 * mm, margin + 95 * mm, 147 * mm)
    canvas_draw.line(margin + 105 * mm, 154 * mm, margin + 105 * mm, 147 * mm)
    canvas_draw.line(margin + 115 * mm, 154 * mm, margin + 115 * mm, 147 * mm)
    canvas_draw.line(margin + 120 * mm, 154 * mm, margin + 120 * mm, 147 * mm)
    canvas_draw.line(margin + 130 * mm, 154 * mm, margin + 130 * mm, 147 * mm)
    canvas_draw.line(margin + 140 * mm, 154 * mm, margin + 140 * mm, 147 * mm)
    canvas_draw.line(margin + 150 * mm, 154 * mm, margin + 150 * mm, 147 * mm)
    canvas_draw.line(margin + 160 * mm, 154 * mm, margin + 160 * mm, 147 * mm)
    canvas_draw.line(margin + 170 * mm, 154 * mm, margin + 170 * mm, 147 * mm)
    canvas_draw.line(margin + 180 * mm, 154 * mm, margin + 180 * mm, 147 * mm)
    canvas_draw.line(margin + 190 * mm, 154 * mm, margin + 190 * mm, 147 * mm)
    canvas_draw.line(width - margin, 154 * mm, width - margin, 147 * mm)
    
#--------------------------------------------------------------------DADOS ADICIONAIS----------------------------------------------------------------------#
    # Horizontais - Ordem de Cima Pra Baixo
    canvas_draw.line(margin - 1 * mm, 17 * mm, width - margin, 17 * mm)
    canvas_draw.line(margin - 1 * mm, 5 * mm, width - margin, 5 * mm)
    # Verticais - Esquerda Pra Direita
    canvas_draw.line(margin - 1 * mm, 17 * mm, margin - 1 * mm, 5 * mm)
    canvas_draw.line(margin + 150 * mm, 17 * mm, margin + 150 * mm, 5 * mm)
    canvas_draw.line(width - margin, 17 * mm, width - margin, 5 * mm)

#--------------------------------------------------------------------PAGINA ADICIONAL----------------------------------------------------------------------#

def render_additional_page(canvas_draw, data: Danfe, width, height, margin):
    # Formatações
    adicionar_altura_y = 20
    serie_formatada = data.identificacao.serie.zfill(3)
    numero_nota = data.identificacao.numeroDocFiscal.zfill(9)
    partes = [numero_nota[i:i+3] for i in range(0, len(numero_nota), 3)]
    numero_nota_formatado = '.'.join(partes)
    cep_formatado = data.emitente.endereco.cep[:5] + '-' + data.emitente.endereco.cep[5:]
    adicionar_altura_y_lista = 88
    emit_municipio = data.emitente.endereco.codigoMunicipio
    response_municipio_emit = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{emit_municipio}')
    nome_municipio_emit = response_municipio_emit.json()

    # Logo
    largura_imagem = 100
    altura_imagem = 23
    linha_esquerda_x = margin - 1 * mm
    linha_direita_x = margin + 95 * mm
    x_centralizado = linha_esquerda_x + ((linha_direita_x - linha_esquerda_x) / 2) - (largura_imagem / 2)
    y_imagem = (260 + adicionar_altura_y) * mm   
    logoCliente = "logo-outbound.jpg"
    canvas_draw.drawImage(logoCliente, x_centralizado, y_imagem, largura_imagem, altura_imagem)

    # Código de Barras Code 128
    chave_acesso = data.key
    codigo_barras = code128.Code128(chave_acesso, barHeight=10.5 * mm, barWidth=0.68)
    codigo_barras.drawOn(canvas_draw, margin + 125.5 * mm, (259.5 + adicionar_altura_y) * mm)
    chave_acesso_formatada = formatar_chave_acesso(data.key)
    
    # Link
    x_position = margin + 165 * mm
    y_position = (241 + adicionar_altura_y) * mm
    text = "www.nfe.fazenda.gov.br/portal ou no site da Sefaz Autorizadora"
    link = "http://www.nfe.fazenda.gov.br/portal"
    text_width = canvas_draw.stringWidth(text, "Times-Bold", 7)
    link_x1 = x_position - (text_width / 2)
    link_y1 = y_position
    link_x2 = x_position + (text_width / 2)
    link_y2 = y_position + 10 
    canvas_draw.linkURL(link, (link_x1, link_y1, link_x2, link_y2), relative=1)

    # Textos
    canvas_draw.setFont("Times-Roman", 5)
    canvas_draw.drawString(margin, (238 + adicionar_altura_y) * mm, "NATUREZA DA OPERAÇÃO")
    canvas_draw.drawString(margin + 131 * mm, (238 + adicionar_altura_y) * mm, "PROTOCOLO DE AUTORIZAÇÃO DE USO")
    canvas_draw.drawString(margin, (231 + adicionar_altura_y) * mm, "INSCRIÇÃO ESTADUAL")
    canvas_draw.drawString(margin + 76 * mm, (231 + adicionar_altura_y) * mm, "INSCRIÇÃO ESTADUAL DO SUBST. TRIBUT.")
    canvas_draw.drawString(margin + 146 * mm, (231 + adicionar_altura_y) * mm, "CNPJ")
    canvas_draw.drawString(margin + 4.8 * mm, (149.9 + adicionar_altura_y_lista) * mm, "CÓDIGO")
    canvas_draw.drawString(margin + 33 * mm, (149.9 + adicionar_altura_y_lista) * mm, "DESCRIÇÃO DO PRODUTO / SERVIÇO")
    canvas_draw.drawString(margin + 84 * mm, (149.9 + adicionar_altura_y_lista) * mm, "NCM/SH")
    canvas_draw.drawString(margin + 97.5 * mm, (149.9 + adicionar_altura_y_lista) * mm, "O/CST")
    canvas_draw.drawString(margin + 107.5 * mm, (149.9 + adicionar_altura_y_lista) * mm, "CFOP")
    canvas_draw.drawString(margin + 116 * mm, (149.9 + adicionar_altura_y_lista) * mm, "UN.")
    canvas_draw.drawString(margin + 122 * mm, (149.9 + adicionar_altura_y_lista) * mm, "QUANT.")
    canvas_draw.drawString(margin + 132 * mm, (151 + adicionar_altura_y_lista) * mm, "VALOR")
    canvas_draw.drawString(margin + 133 * mm, (149 + adicionar_altura_y_lista) * mm, "UNIT.")
    canvas_draw.drawString(margin + 142 * mm, (151 + adicionar_altura_y_lista) * mm, "VALOR")
    canvas_draw.drawString(margin + 142 * mm, (149 + adicionar_altura_y_lista) * mm, "TOTAL")
    canvas_draw.drawString(margin + 151.5 * mm, (151 + adicionar_altura_y_lista) * mm, "B. CÁLC.")
    canvas_draw.drawString(margin + 152.5 * mm, (149 + adicionar_altura_y_lista) * mm, "ICMS")
    canvas_draw.drawString(margin + 161.5 * mm, (151 + adicionar_altura_y_lista) * mm, "VALOR")
    canvas_draw.drawString(margin + 162.5 * mm, (149 + adicionar_altura_y_lista) * mm, "ICMS")
    canvas_draw.drawString(margin + 171.5 * mm, (151 + adicionar_altura_y_lista) * mm, "VALOR")
    canvas_draw.drawString(margin + 173.5 * mm, (149 + adicionar_altura_y_lista) * mm, "IPI")
    canvas_draw.drawString(margin + 182.2 * mm, (151 + adicionar_altura_y_lista) * mm, "ALÍQ.")
    canvas_draw.drawString(margin + 182.5 * mm, (149 + adicionar_altura_y_lista) * mm, "ICMS")
    canvas_draw.drawString(margin + 192 * mm, (151 + adicionar_altura_y_lista) * mm, "ALÍQ.")
    canvas_draw.drawString(margin + 193 * mm, (149 + adicionar_altura_y_lista) * mm, "IPI")

    canvas_draw.setFont("Times-Roman", 6)
    canvas_draw.drawString(margin + 131 * mm, (254.5 + adicionar_altura_y) * mm, "CHAVE DE ACESSO")
    canvas_draw.drawString(margin, (154.5 + adicionar_altura_y_lista) * mm, "DADOS DOS PRODUTOS / SERVIÇOS")

    canvas_draw.setFont("Times-Roman", 7)
    canvas_draw.drawCentredString(margin + 45 * mm, (252 + adicionar_altura_y) * mm, f'{data.emitente.endereco.logradouro} {data.emitente.endereco.numero}')
    canvas_draw.drawCentredString(margin + 45 * mm, (249 + adicionar_altura_y) * mm, f'{data.emitente.endereco.bairro}, {nome_municipio_emit["nome"]}/{data.emitente.endereco.uf} - {cep_formatado}')
    canvas_draw.drawCentredString(margin + 45 * mm, (246 + adicionar_altura_y) * mm, f'Telefone: {formatar_celular(data.emitente.endereco.fone)}')
    canvas_draw.drawCentredString(margin + 165 * mm, (245 + adicionar_altura_y) * mm, "Consulta de autenticidade no portal nacional da NF-e")
    canvas_draw.drawCentredString(x_position, y_position + 1 * mm, text)

    canvas_draw.setFont("Times-Bold", 7.9)
    canvas_draw.drawCentredString(margin + 165 * mm, (250.5 + adicionar_altura_y) * mm, f'{chave_acesso_formatada}')
    
    canvas_draw.setFont("Times-Bold", 7)
    canvas_draw.drawCentredString(margin + 112.5 * mm, (264 + adicionar_altura_y) * mm, "Documento Auxiliar da Nota")

    canvas_draw.setFont("Times-Bold", 8)
    protocolo = get_emissao_details(data)
    canvas_draw.drawCentredString(margin + 165 * mm, (234 + adicionar_altura_y) * mm, f'{protocolo}')
    canvas_draw.drawCentredString(margin + 45 * mm, (255 + adicionar_altura_y) * mm, f'{data.emitente.nome}')
    canvas_draw.drawCentredString(margin + 112.5 * mm, (261 + adicionar_altura_y) * mm, "Fiscal Eletrônica")
    canvas_draw.drawString(margin + 98 * mm, (256 + adicionar_altura_y) * mm, "0 - ENTRADA")
    canvas_draw.drawString(margin + 98 * mm, (252.5 + adicionar_altura_y) * mm, "1 - SAÍDA")

    canvas_draw.setFont("Times-Roman", 10)
    canvas_draw.drawCentredString(margin + 112.5 * mm, (248.5 + adicionar_altura_y) * mm, f'Nº. {numero_nota_formatado}')
    canvas_draw.drawCentredString(margin + 112.5 * mm, (245 + adicionar_altura_y) * mm, f'SÉRIE {serie_formatada}')

    canvas_draw.setFont("Times-Bold", 10)
    canvas_draw.drawCentredString(margin + 60 * mm, (234 + adicionar_altura_y) * mm, f'{data.identificacao.naturezaOperacao}')
    canvas_draw.drawCentredString(margin + 35 * mm, (227 + adicionar_altura_y) * mm, f'{data.emitente.inscricaoEstadual}')  
    canvas_draw.drawCentredString(margin + 110 * mm, (227 + adicionar_altura_y) * mm, f'{data.emitente.cnpj}')
    canvas_draw.drawCentredString(margin + 170 * mm, (227 + adicionar_altura_y) * mm, f'{formatar_cnpj_cpf(data.emitente.cnpj)}')

    canvas_draw.setFont("Times-Roman", 12)
    canvas_draw.drawCentredString(margin + 112 * mm, (267 + adicionar_altura_y) * mm, "DANFE")

    canvas_draw.setFont("Times-Bold", 22)
    canvas_draw.drawCentredString(margin + 125 * mm, (252.5 + adicionar_altura_y) * mm, f'{data.identificacao.tpNf}')


    # Linhas
    #--------------------------------------------------------------------HEADER----------------------------------------------------------------------#
    # Horizontais - Ordem de Cima Pra Baixo
    canvas_draw.line(margin - 1 * mm, (272 + adicionar_altura_y) * mm, width - margin, (272 + adicionar_altura_y) * mm) 
    canvas_draw.line(margin + 130 * mm, (257 + adicionar_altura_y) * mm, width - margin, (257 + adicionar_altura_y) * mm) 
    canvas_draw.line(margin + 130 * mm, (248.5 + adicionar_altura_y) * mm, width - margin, (248.5 + adicionar_altura_y) * mm) 
    canvas_draw.line(margin - 1 * mm, (240 + adicionar_altura_y) * mm, width - margin, (240 + adicionar_altura_y) * mm)
    canvas_draw.line(margin - 1 * mm, (233 + adicionar_altura_y) * mm, width - margin, (233 + adicionar_altura_y) * mm) 
    canvas_draw.line(margin - 1 * mm, (226 + adicionar_altura_y) * mm, width - margin, (226 + adicionar_altura_y) * mm)
    # Verticais - Esquerda Pra Direita
    canvas_draw.line(margin - 1 * mm, (272 + adicionar_altura_y) * mm, margin - 1 * mm, (226 + adicionar_altura_y) * mm)
    canvas_draw.line(margin + 75 * mm, (233 + adicionar_altura_y) * mm, margin + 75 * mm, (226 + adicionar_altura_y) * mm) 
    canvas_draw.line(margin + 95 * mm, (272 + adicionar_altura_y) * mm, margin + 95 * mm, (240 + adicionar_altura_y) * mm)
    canvas_draw.line(margin + 130 * mm, (272 + adicionar_altura_y) * mm, margin + 130 * mm, (233 + adicionar_altura_y) * mm)
    canvas_draw.line(margin + 145 * mm, (233 + adicionar_altura_y) * mm, margin + 145 * mm, (226 + adicionar_altura_y) * mm) 
    canvas_draw.line(width - margin, (272 + adicionar_altura_y) * mm, width - margin, (226 + adicionar_altura_y) * mm)

    #--------------------------------------------------------------------DADOS DOS PRODUTOS / SERVIÇOS----------------------------------------------------------------------#

    # Horizontais - Ordem de Cima Pra Baixo
    canvas_draw.line(margin - 1 * mm, (154 + adicionar_altura_y_lista) * mm, width - margin, (154 + adicionar_altura_y_lista) * mm)
    canvas_draw.line(margin - 1 * mm, 235 * mm, width - margin, 235 * mm)
    canvas_draw.line(margin - 1 * mm, 5 * mm, width - margin, 5 * mm)
    # Verticais - Esquerda Pra Direita
    canvas_draw.line(margin - 1 * mm, (154 + adicionar_altura_y_lista) * mm, margin - 1 * mm, 5 * mm)
    canvas_draw.line(margin + 18 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 18 * mm, 5 * mm)
    canvas_draw.line(margin + 80 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 80 * mm, 5 * mm)
    canvas_draw.line(margin + 95 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 95 * mm, 5 * mm)
    canvas_draw.line(margin + 105 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 105 * mm, 5 * mm)
    canvas_draw.line(margin + 115 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 115 * mm, 5 * mm)
    canvas_draw.line(margin + 120 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 120 * mm, 5 * mm)
    canvas_draw.line(margin + 130 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 130 * mm, 5 * mm)
    canvas_draw.line(margin + 140 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 140 * mm, 5 * mm)
    canvas_draw.line(margin + 150 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 150 * mm, 5 * mm)
    canvas_draw.line(margin + 160 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 160 * mm, 5 * mm)
    canvas_draw.line(margin + 170 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 170 * mm, 5 * mm)
    canvas_draw.line(margin + 180 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 180 * mm, 5 * mm)
    canvas_draw.line(margin + 190 * mm, (154 + adicionar_altura_y_lista) * mm, margin + 190 * mm, 5 * mm)
    canvas_draw.line(width - margin, (154 + adicionar_altura_y_lista) * mm, width - margin, 5 * mm)

#-------------------------------------------------------------------------Funções Auxiliares-------------------------------------------------------------#

def render_item_line(canvas_draw, item, y, margin):
    canvas_draw.setFont("Times-Roman", 5)
    
    # Renderizar descrição do produto com quebra de linha
    descricao = item["prod"].get("descricao", "")
    descricao_linhas = [descricao[i:i+47] for i in range(0, len(descricao), 47)]
    for i, linha in enumerate(descricao_linhas):
        canvas_draw.drawString(margin + 19 * mm, y - (i * 4 * mm), linha)
    
    # Atualizar a coordenada y considerando a altura ocupada pela descrição
    y -= (len(descricao_linhas) - 1) * 4 * mm
    
    # Renderizar os demais campos
    canvas_draw.drawCentredString(margin + 8 * mm, y, item["prod"].get("codigo", ""))
    canvas_draw.drawCentredString(margin + 87.5 * mm, y, item["prod"].get("ncm", ""))
    canvas_draw.drawCentredString(margin + 100 * mm, y, item["imposto"]["icms"].get("cst", "").zfill(3))
    canvas_draw.drawCentredString(margin + 110 * mm, y, item["prod"].get("codigoFiscalOperacoes", ""))
    canvas_draw.drawCentredString(margin + 117.5 * mm, y, item["prod"].get("unidadeComercial", ""))
    canvas_draw.drawRightString(margin + 129 * mm, y, item["prod"].get("quantidadeComercial", ""))
    canvas_draw.drawRightString(margin + 139 * mm, y, formatar_moeda(item["prod"].get("valorUnitarioComercializacao", "")))
    canvas_draw.drawRightString(margin + 149 * mm, y, formatar_moeda(item["prod"].get("valorTotalBruto", "")))
    canvas_draw.drawRightString(margin + 159 * mm, y, formatar_moeda(item["imposto"]["icms"].get("vBc", "")))
    canvas_draw.drawRightString(margin + 169 * mm, y, formatar_moeda(item["imposto"]["icms"].get("vImp", "")))
    canvas_draw.drawRightString(margin + 179 * mm, y, formatar_moeda(item["imposto"]["ipi"].get("vImp", "")))
    canvas_draw.drawRightString(margin + 189 * mm, y, formatar_moeda(item["imposto"]["icms"].get("pImp", "")))
    canvas_draw.drawRightString(margin + 199 * mm, y, formatar_moeda(item["imposto"]["ipi"].get("pImp", "")))

    # Renderizar linhas tracejadas após a descrição completa
    canvas_draw.setDash(4, 1)
    canvas_draw.line(margin - 1 * mm, y - 1 * mm, 205 * mm, y - 1 * mm)
    canvas_draw.setDash()

    # Renderizar linhas verticais
    canvas_draw.line(margin - 1 * mm, 147 * mm, margin - 1 * mm, y - 1 * mm)
    canvas_draw.line(margin + 18 * mm, 147 * mm, margin + 18 * mm, y - 1 * mm)
    canvas_draw.line(margin + 80 * mm, 147 * mm, margin + 80 * mm, y - 1 * mm)
    canvas_draw.line(margin + 95 * mm, 147 * mm, margin + 95 * mm, y - 1 * mm)
    canvas_draw.line(margin + 105 * mm, 147 * mm, margin + 105 * mm, y - 1 * mm)
    canvas_draw.line(margin + 115 * mm, 147 * mm, margin + 115 * mm, y - 1 * mm)
    canvas_draw.line(margin + 120 * mm, 147 * mm, margin + 120 * mm, y - 1 * mm)
    canvas_draw.line(margin + 130 * mm, 147 * mm, margin + 130 * mm, y - 1 * mm)
    canvas_draw.line(margin + 140 * mm, 147 * mm, margin + 140 * mm, y - 1 * mm)
    canvas_draw.line(margin + 150 * mm, 147 * mm, margin + 150 * mm, y - 1 * mm)
    canvas_draw.line(margin + 160 * mm, 147 * mm, margin + 160 * mm, y - 1 * mm)
    canvas_draw.line(margin + 170 * mm, 147 * mm, margin + 170 * mm, y - 1 * mm)
    canvas_draw.line(margin + 180 * mm, 147 * mm, margin + 180 * mm, y - 1 * mm)
    canvas_draw.line(margin + 190 * mm, 147 * mm, margin + 190 * mm, y - 1 * mm)
    canvas_draw.line(205 * mm, 147 * mm, 205 * mm, y - 1 * mm)

    return y  # Retornar a nova coordenada y para o próximo item

def render_items(canvas_draw, items, width, height, margin, data):
    y                   = 147 * mm
    line_height         = 4 * mm
    numero_de_paginas   = 0
    current_items       = 0

    for i, item in enumerate(items):
        # Calcular a altura necessária para o item atual
        descricao = item["prod"].get("descricao", "")
        descricao_linhas = [descricao[j:j+47] for j in range(0, len(descricao), 47)]
        item_height = (len(descricao_linhas) - 1) * 4 * mm + line_height

        # Verificar se há espaço suficiente na página atual
        if y - item_height < 20 * mm:
            canvas_draw.showPage()  # Criar uma nova página
            numero_de_paginas += 1
            render_additional_page(canvas_draw, data, width, height, margin)
            y = 236 * mm  # Linha de referência da página adicional
            current_items = 0

        y -= line_height
        y = render_item_line(canvas_draw, item, y, margin)
        
        current_items += 1

    # Renderizar o restante dos itens
    remaining_items = items[i+1:]
    while remaining_items:
        canvas_draw.showPage()  # Criar uma nova página
        numero_de_paginas += 1
        render_additional_page(canvas_draw, data, width, height, margin)
        y = 236 * mm  # Linha de referência da página adicional
        current_items = 0
        for item in remaining_items:
            descricao = item["prod"].get("descricao", "")
            descricao_linhas = [descricao[j:j+47] for j in range(0, len(descricao), 47)]
            item_height = (len(descricao_linhas) - 1) * 4 * mm + line_height
            
            if y - item_height < 20 * mm:
                canvas_draw.showPage()
                render_additional_page(canvas_draw, data, width, height, margin)
                y = 236 * mm
                current_items = 0
            
            y -= line_height
            y = render_item_line(canvas_draw, item, y, margin)
            current_items += 1

        remaining_items = remaining_items[i+1:]