from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel
 
#-------------------------------------------------------------------------#
#--------------------------Tipando em Python------------------------------#
#-------------------------------------------------------------------------#
# Padrões de Tipagem

# Caso o campo seja obrigatorio
# Campo: tipo

# Caso o campo seja opcional use o modelo abaixo
# Campo: Optional[List[Evento]]

# Caso o tipo seja opcional e você queira definir um valor substituto utilize o modelo abaixo, o valor none pode ser qualquer outro valor.
# Campo: Optional[List[Evento]] = none
#-------------------------------------------------------------------------#
#--------------------------        Fim      ------------------------------#
#-------------------------------------------------------------------------#

class Address(BaseModel):
    city: str
    complement: str
    email: str
    neighborhood: str
    number: int
    phone: str
    postal_code: str
    state: str
    street_name: str

class Buyer(BaseModel):
    knowledgment_of_debt: str
    address: Address
    cpf_cnpj: str
    name: str

class FixedDateDiscount(BaseModel):
    date: str
    value: float

class Discount(BaseModel):
    fixed_date: Optional[List[FixedDateDiscount]] = None
    value: Optional[float] = None
    modality: int

class Fine(BaseModel):
    modality: int
    value: float

class Interest(BaseModel):
    modality: int
    value: float

class AmountDetails(BaseModel):
    discount: Optional[Discount] = None
    fine: Optional[Fine] = None
    interest: Optional[Interest] = None

class Calendar(BaseModel):
    due_date: str
    expiration_date: str
    expedition_date: str

class Billing(BaseModel):
    billing_internal_number: str
    payment_type: int
    buyer: Buyer
    amount_details: Optional[AmountDetails] = None
    bank_slip_type: str
    billing_id: str
    billing_provider_number: str
    calendar: Calendar
    total: str
    messages: Optional[List[str]] = None

class PaymentInfo(BaseModel):
    bar_code: str
    digitable_line: str
    qr_code_pix: str
    qr_code_url: str

class ClientAccount(BaseModel):
    branch_id: str
    is_default: bool

class BankSlipConfig(BaseModel):
    bank_slip_type: Optional[str] = None
    days_valid_after_due: Optional[int] = None
    days_to_negative_report: Optional[int] = None
    days_to_protest: Optional[int] = None
    messages: Optional[str] = None
    amount_details: Optional[AmountDetails] = None
    bank_account_id: int
    send_email_to_buyers: Optional[bool] = None

class ShipayCredential(BaseModel):
    bank_account_id: int
    shipay_client_id: str

class BankAccount(BaseModel):
    id: int
    external_id: str
    tenant_id: str
    name: str
    document_number: str
    wallet_number: Optional[str]
    convenant_code: int
    agency: str
    account_number: int
    account_digit: int
    pix_dict_key: str
    pix_dict_key_type: str
    bank: str
    provider: str
    created_by: str
    created_at: str
    updated_by: Optional[str]
    updated_at: str
    client_accounts: List[ClientAccount]
    bank_slip_config: Optional[BankSlipConfig] = None
    shipay_credential: ShipayCredential

class Boleto(BaseModel):
    billing: Billing
    erp_id: str
    payment_info: PaymentInfo
    bank_account: BankAccount
    bank_code: str