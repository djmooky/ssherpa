#!/bin/bash

rm -f ssherpa.zip
cp ssherpa.py __main__.py
zip ssherpa.zip *.py
echo '#!/usr/bin/env python' | cat - ssherpa.zip > ssherpa
chmod +x ssherpa


