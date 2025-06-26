import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.modules.charges.bankslip.schemas import Boleto, Billing
import pytest
from app.modules.charges.bankslip.schemas import (
    Boleto, Billing, Buyer, Address, Calendar, PaymentInfo, BankAccount
)

client = TestClient(app)

@pytest.fixture
def mock_boleto_payload():
    return [
        Boleto(
            billing=Billing(
                billing_internal_number="ABC123",
                payment_type=1,
                buyer=Buyer(
                    knowledgment_of_debt="Sim",
                    address=Address(
                        city="São Paulo",
                        complement="Apto 101",
                        neighborhood="Centro",
                        number="123",
                        phone="11999999999",
                        postal_code="01000-000",
                        state="SP",
                        street_name="Rua Exemplo",
                        email="comprador@example.com"
                    ),
                    cpf_cnpj="12345678901",
                    name="Empresa XYZ"
                ),
                bank_slip_type="simples",
                billing_id="456DEF",
                billing_provider_number="98765",
                calendar=Calendar(
                    due_date="2025-06-30",
                    expiration_date="2025-07-01",
                    expedition_date="2025-06-01"
                ),
                total="1000"
            ),
            payment_info=PaymentInfo(
                bar_code="12345678901234567890123456789012345678901234",
                digitable_line="12345.67890 12345.678901 23456.789012 3 45670000010000",
                qr_code_pix="00020101021226840014br.gov.bcb.pix0123examplepixkey5204000053039865802BR5925Empresa XYZ6009SAO PAULO62140510ABC1234567896304ABCD",
                qr_code_url="https://example.com/qrcode"
            ),
            bank_account=BankAccount(
                id="1",
                external_id="ext123",
                tenant_id="tenant123",
                name="Banco Exemplo",
                document_number="12345678000199",
                wallet_number="123",
                convenant_code=4567,
                agency="0001",
                account_number=123456,
                account_digit=7,
                bank="Banco XYZ",
                provider="Banco Provedor"
            ),
            bank_code="001",
            branch_name="Agência Central"
        )
    ]

@pytest.fixture
def mock_auth():
    with patch("app.api.auth_module.authorizer.Authorization.create") as mock_create:
        mock_instance = AsyncMock()
        mock_instance.validate.return_value = {"status": 200}
        mock_create.return_value = mock_instance
        yield mock_create

@pytest.fixture
def mock_pdf_generation():
    with patch("app.modules.charges.bankslip.service.create_pdf_boleto") as mock_create_pdf:
        mock_pdf = AsyncMock()
        mock_pdf.read.return_value = b"%PDF-1.4 Fake PDF content"
        mock_pdf.seek.return_value = None
        mock_create_pdf.return_value = mock_pdf
        yield mock_create_pdf

def test_create_bankslip_pdf_success(mock_boleto_payload, mock_auth, mock_pdf_generation):
    headers = {"tenantid": "test-tenant"}
    response = client.post("charges/boleto", json=[boleto.model_dump() for boleto in mock_boleto_payload], headers=headers)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert b"%PDF" in response.content  # Verifica se a resposta tem um PDF válido

def test_create_bankslip_pdf_missing_context(mock_boleto_payload, mock_auth):
    payload = {
        "body-json": [boleto.model_dump() for boleto in mock_boleto_payload],
        "api-gateway-params": {}  # Falta o contexto necessário
    }
    headers = {"tenantid": "test-tenant"}
    response = client.post("/charges/boleto", json=payload, headers=headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Missing context in API Gateway parameters"

def test_create_bankslip_pdf_unauthorized(mock_boleto_payload):
    with patch("app.api.auth_module.authorizer.Authorization.create") as mock_create:
        mock_instance = AsyncMock()
        mock_instance.validate.return_value = {"status": 401, "body": "Unauthorized"}
        mock_create.return_value = mock_instance

        payload = {
            "body-json": [boleto.model_dump() for boleto in mock_boleto_payload],
            "api-gateway-params": {"context": {"authorizations": {}}}
        }
        headers = {"tenantid": "test-tenant"}
        response = client.post("charges/boleto", json=payload, headers=headers)

        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized"
