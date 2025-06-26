import json
import random
import string
from datetime import datetime, timedelta, timezone
from locust import HttpUser, task, between

def random_billing_id():
    # Gera uma string no formato UUID simplificado
    return (
        ''.join(random.choices('abcdef' + string.digits, k=8)) + '-' +
        ''.join(random.choices('abcdef' + string.digits, k=4)) + '-' +
        ''.join(random.choices('abcdef' + string.digits, k=4)) + '-' +
        ''.join(random.choices('abcdef' + string.digits, k=4)) + '-' +
        ''.join(random.choices('abcdef' + string.digits, k=12))
    )

def random_date(start, end):
    """Retorna uma data aleatória entre start e end, formatada como DD/MM/YYYY."""
    delta = end - start
    random_days = random.randrange(delta.days + 1)
    return (start + timedelta(days=random_days)).strftime("%d/%m/%Y")

def generate_dynamic_payload():
    today = datetime.today()
    # Datas aleatórias para as datas do calendário
    due_date = random_date(today, today + timedelta(days=365))
    expiration_date = random_date(today, today + timedelta(days=365))
    expedition_date = random_date(today - timedelta(days=365), today)
    
    payload = [
        {
            "billing": {
                "amount_details": {
                    "discount": None,
                    "fine": {
                        "modality": 1,
                        "value": round(random.uniform(0.5, 5.0), 2)
                    },
                    "interest": {
                        "modality": 3,
                        "value": round(random.uniform(1.0, 10.0), 2)
                    },
                    "rebate": None
                },
                "billing_internal_number": str(random.randint(1, 100)),
                "payment_type": random.choice([1, 2, 3]),
                "buyer": {
                    "knowledgment_of_debt": random.choice(["S", "N"]),
                    "address": {
                        "city": random.choice(["Belo horizonte", "São Paulo", "Rio de Janeiro"]),
                        "complement": "Não informado",
                        "neighborhood": ''.join(random.choices(string.ascii_uppercase, k=10)),
                        "number": random.randint(1, 500),
                        "phone": ''.join(random.choices(string.digits, k=10)),
                        "postal_code": f"{random.randint(10000,99999)}-{random.randint(100,999)}",
                        "state": random.choice(["MG", "SP", "RJ"]),
                        "street_name": random.choice(["Rua Ulhoa Cintra", "Avenida Paulista", "Rua das Flores"])
                    },
                    "cpf_cnpj": ''.join(random.choices(string.digits, k=11)),
                    "name": random.choice(["Selton melo", "Maria Silva", "João Souza"])
                },
                "bank_slip_type": random.choice(["DV", "NN"]),
                "billing_id": random_billing_id(),
                "billing_provider_number": str(random.randint(10000, 99999)),
                "calendar": {
                    "due_date": due_date,
                    "expiration_date": expiration_date,
                    "expedition_date": expedition_date
                },
                "total": f"{round(random.uniform(100.0, 5000.0), 2)}".replace('.', ','),
                "messages": []
            },
            "erp_id": str(random.randint(1, 100)),
            "payment_info": {
                "bar_code": ''.join(random.choices(string.digits, k=44)),
                "digitable_line": ''.join(random.choices(string.digits, k=47)),
                "qr_code_pix": "fake_qr_code_pix_data",
                "qr_code_url": "data:image/png;base64,FAKE_BASE64_DATA"
            },
            "bank_account": {
                # "id": random.randint(1, 10),
                # "external_id": random_billing_id(),
                "tenant_id": ''.join(random.choices(string.ascii_lowercase + string.digits, k=36)),
                "name": random.choice(["Seidor", "Banco X"]),
                "document_number": ''.join(random.choices(string.digits, k=14)),
                "wallet_number": None,
                "convenant_code": random.randint(100, 999),
                "agency": ''.join(random.choices(string.digits, k=4)) + "-" + str(random.randint(0,9)),
                "account_number": random.randint(1000, 9999),
                "account_digit": random.randint(0, 9),
                "pix_dict_key": ''.join(random.choices(string.digits, k=14)),
                "pix_dict_key_type": random.choice(["evp", "cpf"]),
                "bank": random.choice(["001", "237"]),
                # "provider": random.choice(["shipay", "other"]),
                "created_by": "test@example.com",
                "created_at": datetime.now(timezone.utc).isoformat() + "Z",
                "updated_by": None,
                "updated_at": datetime.now(timezone.utc).isoformat() + "Z",
                "client_accounts": [],
                "bank_slip_config": None
            },
            "bank_code": "001-9"
        }
    ]
    return payload

class BoletoUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def generate_boleto_pdf(self):
        payload = generate_dynamic_payload()
        headers = {
            "tenantid": "seu_tenant_id",  # ajuste conforme necessário
            "Content-Type": "application/json"
        }
        self.client.post("/charges/boleto", json=payload, headers=headers)
