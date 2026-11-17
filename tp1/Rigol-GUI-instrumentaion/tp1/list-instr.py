#!/usr/bin/env python3
"""VISA test executable - lists every VISA resource found (generator + scope)"""

import pyvisa

print("PyVISA version:", pyvisa.__version__)
rm = pyvisa.ResourceManager('@py')
for i, res in enumerate(rm.list_resources(), 1):
    print(f"  {i}. {res}")
rm.close()
