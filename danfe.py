from datetime import datetime
import time
import json
import locale
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from io import BytesIO

from danfe_render_nfe import (
    render_first_page,
    render_items
)

start_time = time.time()
# Formatação Local BR
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        margin = 5 * mm
        if self._pageNumber == 1:
            self.setFont("Times-Italic", 8)
            self.drawCentredString(margin + 112.5 * mm, 241 * mm, f"FOLHA {self._pageNumber}/{page_count}")
        else:
            self.setFont("Times-Italic", 8)
            self.drawCentredString(margin + 112.5 * mm, 261 * mm, f"FOLHA {self._pageNumber}/{page_count}")


def create_pdf(data: dict):
    # Configurações Iniciais
    buffer = BytesIO()
    pdf_canvas = NumberedCanvas(buffer, pagesize=A4)
    width, height = A4
    margin = 5 * mm

    # Formatações
    data_emissao = datetime.fromisoformat(data["identificacao"]["dataHoraEmissao"])
    data_formatada = data_emissao.strftime("%d-%m-%Y")
    serie_formatada = data["identificacao"]["serie"].zfill(3)
    numero_nota = data["identificacao"]["numeroDocFiscal"].zfill(9)
    partes = [numero_nota[i:i+3] for i in range(0, len(numero_nota), 3)]
    numero_nota_formatado = '.'.join(partes)

    # Renderizar primeira página
    render_first_page(pdf_canvas, data, data_formatada, serie_formatada, numero_nota_formatado, width, height, margin)

    # Renderizar itens na primeira página e demais páginas se necessário
    render_items(pdf_canvas, data["det"], width, height, margin, data)

    pdf_canvas.save()
    buffer.seek(0)
    with open(f"danfecopy.pdf", "wb") as f:
        f.write(buffer.read())

    end_time = time.time()
    print(f"Tempo de execução: {end_time - start_time} segundos")   
    return buffer

if __name__ == "__main__":
    # Caminho para o arquivo JSON
    json_file_path = 'payload.json'
    # Carregar dados do arquivo JSON
    with open(json_file_path, 'r') as file:
        input_data = json.load(file)
    # Criar PDF com os dados carregados
    create_pdf(input_data)
