
from reportlab.lib.units import mm
from reportlab.lib.colors import Color

from app.modules.dfes.dacte.schemas import DactePayload
from app.utils.utils import safe_getattr

def add_watermark(canvas_obj, data: DactePayload):
    # Adiciona a marca d'água
    cteProc = safe_getattr(data.data, "cteProc")
    protCTe = safe_getattr(cteProc, "protCTe")
    infProt = safe_getattr(protCTe, "infProt")
    tpAmb = safe_getattr(infProt, "tpAmb")
    
    if tpAmb == "2":
        canvas_obj.setFont("Helvetica-Bold", 30)
        canvas_obj.setFillColor(Color(0.6, 0.6, 0.6, alpha=0.4))
        canvas_obj.drawCentredString(100 * mm, 200 * mm, "CT-e EMITIDO EM AMBIENTE") 
        canvas_obj.drawCentredString(100 * mm, 180 * mm, "DE HOMOLOGAÇÃO")