import os
import re
import random
import subprocess
import string
from PIL import Image
import logging

from django.conf import settings


logger = logging.getLogger('util.pdf')

PPM_TMP_ROOT = settings.PPM_TMP_ROOT
logger.debug('pdf module initialized with PPM_TMP_ROOT at %s', PPM_TMP_ROOT)


pages_pattern = re.compile(r'^Pages:\s+(?P<pages>\d+)$', re.MULTILINE)
ppmfile_pattern = re.compile(r'(\d+)\.ppm$')
                             
def create_random_dir(base_path):
    name = "".join(random.sample(string.letters+string.digits, 10))
    ppm_dir = os.path.join(base_path, name)
    if not os.path.exists(ppm_dir):
        os.makedirs(ppm_dir)
    return ppm_dir


def pdf2ppm(pdf_file_path, callback, sizes=[]):
    pages = 0
    output = subprocess.Popen(['pdfinfo', pdf_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    logger.debug('pdfinfo for file %s: %s', pdf_file_path, output)
    if output:
        match = pages_pattern.search(output)
        if match:
            pages = int(match.groupdict()['pages'])
    if not pages:
        return

    ppm_dir = create_random_dir(PPM_TMP_ROOT)
    logger.debug('created tempdir %s', ppm_dir)

    format = "%s/page-%s.ppm" % (ppm_dir, "%d")

    subprocess.call(['pdftoppm', pdf_file_path, ppm_dir+'/page'])
    logger.debug('ppm files generated to %s', ppm_dir+'/page')

    pdfdir, pdfname =  os.path.split(pdf_file_path)
    pdfname, ext = os.path.splitext(pdfname)
    
    for ppm_file in os.listdir(ppm_dir):
        page = int(ppmfile_pattern.findall(ppm_file)[0])
        image = Image.open(os.path.join(ppm_dir, ppm_file))
        callback(image, pdfname, page) 
#        for size in sizes:
#            thumb = image.copy()
#            thumb.thumbnail(size, Image.ANTIALIAS)
#            filename = '%s-%dx%d-%d.png' % (pdfname, size[0], size[1], page)
#            callback(thumb, filename, page)

    logger.debug('removing tempdir %s', ppm_dir)
    subprocess.call('rm -r ' + ppm_dir, shell=True)
    
    return pages
