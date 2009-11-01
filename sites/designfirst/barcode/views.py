from huBarcode.code128 import Code128Encoder, Code128Renderer
from huBarcode.datamatrix import DataMatrixEncoder, DataMatrixRenderer

from StringIO import StringIO

from django.http import HttpResponse


def _generate_code128(val, scale):
    "Generate a code128 image based on the passed in string"
    buf = StringIO()
    code = Code128Encoder(val)
    rend = Code128Renderer(code.bars, None)
    image = rend.get_pilimage(scale)
    image.save(buf, 'PNG')
    return buf.getvalue()

def _generate_datamatrix(val, scale):
    "Generate a datamatrix image based on the passed in string"
    buf = StringIO()
    code = DataMatrixEncoder(val)
    rend = DataMatrixRenderer(code.matrix)
    image = rend.get_pilimage(scale)
    image.save(buf, 'PNG')
    return buf.getvalue()

_symbologies = {
    'c128': (_generate_code128, 3),
    'dmtx': (_generate_datamatrix, 5),
}
    
def generate_barcode_response(request, type, val):
    "Generate a barcoded image based on the passed in string"
    encoder, scale = _symbologies.get(type)
    if 'scale' in request.GET:
        scale = int(request.GET['scale'])
    response = HttpResponse(
        encoder(val, scale), 'image/png')
    return response