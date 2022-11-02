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

indices = {el: n for n, el in enumerate(elements)}

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

old_line_order = {}
old_data = {}
try:
    with open('data.js') as old:
        for n, line in enumerate(old):
            if ':[' in line:
                k, v =  line.split(':')
                old_line_order[k] = n
                old_data[k] = [c.strip("'") for c in v[:-3].split(',')[1:]]
except IOError:
    pass

out = sys.stdout
out.write('var elem_count = [')
for n, el in enumerate(elements):
    if n % 15 == 0:
        out.write('\n ')
    out.write('%d,' % cnt.get(el.upper(), 0))
out.write('\n];\n')
keys = list(ids_by_elems.keys())
keys.sort(key=lambda x: (-len(ids_by_elems[x]), old_line_order.get(x, 0)))
out.write('var ids_by_elems = {\n')
for k in keys:
    codes = ids_by_elems[k]
    if k in old_data and set(old_data[k]) == set(codes):
        codes = old_data[k]
    else:
        random.shuffle(codes)
        codes.sort(key=lambda x: 0 if x in top_codes else 1)
    cc = ','.join("'%s'" % c for c in codes[:entry_limit])
    out.write('%s:[%d,%s],\n' % (k, len(codes), cc))
out.write('};\n')

