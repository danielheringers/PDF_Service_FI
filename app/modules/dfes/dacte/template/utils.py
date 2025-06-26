import base64
import os
from io import BytesIO
from typing import Optional

import qrcode
import qrcode.constants
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader


def generate_qrcode(data: Optional[str] = None) -> ImageReader:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2,
    )
    if not data:
        qr.add_data("https://www.cte.fazenda.gov.br/portal/")
        qr.make(fit=True)
    else:
        qr.add_data(data)
        qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)
    return ImageReader(buffer)

def generate_barcode(data: str) -> code128.Code128:
    barHeight = 8 * mm
    barWidth = 0.13 * mm
    barcode = code128.Code128(data, barHeight=barHeight, barWidth=barWidth)
    return barcode

def sem_logo() :
    logo_image = None
    logo_path = os.path.join(os.path.dirname(__file__), "../../../../assets/images/sem_logo.png")
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo file not found at {logo_path}")
    with open(logo_path, "rb") as logo_file:
        logo_image = ImageReader(logo_path)
    return logo_image

def generate_logo(logo: str) -> ImageReader:
    logo_image = None
    try:
        if logo:
            logo_data = base64.b64decode(logo)
            buffer = BytesIO(logo_data)
            buffer.seek(0)
            logo_image = ImageReader(buffer)
        else:
            logo_image = sem_logo()
    except:
        logo_image = sem_logo()

    return logo_image