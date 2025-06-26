from typing import Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


def ensure_list(values: dict, field_name: str) -> dict:
    """
    Se o campo existir e for um dict, transforma em lista de dicts.
    Se o campo for '', converte para None.
    """
    val = values.get(field_name)
    if val and isinstance(val, dict):
        values[field_name] = [val]
    elif val == '':
        values[field_name] = None
    return values

class InfMunCarrega(BaseModel):
    cMunCarrega: str = Field(..., description="Código IBGE do município de carregamentol")
    xMunCarrega: str = Field(..., description="Nome do município de carregamento")

class InfPercurso(BaseModel):
    UFPer: str = Field(..., description="UF intermediária percorrida no trajeto")

class Ide(BaseModel):
    cUF: str = Field(..., description="Código da UF do emitente do Documento Fiscal")
    tpEmit: str = Field(..., description="Tipo do emitente: 1 - Prestador / 2 - Carga Própria.")
    mod: str = Field(..., description="Código do Modelo do Documento Fiscal (58 para MDF-e)")
    serie: str = Field(..., description="Série do MDF-e (0 para série única).")
    nMDF: str = Field(..., description="Número do MDF-e.")
    cMDF: str = Field(..., description="Código numérico da Chave de Acesso do MDF-e")
    modal: str = Field(..., description="Modal (1 - Rodoviário, 2 - Aéreo, etc.)")
    dhEmi: str = Field(..., description="Data/hora de emissão no formato ISO com timezone")
    tpEmis: str = Field(..., description="Forma de emissão do MDF-e (1 - Normal, 2 - Contingência)")
    procEmi: str = Field(..., description="Código do processo de emissão do MDF-e")
    verProc: str = Field(..., description="Versão do processo de emissão do MDF-e")
    UFIni: str = Field(..., description="UF de Carregamento (ou EX para exterior)")
    UFFim: str = Field(..., description="UF de Descarregamento (ou EX para exterior)")
    infMunCarrega: Optional[InfMunCarrega] = Field(None, description="Município de início do percurso com carregamento")
    infPercurso: Optional[List[InfPercurso]] = Field(None, description="UF intermediárias do percurso")
    dhIniViagem: str = Field(..., description='Data/hora de início da viagem no formato ISO com timezone')

    @model_validator(mode='before')
    def ajustar_infPercurso(cls, values):
        return ensure_list(values, "infPercurso")

# Modo	        Quando Executa	                    Uso Principal
# before	    Antes da validação dos campos	    Pré-processar dados, ajustar tipos, preencher padrões
# after	        Após a validação dos campos	        Validações interdependentes, combinar campos
# wrap	        Envolve todo o processo	            Controle completo da validação, lógica complexa

class EnderEmit(BaseModel):
    xLgr: str = Field(..., description="Logradouro")
    nro: str = Field(..., description="Número do endereço")
    xCpl: Optional[str] = Field(None, description="Complemento do endereço")
    xBairro: str = Field(..., description="Bairro")
    cMun: str = Field(..., description="Código do município IBGE (7 dígitos)")
    xMun: str = Field(..., description="Nome do município")
    CEP: Optional[str] = Field(None, description="CEP")
    UF: str = Field(..., description="UF")
    fone: Optional[str] = Field(None, description="Telefone")
    email: Optional[str] = Field(None, description="E-mail")

class Emit(BaseModel):
    CNPJ: Optional[str] = Field(None, description="CNPJ do Emitente.")
    CPF: Optional[str] = Field(None, description="CPF do Emitente.")
    IE: str = Field(..., description="Inscrição Estadual do emitente.")
    xNome: str = Field(..., description="Razão Social do emitente.")
    xFant: str = Field(..., description="Nome Fantasia do emitente.")
    enderEmit: EnderEmit = Field(..., description="Endereço do emitente.")

class InfCIOT(BaseModel):
    CIOT: str = Field(..., description="Código Identificador da Operação de Transporte.")
    CPF: Optional[str] = Field(None, min_length=11, max_length=11, description='CPF do responsável pelo CIOT.')
    CNPJ: str = Field(..., min_length=14, max_length=14, description='CNPJ do responsável pela geração do CIOT.')

class Disp(BaseModel):
    CNPJForn: str = Field(..., description="CNPJ do Fornecedor do Vale-Pedágio")
    CNPJPg: Optional[str] = Field(None, description="CNPJ do responsável pelo pagamento do Vale Pedágio.")
    nCompra: str = Field(..., description="Número do comprovante de compra do Vale-Pedágio")
    vValePed: Optional[str] = Field(None, description="Valor do vale pedágio")
    tpValePed: Optional[str] = Field(None, description="Tipo de vale pedágio (01-TAG, 02-Cupom, 03-Cartão)")

class ValePed(BaseModel):
    disp: List[Disp] = Field(..., description="Dispositivos de Vale-Pedágio")
    categCombVeic: Optional[str] = Field(
        None,
        description="Categoria de Combinação Veicular"
    )

    @model_validator(mode='before')
    def ajustar_disp(cls, values):
        return ensure_list(values, "disp")

class InfContratante(BaseModel):
    xNome: Optional[str] = Field(None, min_length=2, max_length=60)
    CPF: Optional[str] = Field(None, min_length=11, max_length=11)
    CNPJ: Optional[str] = Field(None, min_length=14, max_length=14)
    idEstrangeiro: Optional[str] = Field(None, min_length=2, max_length=20)
    NroContrato: Optional[str] = Field(None, min_length=1, max_length=20)
    vContratoGlobal: Optional[float] = Field(None, description='Valor Global do Contrato')

class InfANTT(BaseModel):
    RNTRC: Optional[str] = Field(None, min_length=8, max_length=8)
    infCIOT: Optional[List[InfCIOT]] = Field(None, description="Informações do CIOT.")

    @model_validator(mode='before')
    def ajustar_infCIOT(cls, values):
        return ensure_list(values, "infCIOT")

    valePed: Optional[ValePed] = Field(None, description="Informações do Vale Pedágio.")
    infContratante: Optional[List[InfContratante]] = Field(None, description="Informações do contratante.")

    @model_validator(mode='before')
    def ajustar_infContratante(cls, values):
        return ensure_list(values, "infContratante")

    infPag: Optional[str] = Field(None, description="Informações de pagamento do serviço.")

class Condutor(BaseModel):
    xNome: Optional[str] = Field(None, min_length=1, max_length=60)
    CPF: Optional[str] = Field(None, min_length=11, max_length=11)

class VeicTracao(BaseModel):
    cInt: Optional[str] = Field(None, min_length=1, max_length=10)
    placa: str = Field(..., min_length=7, max_length=7)
    RENAVAM: Optional[str] = Field(None, min_length=9, max_length=11)
    tara: str = Field(..., min_length=1, max_length=6)
    capKG: Optional[str] = Field(None, min_length=1, max_length=6)
    capM3: Optional[str] = Field(None, min_length=1, max_length=3)
    condutor: Condutor
    tpRod: str = Field(..., min_length=2, max_length=2)
    tpCar: str = Field(..., min_length=2, max_length=2)
    UF: Optional[str] = Field(None, min_length=2, max_length=2)

class VeicReboque(BaseModel):
    cInt: Optional[str] = Field(None, min_length=1, max_length=10)
    placa: str = Field(..., min_length=7, max_length=7)
    RENAVAM: Optional[str] = Field(None, min_length=9, max_length=11)
    tara: str = Field(..., min_length=1, max_length=6)
    capKG: str = Field(..., min_length=1, max_length=6)
    capM3: Optional[str] = Field(None, min_length=1, max_length=3)
    tpCar: str = Field(..., min_length=2, max_length=2)
    UF: Optional[str] = Field(None, min_length=2, max_length=2)

class Rodo(BaseModel):
    infANTT: InfANTT
    veicTracao: VeicTracao
    veicReboque: Optional[List[VeicReboque]] = Field(None)

    @model_validator(mode='before')
    def ajustar_veicReboque(cls, values):
        return ensure_list(values, "veicReboque")

class InfModal(BaseModel):
    rodo: Rodo
    versaoModal: Optional[str] = Field(None, min_length=4, max_length=4)

class InfCTe(BaseModel):
    chCTe: str = Field(..., min_length=44, max_length=44)
    SegCodBarras: Optional[str] = Field(None, min_length=36, max_length=36)
    indReentrega_Opc: Optional[str] = Field(None, min_length=1, max_length=1)
    infUnidTransp_Grupo_Opc: Optional[str] = Field(None)
    peri_Grupo_Opc: Optional[str] = Field(None)
    infEntregaParcial_Opc: Optional[str] = Field(None)

class InfNFe(BaseModel):
    chNFe: str = Field(..., min_length=44, max_length=44)
    SegCodBarras: Optional[str] = Field(None, min_length=36, max_length=36)
    indReentrega_Opc: Optional[str] = Field(None, min_length=1, max_length=1)
    infUnidTransp_Grupo_Opc: Optional[str] = Field(None)
    peri_Grupo_Opc: Optional[str] = Field(None)

class InfMDFe(BaseModel):
    chMDFe: str = Field(..., min_length=44, max_length=44)
    indReentrega: Optional[str] = Field(None, min_length=1, max_length=1)
    infUnidTransp: Optional[str] = Field(None)
    peri: Optional[str] = Field(None)

class InfMunDescarga(BaseModel):
    cMunDescarga: str = Field(..., description="Código IBGE do município de descarregamento")
    xMunDescarga: str = Field(..., description="Nome do município de descarregamento")
    infCTe: Optional[List[InfCTe]] = Field(None)
    infNFe: Optional[List[InfNFe]] = Field(None)
    infMDFe: Optional[List[InfMDFe]] = Field(None)

    @model_validator(mode='before')
    def ajustar_inf_fields(cls, values):
        for campo in ["infCTe", "infNFe", "infMDFe"]:
            values = ensure_list(values, campo)
        return values


class InfDoc(BaseModel):
    infMunDescarga: Optional[List[InfMunDescarga]] = ''

    @model_validator(mode='before')
    def ajustar_infMunDescarga(cls, values):
        inf = values.get("infMunDescarga")
        if inf and isinstance(inf, dict):
            values["infMunDescarga"] = [inf]
        return values


class Tot(BaseModel):
    qNFe: Optional[str] = Field(None, min_length=1, max_length=4)
    qCTe: Optional[str] = Field(None, min_length=1, max_length=4)
    vCarga: str = Field(..., min_length=1, max_length=15)
    cUnid: Optional[str] = Field(None)
    qCarga: str = Field(..., min_length=1, max_length=15)

class InfAdic(BaseModel):
    infAdFisco: Optional[str] = Field(None, max_length=2000)
    infCpl: Optional[str] = Field(None, max_length=5000)

class InfMDFeSupl(BaseModel):
    qrCodMDFe: Optional[str] = Field(None, min_length=1, max_length=500)

class MDFe(BaseModel):
    versao: str
    branchId: str
    logo: Optional[str] = Field(None)
    ide: Ide
    emit: Emit
    infModal: InfModal
    infDoc: InfDoc
    tot: Tot
    infAdic: Optional[InfAdic] = None
    infMDFeSupl: Optional[InfMDFeSupl] = None

class ProtAttributes(BaseModel):
    versao: str = Field(..., min_length=1, max_length=5)

class InfProtAttributes(BaseModel):
    Id: str = Field(..., min_length=1, max_length=50)

class InfProt(BaseModel):
    attributes: InfProtAttributes
    tpAmb: str
    verAplic: str = Field(..., min_length=1, max_length=20)
    chMDFe: str = Field(..., min_length=44, max_length=44)
    dhRecbto: str
    nProt: str = Field(..., min_length=1, max_length=15)
    digVal: str = Field(..., min_length=1, max_length=28)
    cStat: str
    xMotivo: str = Field(..., min_length=1, max_length=255)

class ProtMDFe(BaseModel):
    attributes: ProtAttributes
    infProt: InfProt

class RetMDFe(BaseModel):
    attributes: Dict[str, str]
    tpAmb: str = Field(..., min_length=1, max_length=2)
    cUF: str = Field(..., min_length=2, max_length=2)
    verAplic: str = Field(..., min_length=1, max_length=20)
    cStat: str
    xMotivo: str = Field(..., min_length=1, max_length=255)
    protMDFe: Optional[ProtMDFe] = None

class DamdfePayload(BaseModel):
    MDFe: MDFe
    retMDFe: RetMDFe

    model_config = {
        "extra": "ignore"  # Ajuste conforme a necessidade (ignore, forbid, allow)
    }

# ignore: Campos extras são ignorados e descartados. O modelo processa apenas os campos definidos.
# forbid: Campos extras causam um erro de validação. Garante que apenas os campos esperados sejam fornecidos.
# allow: Campos extras são permitidos e armazenados no objeto. Eles não são validados pelo modelo.

# Como Escolher a Opção Adequada?
# 1. Quando usar ignore:

# Situação: Você está recebendo dados de fontes que podem incluir informações adicionais irrelevantes para o seu modelo.
# Vantagem: Evita erros de validação por causa de dados extras não necessários.
# Exemplo de uso: APIs públicas que recebem dados de várias fontes onde campos adicionais podem estar presentes, mas não são críticos para o processamento.
# 2. Quando usar forbid:

# Situação: Você quer garantir a integridade e a segurança dos dados, certificando-se de que somente os campos esperados sejam aceitos.
# Vantagem: Previne a entrada de dados não autorizados ou potencialmente maliciosos.
# Exemplo de uso: Processamento de dados sensíveis, como informações financeiras ou pessoais, onde a entrada deve ser rigorosamente controlada.
# 3. Quando usar allow:

# Situação: Você precisa manter todos os dados recebidos, inclusive os não previstos no modelo, possivelmente para armazenamento ou processamento posterior.
# Vantagem: Flexibilidade máxima para lidar com dados dinâmicos ou esquemas que podem variar.
# Exemplo de uso: Aplicações que funcionam como proxies ou registradores de dados, onde todas as informações devem ser preservadas.