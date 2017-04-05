#!/usr/bin/env python

import sys
import random
from collections import Counter

elements = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na',
'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr',
'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb',
'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu',
'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os',
'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac',
'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No',
'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc',
'Lv', 'Ts', 'Og',
'D', 'X']

top_list = 'Top8000-SFbest_hom50_pdb_chain_list.csv'
top_codes = [line.split(',')[0] for line in open(top_list)][1:]

indices = dict((el, n) for n, el in enumerate(elements))

input_file = sys.argv[1]
entry_limit = int(sys.argv[2])

ids_by_elems = {}

cnt = Counter()
for line in open(input_file):
    if line.startswith('Oops'):
        sys.stderr.write('Something went wrong: Oops in the input. Exiting.\n')
        sys.exit(1)
    sp = line.split()
    cnt.update(sp[1:])
    el_in_entry = [e.title() for e in sp[1:]]
    el_in_entry.sort(key=lambda x: indices[x])
    key = ''.join(e.ljust(2, '_') for e in el_in_entry)
    code = sp[0][:4]
    ids_by_elems.setdefault(key, []).append(code)

out = sys.stdout
out.write('var elem_count = [')
for n, el in enumerate(elements):
    if n % 15 == 0:
        out.write('\n ')
    out.write('%d,' % cnt.get(el.upper(), 0))
out.write('\n];\n')
keys = sorted(ids_by_elems.keys(), key=lambda x: -len(ids_by_elems[x]))
out.write('var ids_by_elems = {\n')
for k in keys:
    codes = ids_by_elems[k]
    random.shuffle(codes)
    codes.sort(key=lambda x: 0 if x in top_codes else 1)
    # todo sort by quality? random shuffle?
    cc = ','.join("'%s'" % c for c in codes[:entry_limit])
    out.write('%s:[%d,%s],\n' % (k, len(codes), cc))
out.write('};\n')

