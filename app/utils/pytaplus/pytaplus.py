from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, lightgrey
from reportlab.platypus import SimpleDocTemplate, Flowable
from reportlab.lib.units import mm
from reportlab.lib import colors

def create_pdf_teste():
    class CustomTable(Flowable):
        def __init__(self, data, col_widths, row_heights, xoffset= 5, yoffset=0, fillcolor=None, strokecolor=black):
            self.data = data
            self.col_widths = col_widths
            self.row_heights = row_heights
            self.xoffset = xoffset
            self.yoffset = yoffset
            self.fillcolor = fillcolor
            self.strokecolor = strokecolor

        def wrap(self, *args):
            width = max(sum(row) for row in self.col_widths)
            height = sum(self.row_heights)
            return (width, height)
        
        def draw(self):
            canvas = self.canv
            canvas.setStrokeColor(self.strokecolor)
            canvas.setLineWidth(1)

            y = self.yoffset + sum(self.row_heights)  # Start from the top

            for row_idx, row in enumerate(self.data):
                y -= self.row_heights[row_idx]  # Move to the correct row
                x = self.xoffset  # Reset to the starting x position
                
                col_widths = self.col_widths[row_idx]  # Get column widths for this row
                
                for col_idx, cell in enumerate(row):
                    width = col_widths[col_idx]
                    height = self.row_heights[row_idx]
                    
                    # Draw cell background if specified
                    if self.fillcolor:
                        canvas.setFillColor(self.fillcolor)
                        canvas.rect(x, y, width, height, stroke=0, fill=1)
                    
                    # Draw cell border
                    canvas.setFillColor(self.strokecolor)
                    canvas.rect(x, y, width, height, stroke=1, fill=0)

                    # Draw the text inside the cell
                    if cell:
                        canvas.setFont("Helvetica", 10)
                        text_x = x + 2  # Slight padding from the left
                        text_y = y + height - 10 
                        canvas.drawString(text_x, text_y, str(cell))

                    x += width


    data = [
        ['Header 1', 'Header 2', 'Header 3'],
        ['Row 2, Col 1', 'Row 2, Col 2'],
        ['Row 3, Col 1', 'Row 3, Col 2', 'Row 3, Col 3'],
    ]

    col_widths = [
        [100, 100, 100],
        [150, 150],
        [80, 120, 100]
    ]

    row_heights = [20, 30, 20]  # Alturas para as 3 linhas

    table = CustomTable(data, col_widths, row_heights)

    # Criação do buffer para o PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=5*mm, rightMargin=5*mm,
                            topMargin=5*mm, bottomMargin=5*mm)
    elements = [table]
    doc.build(elements)

    buffer.seek(0)
    return buffer
