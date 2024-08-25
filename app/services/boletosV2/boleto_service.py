from reportlab.lib.colors import black
from reportlab.platypus import Flowable, Image

class CustomTable(Flowable):
    def __init__(self, data, col_widths, row_heights, xoffset=5, yoffset=5, fillcolor=None, strokecolor=black):
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
        return width, height

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

                if "image" in cell:
                    img: Image = cell["image"]
                    img_x = x + cell.get("image_x", 0)
                    img_y = y + cell.get("image_y", 0)
                    img.drawOn(canvas, img_x, img_y)

                if "title" in cell:
                    canvas.setFont(cell.get("title_font", "Helvetica-Bold"), cell.get("title_size", 6))
                    title_align = cell.get("title_align", "left")
                    title_padding_x = cell.get("title_padding_x", 4)
                    title_padding_y = cell.get("title_padding_y", 7)

                    if title_align == "center":
                        title_x = x + width / 2 - canvas.stringWidth(cell["title"]) / 2
                    elif title_align == "right":
                        title_x = x + width - canvas.stringWidth(cell["title"]) - title_padding_x
                    else:
                        title_x = x + title_padding_x

                    title_y = y + height - title_padding_y
                    canvas.drawString(title_x, title_y, str(cell["title"]))

                if "text" in cell:
                    canvas.setFont(cell.get("text_font", "Helvetica"), cell.get("text_size", 8))
                    text_align = cell.get("text_align", "left")
                    text_padding_x = cell.get("text_padding_x", 4)
                    text_padding_y = cell.get("text_padding_y", 5)

                    if text_align == "center":
                        text_x = x + width / 2 - canvas.stringWidth(cell["text"]) / 2
                    elif text_align == "right":
                        text_x = x + width - canvas.stringWidth(cell["text"]) - text_padding_x
                    else:
                        text_x = x + text_padding_x

                    text_y = y + text_padding_y
                    canvas.drawString(text_x, text_y, str(cell["text"]))

                x += width
