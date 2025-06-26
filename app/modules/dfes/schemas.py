from typing import Optional
from pydantic import BaseModel, Field

class Ender(BaseModel):
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
    xPais: Optional[str] = Field(None, description="Nome do país")

class Emit(BaseModel):
    CNPJ: Optional[str] = Field(None, description="CNPJ do Emitente.")
    CPF: Optional[str] = Field(None, description="CPF do Emitente.")
    IE: str = Field(..., description="Inscrição Estadual do emitente.")
    xNome: str = Field(..., description="Razão Social do emitente.")
    xFant: str = Field(..., description="Nome Fantasia do emitente.")
    enderEmit: Ender = Field(..., description="Endereço do emitente.")