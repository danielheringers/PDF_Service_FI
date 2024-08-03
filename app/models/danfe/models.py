from __future__ import annotations
from typing import Any, List, Optional
from pydantic import BaseModel
 
 
class Identificacao(BaseModel):
    codigoUf: str
    codigoNf: str
    tpNf: str
    naturezaOperacao: str
    serie: str
    numeroDocFiscal: str
    dataHoraEmissao: str
    dataHoraSaidaOuEntrada: str
    idLocalDestino: str
    codigoMunicipioFg: str
    formatoNfe: str
    finalidade: str
    indFinal: str
    indPres: str
    indIntermed: str
 
 
class Endereco(BaseModel):
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    codigoMunicipio: str
    uf: str
    cep: str
    codigoPais: str
    fone: str
    ie: str
 
 
class Destinatario(BaseModel):
    cnpj: str
    nome: str
    endereco: Endereco
    indIeDestinatario: str
    ie: str
 
 
class Endereco1(BaseModel):
    logradouro: str
    numero: str
    bairro: str
    codigoMunicipio: str
    municipio: str
    uf: str
    cep: str
    codigoPais: str
    pais: str
    fone: str
    complemento: Any
 
 
class Emitente(BaseModel):
    endereco: Endereco1
    nome: str
    nomeFantasia: str
    inscricaoEstadual: str
    codigoRegimeTributario: str
    cnpj: str
    inscricaoMunicipal: str
 
 
class Prod(BaseModel):
    codigo: str
    cean: str
    descricao: str
    ncm: str
    cest: str
    cBenef: str
    codigoFiscalOperacoes: str
    unidadeComercial: str
    quantidadeComercial: str
    valorUnitarioComercializacao: str
    valorTotalBruto: str
    ceanTrib: str
    unidadeTributavel: str
    quantidadeTributavel: str
    valorUnitarioTributacao: str
    valorFrete: str
    indTot: str
    di: List
 
 
class Icms(BaseModel):
    orig: str
    cst: str
    modBc: str
    vBc: str
    pImp: str
    vImp: str
 
 
class Pis(BaseModel):
    cst: str
    vBc: str
    pPis: str
    vPis: str
 
 
class Cofins(BaseModel):
    cst: str
    vBc: str
    pImp: str
    vImp: str
 
 
class Ipi(BaseModel):
    cEnq: str
    cst: str
    vBc: str
    pImp: str
    vImp: str
 
 
class Imposto(BaseModel):
    icms: Icms
    pis: Pis
    cofins: Cofins
    ipi: Ipi
 
 
class DetItem(BaseModel):
    nItem: str
    prod: Prod
    imposto: Imposto
 
 
class Transp(BaseModel):
    modFrete: str
    transporta: Transporta
    veicTransp: VeicTransp
    vol: Volume

class Transporta(BaseModel):
    nome: str
    cnpj: str
    inscricaoEstadual: str
    enderecoCompleto: str
    nomeMunicipio: str
    uf: str

class VeicTransp(BaseModel):
    placa: str
    uf: str
    veic: Veic

class Veic(BaseModel):
    rntc: str

class Volume(BaseModel):
    quantidade: str
    especie: str
    pesoLiquido: str
    pesoBruto: str
    marca: str
    nVol: str
 
class DetPagItem(BaseModel):
    indPag: str
    tPag: str
    vPag: str
 
 
class Pag(BaseModel):
    detPag: List[DetPagItem]
 
 
class IcmsTot(BaseModel):
    vBc: str
    vIcms: str
    vIcmsDeson: str
    vFcpUfDest: str
    vIcmsUfDest: str
    vIcmsUfRemet: str
    vFcp: str
    vBcSt: str
    vSt: str
    vFcpSt: str
    vFcpStRet: str
    vProd: str
    vFrete: str
    vSeg: str
    vDesc: str
    vIi: str
    vIpi: str
    vIpiDevol: str
    vPis: str
    vCofins: str
    vOutro: str
    vNf: str
 
 
class Total(BaseModel):
    icmsTot: IcmsTot
 
class Danfe(BaseModel):
    identificacao: Identificacao
    destinatario: Destinatario
    emitente: Emitente
    det: List[DetItem]
    transp: Transp
    pag: Pag
    total: Total
    emails: List
    dadosCobranca: str
    tipoOperacao: str
    tenantid: str
    key: str