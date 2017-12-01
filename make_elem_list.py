#!/usr/bin/env python
import os
import sys
from gemmi import cif

def main():
    for arg in sys.argv[1:]:
      if os.path.isdir(arg):
        for root, _, files in os.walk(arg):
          for name in files:
            if not name.endswith('.cif') and not name.endswith('.cif.gz'):
              print("skip " + name)
              continue
            find_elements(root, name)
      else:
        root, name = os.path.split(arg)
        find_elements(root, name)

def find_elements(root, name):
  try:
    doc = cif.read(os.path.join(root, name))
    block = doc.sole_block()
    elems = set(block.find_loop("_atom_site.type_symbol"))
    print(name + ' ' + ' '.join(elems))
  except Exception as e:
    print("Oops. %s" % e)

main()
