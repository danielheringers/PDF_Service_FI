from reportlab.lib.colors import black
from reportlab.platypus import Flowable, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.colors import black, white
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

class CustomTextTable(Flowable):
    def __init__(self, title, texts, col_width, row_height, text_line_height, xoffset=5, yoffset=0, 
                 fillcolor=None, strokecolor=black, title_font="Helvetica-Bold", title_size=12, 
                 title_align="left", title_padding_x=5, title_padding_y=5,
                 text_font="Helvetica", text_size=10, text_align="left", text_padding_x=5, text_padding_y=5):
        self.title = title
        self.texts = texts
        self.col_width = col_width
        self.row_height = row_height
        self.text_line_height = text_line_height
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.fillcolor = fillcolor
        self.strokecolor = strokecolor
        self.title_font = title_font
        self.title_size = title_size
        self.title_align = title_align
        self.title_padding_x = title_padding_x
        self.title_padding_y = title_padding_y
        self.text_font = text_font
        self.text_size = text_size
        self.text_align = text_align
        self.text_padding_x = text_padding_x
        self.text_padding_y = text_padding_y

    def wrap(self, *args):
        width = self.col_width
        height = self.row_height + len(self.texts) * self.text_line_height
        return width, height

    def draw(self):
        canvas = self.canv
        canvas.setStrokeColor(self.strokecolor)
        canvas.setLineWidth(1)

        y = self.yoffset + self.row_height + len(self.texts) * self.text_line_height
        x = self.xoffset

        if self.fillcolor:
            canvas.setFillColor(self.fillcolor)
            canvas.rect(x, y - self.row_height, self.col_width, self.row_height, stroke=0, fill=1)

        canvas.setFillColor(self.strokecolor)
        canvas.setFont(self.title_font, self.title_size)

        if self.title_align == "center":
            title_x = x + self.col_width / 2 - canvas.stringWidth(self.title) / 2
        elif self.title_align == "right":
            title_x = x + self.col_width - canvas.stringWidth(self.title) - self.title_padding_x
        else:
            title_x = x + self.title_padding_x

        title_y = y - self.row_height + self.title_padding_y
        canvas.drawString(title_x, title_y, self.title)

        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleN.fontName = self.text_font
        styleN.fontSize = self.text_size
        styleN.leading = self.text_line_height

        y -= self.row_height

        for text in self.texts:
            y -= self.text_line_height
            paragraph = Paragraph(text, styleN)
            width, height = paragraph.wrap(self.col_width - 2 * self.text_padding_x, self.text_line_height)
            text_x = x + self.text_padding_x

            if self.text_align == "center":
                text_x = x + (self.col_width - width) / 2
            elif self.text_align == "right":
                text_x = x + self.col_width - width - self.text_padding_x
            
            text_y = y + self.text_padding_y
            paragraph.drawOn(canvas, text_x, text_y)

        canvas.rect(x, y, self.col_width, self.row_height + len(self.texts) * self.text_line_height, stroke=1, fill=0)



class CustomMixedColumnTable(Flowable):
    def __init__(self, col1_title, col1_texts, col2_data, col1_width, col1_height, col2_widths, col2_heights, 
                 xoffset=5, yoffset=0, fillcolor=None, strokecolor=black, 
                 title_font="Helvetica-Bold", title_size=12, title_padding_y=2.5*mm,
                 text_font="Helvetica", text_size=10, text_line_spacing=3.7*mm):
        self.col1_title = col1_title
        self.col1_texts = col1_texts
        self.col2_data = col2_data
        self.col1_width = col1_width
        self.col1_height = col1_height
        self.col2_widths = col2_widths
        self.col2_heights = col2_heights
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.fillcolor = fillcolor
        self.strokecolor = strokecolor
        self.title_font = title_font
        self.title_size = title_size
        self.title_padding_y = title_padding_y
        self.text_font = text_font
        self.text_size = text_size
        self.text_line_spacing = text_line_spacing

    def wrap(self, *args):
        width = self.col1_width + sum(self.col2_widths)
        height = max(self.col1_height, sum(self.col2_heights))
        return width, height

    def draw(self):
        canvas = self.canv
        canvas.setStrokeColor(self.strokecolor)
        canvas.setLineWidth(1)

        x = self.xoffset
        y = self.yoffset + self.col1_height
        if self.fillcolor:
            canvas.setFillColor(self.fillcolor)
            canvas.rect(x, y - self.col1_height, self.col1_width, self.col1_height, stroke=1, fill=1)
        
        canvas.setFillColor(white)
        canvas.rect(x, y - self.col1_height, self.col1_width, self.col1_height, stroke=1, fill=0)

        canvas.setFillColor(self.strokecolor)
        canvas.setFont(self.title_font, self.title_size)

        title_x = x + 5
        title_y = y - 7
        canvas.drawString(title_x, title_y, self.col1_title)

        text_y = title_y - self.title_size - self.title_padding_y
        canvas.setFont(self.text_font, self.text_size)

        for text in self.col1_texts:
            text_y -= self.text_line_spacing
            canvas.drawString(title_x, text_y, text)

        x += self.col1_width
        y = self.yoffset + sum(self.col2_heights) + self.col1_height
        
        for idx, text in enumerate(self.col2_data):
            height = self.col2_heights[idx]
            width = self.col2_widths[idx]
            
            if idx == 0:
                y -= self.col1_height
            
            canvas.setFillColor(self.fillcolor or white)
            canvas.rect(x, y - height, width, height, stroke=1, fill=1)

            canvas.setFillColor(self.strokecolor)
            canvas.setFont(self.text_font, 10)
            canvas.drawString(x + 5, y - height + 5, text)

            y -= height