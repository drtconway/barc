import base64
import io
import sys
import hashlib
import uuid

import yaml

import barcode
from barcode.base import Barcode
import dominate
from dominate.tags import *

def mkBarc(kind, code):
    bio = io.BytesIO()
    barcode.get(kind, code, writer=barcode.writer.ImageWriter()).render().save(bio, 'png')
    bio.seek(0)
    return base64.b64encode(bio.read()).decode('utf-8')

def rndCode():
    u = str(uuid.uuid4())
    d = hashlib.new('SHA1', u)
    return d.hexdigest()[:12]

Barcode.default_writer_options['write_text'] = False

with open(sys.argv[1]) as f:
    spec = yaml.safe_load(f)

kind = "Code128"
pxf = ''
sty = None

if 'options' in spec:
    if 'barcode-type' in spec["options"]:
        kind = spec["options"]["barcode-type"]

    if 'prefix' in spec["options"]:
        pfx = spec["options"]["prefix"]

    if 'style' in spec['options']:
        sty = spec['options']['style']

doc = dominate.document(title='Barcodes')

with doc.head:
    if sty is not None:
        link(rel='stylesheet', href=f'{sty}.css')

with doc:
    with table(_class='labels'):
        for row in spec['barcodes']:
            with tr():
                for itm in row:
                    if 'code' in itm:
                        bc = itm['code']
                    else:
                        bc = None
                    if 'label' in itm:
                        lb = itm['label']
                    else:
                        lb = None
                    if lb is None and (bc is None or len(bc) == 0):
                        bc = rndCode()
                    if bc is None:
                        bc = lb
                    if lb is None:
                        lb = bc

                    with td(_class='label'):
                        x = mkBarc(kind, bc)
                        img(src=f'data:image/png;base64,{x}')
                        if isinstance(lb, list):
                            for l in lb:
                                p(l)
                        else:
                            p(lb)
print(doc)
