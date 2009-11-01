from huBarcode.code128 import Code128Encoder, Code128Renderer
from StringIO import StringIO

from django.http import HttpResponse

def _generate_barcode(val, scale):
    "Generate a barcoded image based on the passed in string"
    buf = StringIO()
    code = Code128Encoder(val)
    rend = Code128Renderer(code.bars, None)
    image = rend.get_pilimage(scale)
    image.save(buf, 'PNG')
    return buf.getvalue()
    
def generate_barcode_response(request, val, scale=3):
    "Generate a barcoded image based on the passed in string"
    response = HttpResponse(
        _generate_barcode(val, scale), 'image/png')
    return response