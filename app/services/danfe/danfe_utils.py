# from datetime import datetime
# import locale
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import mm
# from io import BytesIO
# from app.services.danfe.danfe_render_nfe import render_first_page, render_items
# from app.schemas.danfe.models import Danfe
# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# class NumberedCanvas(canvas.Canvas):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._saved_page_states = []

#     def showPage(self):
#         self._saved_page_states.append(dict(self.__dict__))
#         self._startPage()

#     def save(self):
#         num_pages = len(self._saved_page_states)
#         for state in self._saved_page_states:
#             self.__dict__.update(state)
#             self.draw_page_number(num_pages)
#             super().showPage()
#         super().save()

#     def draw_page_number(self, page_count):
#         margin = 5 * mm
#         self.setFont("Times-Italic", 8)
#         if self._pageNumber == 1:
#             self.drawCentredString(margin + 112.5 * mm, 241 * mm, f"FOLHA {self._pageNumber}/{page_count}")
#         else:
#             self.drawCentredString(margin + 112.5 * mm, 261 * mm, f"FOLHA {self._pageNumber}/{page_count}")

# def create_pdf_danfe(data: Danfe) -> BytesIO:
#     buffer = BytesIO()
#     pdf_canvas = NumberedCanvas(buffer, pagesize=A4)
#     width, height = A4
#     margin = 5 * mm

#     data_emissao = datetime.fromisoformat(data.identificacao.dataHoraEmissao)
#     data_formatada = data_emissao.strftime("%d-%m-%Y")
#     serie_formatada = data.identificacao.serie.zfill(3)
#     numero_nota = data.identificacao.numeroDocFiscal.zfill(9)
#     partes = [numero_nota[i:i+3] for i in range(0, len(numero_nota), 3)]
#     numero_nota_formatado = '.'.join(partes)

#     render_first_page(pdf_canvas, data, data_formatada, serie_formatada, numero_nota_formatado, width, height, margin)
#     render_items(pdf_canvas, data.det, width, height, margin, data)

#     pdf_canvas.showPage() 
#     pdf_canvas.save()     
#     buffer.seek(0)
    
#     with open("output_test.pdf", "wb") as f:
#         f.write(buffer.getbuffer())
    
#     return buffer