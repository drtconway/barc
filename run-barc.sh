#!/bin/bash

for f in *.yaml
do
    b=$(basename ${f} .yaml)
    h="${b}.html"
    p="${b}.pdf"
    python3 /barc.py ${f} > ${h}
    prince ${h} -o ${p}
done
