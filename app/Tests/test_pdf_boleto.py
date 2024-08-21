import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.Models.Boleto.models import Boleto, Billing, PaymentInfo, BankAccount, Buyer, Calendar, Address

client = TestClient(app)

def test_generate_pdf():
    boleto_data = {
        "billing": {
            "billing_internal_number": "125125",
            "payment_type": 1,
            "buyer": {
                "knowledgment_of_debt": "Sim",
                "address": {
                    "city": "Belo Horizonte",
                    "complement": "Apto 101",
                    "email": "buyer@example.com",
                    "neighborhood": "Centro",
                    "number": "123",
                    "phone": "31999999999",
                    "postal_code": "30100-000",
                    "state": "MG",
                    "street_name": "Rua Exemplo"
                },
                "cpf_cnpj": "12345678900",
                "name": "João da Silva"
            },
            "amount_details": {
                "discount": {
                    "value": 1.54,
                    "modality": 5
                },
                "fine": {
                    "modality": 1,
                    "value": 1
                },
                "interest": {
                    "modality": 1,
                    "value": 1
                },
                "rebate": {
                    "modality": 1,
                    "value": 2
                }
            },
            "bank_slip_type": "A4",
            "billing_id": "abc123",
            "billing_provider_number": "1000",
            "calendar": {
                "due_date": "2024-08-30",
                "expiration_date": "2024-09-10",
                "expedition_date": "2024-08-15"
            },
            "total": 1500.00,
            "messages": ["Pagamento à vista", "Não aceitar após vencimento"]
        },
        "erp_id": "ERP123456",
        "payment_info": {
            "bar_code": "12345678901234567890123456789012345678901234",
            "digitable_line": "12345.67890 12345.678901 23456.789012 3 45670000015000",
            "qr_code_pix": "00020126360014BR.GOV.BCB.PIX0114+55619999999990204abcd52040000530398654071500.005802BR5925Joao da Silva6009BRASILIA62070503***63040F17",
            "qr_code_url": "https://example.com/qrcode"
        },
        "bank_account": {
            "id": 1,
            "external_id": "EXT123456",
            "tenant_id": "TNT123",
            "name": "Razão Social Exemplo",
            "document_number": "12345678000195",
            "wallet_number": "19",
            "convenant_code": 123456,
            "agency": "1234",
            "account_number": 56789,
            "account_digit": 0,
            "pix_dict_key": "abc123def456ghi789",
            "pix_dict_key_type": "EMAIL",
            "bank": "341",
            "provider": "Banco Itaú S.A.",
            "created_by": "admin",
            "created_at": "2024-08-20",
            "updated_by": "admin",
            "updated_at": "2024-08-21",
            "client_accounts": [],
            "bank_slip_config": None,
            "shipay_credential": {
                "bank_account_id": 1,
                "shipay_client_id": "SHIPAY123"
            }
        },
        "bank_code": "341-7"
    }
    
    headers = {
        "tenantid": "Teste",
        "username": "testuser",
        "useremail": "testuser@example.com"
    }
    
    response = client.post("/gerar/pdf/boleto", json=boleto_data, headers=headers)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

    with open("test_boleto.pdf", "wb") as f:
        f.write(response.content)


@pytest.mark.parametrize("invalid_data, expected_error_property", [
    # Teste 1: Omitir 'billing'
    ({"erp_id": "ERP123456", "payment_info": {"bar_code": "12345678901234567890123456789012345678901234"}, "bank_account": {"id": 1}, "bank_code": "001"}, "billing"),
    
    # Teste 2: Omitir 'payment_info'
    ({"billing": {"billing_internal_number": "12345"}, "erp_id": "ERP123456", "bank_account": {"id": 1}, "bank_code": "001"}, "payment_info"),
    
    # Teste 3: Omitir 'erp_id'
    ({"billing": {"billing_internal_number": "12345"}, "payment_info": {"bar_code": "12345678901234567890123456789012345678901234"}, "bank_account": {"id": 1}, "bank_code": "001"}, "erp_id"),
    
    # Teste 4: Campo 'billing_internal_number' com tipo incorreto
    ({"billing": {"billing_internal_number": 12345}, "erp_id": "ERP123456", "payment_info": {"bar_code": "12345678901234567890123456789012345678901234"}, "bank_account": {"id": 1}, "bank_code": "001"}, "billing.billing_internal_number"),
    
])
def test_invalid_payloads(invalid_data, expected_error_property):
    headers = {
        "tenantid": "Teste",
        "username": "testuser",
        "useremail": "testuser@example.com"
    }

    response = client.post("/gerar/pdf/boleto", json=invalid_data, headers=headers)

    assert response.status_code == 422
    
    error_details = response.json().get('errors', [])
    assert len(error_details) > 0, f"No validation errors found in response for {expected_error_property}"

    assert any(expected_error_property == error.get('property_errors', [{}])[0].get('property') for error in error_details), f"{expected_error_property} not found in error details"
