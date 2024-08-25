from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import black
from reportlab.platypus import SimpleDocTemplate
from io import BytesIO
from app.schemas.boleto.models import Boleto
from app.services.boletosV2.boleto_service import CustomTable
from reportlab.pdfgen import canvas
from app.utils.general_pdf_utils import formatar_cnpj_cpf, formatar_moeda_sem_cifrao, logo_bank_names
from app.utils.instructions import payment_instructions

def create_pdf_teste(data: Boleto) -> BytesIO:
    buffer = BytesIO()
    payment_place = "Pagável em qualquer Banco, Lotérica, Internet Banking e outros"
    instructions_text = "Instruções (instruções de responsabilidade do beneficiário. Qualquer dúvida sobre este boleto, contate o beneficiário)"
    
    img, bank_name, bank_code_digit, x_position, y_position = logo_bank_names(data)
    cpf_cnpj_beneficiario = formatar_cnpj_cpf(data.bank_account.document_number)

    main_table_data = [
        [
            {
                'image': img,
                'image_x': x_position,
                'image_y': y_position,
                'title': bank_name,
                'title_font': 'Helvetica-Bold',
                'title_size': 13,
                'title_align': 'left',
                'title_padding_x': 13.5 * mm,
                'title_padding_y': 9.5 * mm,
            },
            {
                'title': bank_code_digit,
                'title_font': 'Helvetica-Bold',
                'title_size': 14,
                'title_align': 'center',
                'title_padding_y': 9 * mm,
            },
            {
                'title': 'Recibo do Pagador',
                'title_font': 'Helvetica-Bold',
                'title_size': 9,
                'title_align': 'right',
                'title_padding_x': 2 * mm,
                'title_padding_y': 13 * mm,
            },
        ],
        [
            {'title': 'Local de Pagamento', 'text': payment_place},
            {'title': 'Vencimento', 'text': f'{data.billing.calendar.due_date}', 'text_align': 'right'},
        ],
        [
            {'title': 'Beneficiário', 'text': f'{data.bank_account.name} - {cpf_cnpj_beneficiario}'},
            {'title': 'Agência / Código Beneficiário', 'text': f'{data.bank_account.agency}/{data.bank_account.account_number}-{data.bank_account.account_digit}', 'text_align': 'right'},
        ],
        [
            {'title': 'Data do Documento', 'text': f'{data.billing.calendar.expedition_date}'},
            {'title': 'Número Documento', 'text': f'{data.billing.billing_internal_number}'},
            {'title': 'Espeçie Doc.', 'text': f'{data.billing.bank_slip_type}'},
            {'title': 'Aceite', 'text': f'{data.billing.buyer.knowledgment_of_debt}'},
            {'title': 'Data Processamento', 'text': f'{data.billing.calendar.expedition_date}'},
            {'title': 'Nosso Número', 'text': f'{data.billing.billing_provider_number}', 'text_align': 'right'},
        ],
        [
            {'title': 'Uso do Banco'},
            {'title': 'CIP'},
            {'title': 'Carteira', 'text': f'{data.bank_account.convenant_code}'},
            {'title': 'Esp. Moeda', 'text': f'Real'},
            {'title': 'Quantidade'},
            {'title': 'Valor'},
            {'title': '(=) Valor do Documento', 'text': f'{formatar_moeda_sem_cifrao(data.billing.total)}', 'text_align': 'right'},
        ],
    ]
    instructions_data = [[{'title': instructions_text}]]
    amount_details_data = [
        [{'title': '(-) Desconto / Abatimento'}],
        [{'title': '(-) Outras Deduções'}],
        [{'title': '(+) Mora / Multa'}],
        [{'title': '(+) Outros Acréscimos'}],
        [{'title': '(=) Valor Cobrado'}]
    ]

    main_table_col_widths = [
                    [50 * mm, 30 * mm, 115 * mm],
                    [150 * mm, 45 * mm],
                    [150 * mm, 45 * mm],
                    [30 * mm, 30 * mm, 25 * mm, 30 * mm, 35 * mm, 45 * mm],
                    [25 * mm, 15 * mm, 20 * mm, 25 * mm, 30 * mm, 35 * mm, 45 * mm]
                ]
    main_table_row_heights = [15 * mm, 10 * mm, 10 * mm, 10 * mm, 10 * mm]
    
    instructions_col_width = [[150 * mm]]
    instructions_row_heights = [50 * mm]
    
    amount_details_widths = [[45 * mm],[45 * mm],[45 * mm],[45 * mm],[45 * mm],]
    amount_details_heights = [10 * mm, 10 * mm, 10 * mm, 10 * mm, 10 * mm]

    table = CustomTable(main_table_data, main_table_col_widths, main_table_row_heights, fillcolor=None, strokecolor=black)
    instructions_table = CustomTable(instructions_data, instructions_col_width, instructions_row_heights,  fillcolor=None, strokecolor=black)
    amount_details_table = CustomTable(amount_details_data, amount_details_widths, amount_details_heights, xoffset=151.78 * mm, yoffset=50*mm, fillcolor=None, strokecolor=black)
    
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=5 * mm, rightMargin=5 * mm, topMargin=5 * mm, bottomMargin=5 * mm)
    elements = [table, instructions_table, amount_details_table]
    doc.build(elements)

    buffer.seek(0)
    return buffer
