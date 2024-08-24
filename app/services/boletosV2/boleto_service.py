from reportlab.lib.colors import black
from reportlab.platypus import Flowable

class CustomTable(Flowable):
    def __init__(self, data, col_widths, row_heights, xoffset=5, yoffset=0, fillcolor=None, strokecolor=black):
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

        y = self.yoffset + sum(self.row_heights)

        for row_idx, row in enumerate(self.data):
            y -= self.row_heights[row_idx]
            x = self.xoffset
            
            col_widths = self.col_widths[row_idx]
            
            for col_idx, cell in enumerate(row):
                width = col_widths[col_idx]
                height = self.row_heights[row_idx]
                
                if self.fillcolor:
                    canvas.setFillColor(self.fillcolor)
                    canvas.rect(x, y, width, height, stroke=0, fill=1)
                
                canvas.setFillColor(self.strokecolor)
                canvas.rect(x, y, width, height, stroke=1, fill=0)

                if cell:

                    if 'title' in cell:
                        canvas.setFont(cell.get('title_font', 'Helvetica-Bold'), cell.get('title_size', 10))
                        title_x = x + cell.get('title_padding_x', 2)
                        title_y = y + height - cell.get('title_padding_y', 4)
                        canvas.drawString(title_x, title_y, str(cell['title']))
                        
                    if 'text' in cell:
                        canvas.setFont(cell.get('text_font', 'Helvetica'), cell.get('text_size', 8))
                        
                        if cell.get('text_align', 'left') == 'center':
                            text_x = x + width / 2 - canvas.stringWidth(cell['text']) / 2
                        elif cell.get('text_align') == 'right':
                            text_x = x + width - canvas.stringWidth(cell['text']) - cell.get('text_padding_x', 2)
                        else:
                            text_x = x + cell.get('text_padding_x', 2)
                        
                        text_y = y + cell.get('text_padding_y', 4)
                        canvas.drawString(text_x, text_y, str(cell['text']))

                x += width
