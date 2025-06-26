# from typing import Dict, List, Any, Optional, Literal
from typing import Optional, Literal, List, Union
from pydantic import BaseModel, Field, model_validator, field_validator

from app.modules.dfes.schemas import Emit
from app.modules.dfes.schemas import Ender


def ensure_list(values: dict, field_name: str) -> dict:
    """
    Se o campo existir e for um dict, transforma em lista de dicts.
    Se o campo for '', converte para None.
    """
    val = values.get(field_name)
    if val and isinstance(val, dict):
        values[field_name] = [val]
    elif val == "":
        values[field_name] = None
    return values


class Xml(BaseModel):
    data: str = Field(..., description="XML do CTe.")


class Logo(BaseModel):
    logo_base64: Optional[str] = Field(None, description="Logo em base64.")

    @model_validator(mode="before")
    def check_logo_base64(cls, values):
        """
        Verifica se o logo_base64 é uma string vazia e converte para None.
        """
        return ensure_list(values, "logo_base64")


class InfNFe(BaseModel):
    chave: Optional[str] = Field(None, description="Chave de acesso do CTe.")


class InfDoc(BaseModel):
    infNFe: Optional[Union[InfNFe, List[InfNFe]]] = Field(
        None, description="Informações do documento."
    )

    @field_validator("infNFe")
    def ensure_list(cls, v):
        return v if isinstance(v, list) else [v]


class IdDocAntEle(BaseModel):
    chCTe: str = Field(..., description="Chave de acesso do CTe.")


class IdDocAnt(BaseModel):
    idDocAntEle: Optional[Union[IdDocAntEle, List[IdDocAntEle]]] = Field(
        None, description="Identificação do documento anterior."
    )

    @field_validator("idDocAntEle")
    def ensure_list(cls, v):
        return v if isinstance(v, list) else [v]


class EmiDocAnt(BaseModel):
    idDocAnt: Optional[IdDocAnt] = Field(
        None, description="Emitente do documento anterior."
    )


class DocAnt(BaseModel):
    emiDocAnt: Optional[EmiDocAnt] = Field(
        None, description="Emitente do documento anterior."
    )


class InfQ(BaseModel):
    cUnid: Optional[str] = Field(None, description="Código da unidade de medida.")
    qCarga: Optional[str] = Field(None, description="Quantidade da carga.")
    tpMed: Optional[str] = Field(None, description="Tipo de medida.")


class InfCarga(BaseModel):
    proPred: Optional[str] = Field(None, description="Produto ou serviço.")
    xOutCat: Optional[str] = Field(None, description="Descrição do produto ou serviço.")
    vCarga: Optional[str] = Field(None, description="Valor da carga.")
    infQ: Optional[Union[List[InfQ], InfQ]] = Field(None, description="Informações da carga.")

    @field_validator("infQ")
    def ensure_list(cls, v):
        return v if isinstance(v, list) else [v]


class InfCTeNorm(BaseModel):
    infModal: dict
    infDoc: Optional[InfDoc] = Field(None, description="Informações do documento.")
    docAnt: Optional[DocAnt] = Field(None, description="Documentos anteriores.")
    infCarga: InfCarga

class Toma(BaseModel):
    CNPJ: Optional[str] = Field(None, description="CNPJ do tomador.")
    CNPJ: Optional[str] = Field(None, description="CNPJ do tomador.")
    xNome: str
    xFant: Optional[str] = Field(None, description="Nome fantasia do tomador.")
    IE: Optional[str] = Field(None, description="Inscrição estadual do tomador.")
    fone: Optional[str] = Field(None, description="Telefone do tomador.")
    enderToma: Ender  

class Toma3(BaseModel):
    toma: Optional[str] = Field(None, description="Tomador do serviço.")
class Ide(BaseModel):
    tpCTe: Literal["0", "1", "2", "3"]
    tpServ: Literal["0", "1", "2", "3", "4"]
    mod: str
    serie: str
    nCT: str
    dhEmi: str
    CFOP: str
    natOp: str
    UFIni: Optional[str] = Field(None, description="UF de início da prestação do serviço.")
    xMunIni: Optional[str] = Field(None, description="Município de início da prestação do serviço.")
    UFFim: str
    xMunFim: str
    toma3: Optional[Toma3] = Field(
        None, description="Tomador do serviço (opcional)."
    )
    toma4: Optional[Toma] = Field(
        None, description="Tomador do serviço (opcional)."
    )


class Dest(BaseModel):
    CNPJ: str
    xNome: str
    IE: str
    fone: Optional[str] = Field(None, description="Telefone do destinatário.")
    ISUF: Optional[str] = Field(None, description="Inscrição SUF do destinatário.")
    enderDest: Ender


class Rem(BaseModel):
    CNPJ: str
    xNome: str
    fone: Optional[str] = Field(None, description="Telefone do remetente.")
    IE: str
    enderReme: Ender


class Exped(BaseModel):
    CNPJ: str
    xNome: str
    fone: Optional[str] = Field(None, description="Telefone do expedidor.")
    IE: str
    enderExped: Ender


class Receb(BaseModel):
    CNPJ: str
    xNome: str
    fone: Optional[str] = Field(None, description="Telefone do recebedor.")
    IE: str
    enderReceb: Ender


class ComData(BaseModel):
    dProg: Optional[str] = Field(None, description="Data programada para entrega.")


class EntregaModel(BaseModel):
    comData: Optional[ComData] = Field(None, description="Informações de entrega.")


class Compl(BaseModel):
    xObs: Optional[str] = Field(None, description="Observação do CTe.")
    Entrega: Optional[EntregaModel] = Field(None, description="Informações de entrega.")


class IcmsValue(BaseModel):
    CST: Optional[str] = Field(None, description="Valor da base de cálculo do ICMS.")
    vBC: Optional[str] = Field(None, description="Percentual do ICMS.")
    pICMS: Optional[str] = Field(None, description="Percentual do ICMS.")
    vICMS: Optional[str] = Field(None, description="Valor do ICMS.")

class Icms(BaseModel):
    ICMS00: Optional[IcmsValue] = Field(
        None, description="ICMS com tributação integral."
    )
    ICMS20: Optional[IcmsValue] = Field(
        None, description="ICMS com redução de base de cálculo."
    )
    ICMS45: Optional[IcmsValue] = Field(None, description="ICMS isento.")
    ICMS60: Optional[IcmsValue] = Field(
        None, description="ICMS cobrado anteriormente por substituição tributária."
    )
    ICMS90: Optional[IcmsValue] = Field(None, description="Outros tipos de ICMS.")
    ICMSOutraUF: Optional[IcmsValue] = Field(
        None, description="ICMS de outra unidade da federação."
    )

class Imp(BaseModel):
    ICMS: Icms
    infAdFisco: Optional[str] = Field(None, description="Informações adicionais de fiscalização.")

class CompInterface(BaseModel):
    xNome: Optional[str] = Field(None, description="Nome do Comp.")
    vComp: Optional[str] = Field(None, description="Valor do complemento.")


class VPrest(BaseModel):
    vTPrest: Optional[str] = Field(None, description="Valor total.")
    vRec: Optional[str] = Field(None, description="Valor total a receber.")
    Comp: Optional[Union[CompInterface, List[CompInterface]]] = Field(
        None, description="Complemento do valor."
    )

    @field_validator("Comp")
    def ensure_list(cls, v):
        return v if isinstance(v, list) else [v]
class InfCte(BaseModel):
    emit: Emit
    ide: Ide
    compl: Optional[Compl] = Field(
        None, description="Informações complementares do CTe."
    )
    infCTeNorm: Optional[InfCTeNorm] = Field(
        None, description="Informações do CTe normal."
    )
    dest: Optional[Dest] = Field(None, description="Destinatário do CTe.")
    rem: Optional[Rem] = Field(None, description="Remetente do CTe.")
    exped: Optional[Exped] = Field(None, description="Expedidor do CTe.")
    receb: Optional[Receb] = Field(None, description="Recebedor do CTe.")
    imp: Imp
    vPrest: Optional[VPrest] = Field(None, description="Valor.")
    toma: Optional[Toma] = Field(
        None, description="Tomador do serviço."
    )


class InfCTeSupl(BaseModel):
    qrCodCTe: Optional[str] = Field(None, description="QR Code do CTe.")


class CTe(BaseModel):
    infCte: InfCte
    infCTeSupl: Optional[InfCTeSupl] = Field(
        None, description="Informações adicionais do CTe."
    )


class InfProt(BaseModel):
    nProt: str
    chCTe: str
    dhRecbto: str
    tpAmb: str


class ProtCTe(BaseModel):
    infProt: InfProt


class CTeProc(BaseModel):
    CTe: CTe
    protCTe: ProtCTe


class CTeComplete(BaseModel):
    cteProc: CTeProc


class DactePayload(BaseModel):
    data: CTeComplete
    status: str
    logo_base64: Optional[str] = Field(None, description="Logo em base64.")

    model_config = {
        "extra": "ignore"  # Ajuste conforme a necessidade (ignore, forbid, allow)
    }


# Definições de Tipos de CTe
TIPOS_CTE = {
    "0": "CT-E NORMAL",
    "1": "CT-E COMPLEMENTAR",
    "2": "CT-E DE ANULAÇÃO",
    "3": "CT-E DE SUBSTITUIÇÃO",
}

# Definições de Tipos de Serviço
TIPOS_SERVICO = {
    "0": "NORMAL",
    "1": "SUBCONTRATAÇÃO",
    "2": "REDESPACHO",
    "3": "REDESPACHO INTERMEDIÁRIO",
    "4": "SERVIÇO VINCULADO A MULTIMODAL",
}

# Definições de Tipos de CST
TIPOS_CST = {
    "0": "00 - Tributada integralmente",
    "00": "00 - Tributada integralmente",
    "20": "20 - Com redução de base de cálculo",
    "40": "40 - Isenta",
    "41": "41 - Não tributada",
    "51": "51 - Suspensão",
    "60": "60 - ICMS cobrado anteriormente por substituição tributária",
    "90": "90 - Outros",
}
