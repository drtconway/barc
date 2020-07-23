"""barc - create sheets of barcode labels

Usage:
    barc [options] [<spec.yaml>]

Options:
    -l --list       list the available barcode types
    -n --check      check the validity of the specification but don't produce html output
    -o FILE         specify an output file ('-' for stdout) [default: -]
"""

import base64
import io
import sys
import hashlib
import uuid

import docopt
import yaml

import barcode
from barcode.base import Barcode
import dominate
from dominate.tags import *

version = '0.1.0'

def make_barcode(kind, code):
    bio = io.BytesIO()
    barcode.get(kind, code, writer=barcode.writer.ImageWriter()).render().save(bio, 'png')
    bio.seek(0)
    return base64.b64encode(bio.read()).decode('utf-8')

def rndCode():
    u = str(uuid.uuid4())
    d = hashlib.new('SHA1', u)
    return d.hexdigest()[:12]

def check(spec):
    
    # Version check
    #
    if 'version' not in spec:
        print('missing version from spec', file=sys.stderr)
        return False
    if spec['version'] != '1' and spec['version'] != 1:
        print("version must be '1'.", file=sys.stderr)
        return False

    # Options Check
    #
    if 'options' in spec:
        if not isinstance(spec['options'], dict):
            print("error: options must be a map/dictionary", file=sys.stderr)
            return False

        permitted = set(['barcode-type', 'barcode-prefix', 'style'])
        seen = set(spec['options'].keys())
        bad = seen - permitted
        if len(bad) > 0:
            print(f"error: the following option[s] are unrecognised: {', '.join(sorted(bad))}", file=sys.stderr)
            return False

    # Check given options
    #
    if 'barcode-type' in spec['options']:
        bc = spec['options']['barcode-type'].lower()
        if bc not in barcode.PROVIDED_BARCODES:
            print(f"barcode-type not supported: {spec['options']['barcode-type']}", file=sys.stderr)
            return False

    return True

def main():
    opts = docopt.docopt(__doc__, version=f'barc {version}')

    if opts['--list']:
        print(', '.join(barcode.PROVIDED_BARCODES), file=sys.stdout)
        sys.exit(0)

    if not opts['<spec.yaml>']:
        print("specification file required", file=sys.stdout)
        sys.exit(1)

    with open(opts['<spec.yaml>']) as f:
        spec = yaml.safe_load(f)

    if not check(spec):
        sys.exit(1)

    if opts['--check']:
        sys.exit(0)

    Barcode.default_writer_options['write_text'] = False

    kind = "Code128"
    pxf = ''
    sty = None

    if 'options' in spec:
        if 'barcode-type' in spec["options"]:
            kind = spec["options"]["barcode-type"]

        if 'barcode-prefix' in spec["options"]:
            pfx = spec["options"]["barcode-prefix"]

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
                            x = make_barcode(kind, bc)
                            img(src=f'data:image/png;base64,{x}')
                            if isinstance(lb, list):
                                for l in lb:
                                    p(l)
                            else:
                                p(lb)
    print(doc)

if __name__ == '__main__':
    main()

