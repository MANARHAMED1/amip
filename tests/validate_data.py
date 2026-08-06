import csv
from pathlib import Path

data_dir = Path(r'D:\amip\generated_data')

def read_csv(name):
    with open(data_dir / f'{name}.csv', 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

print('=== FK VALIDATION ===')

secteurs = read_csv('secteur')
machines = read_csv('machine')
matieres = read_csv('matiere')
outils = read_csv('outil')
pieces = read_csv('piece')
gammes = read_csv('gamme_usinage')
phases = read_csv('phase_gamme')
ofs = read_csv('ordre_fabrication')
execs = read_csv('execution_phase')
exec_outils = read_csv('execution_outil')
causes = read_csv('cause_rebut')
controles = read_csv('controle_qualite')
maints = read_csv('maintenance')
sensors = read_csv('sensor_data')
operateurs = read_csv('operateur')
programmes = read_csv('programme_usinage')

secteur_ids = set(s['secteur_id'] for s in secteurs)
machine_ids = set(m['machine_id'] for m in machines)
matiere_ids = set(m['matiere_id'] for m in matieres)
outil_ids = set(o['outil_id'] for o in outils)
piece_ids = set(p['piece_id'] for p in pieces)
gamme_ids = set(g['gamme_id'] for g in gammes)
phase_ids = set(p['phase_gamme_id'] for p in phases)
of_ids = set(o['ordre_fabrication_id'] for o in ofs)
exec_ids = set(e['execution_id'] for e in execs)
cause_ids = set(c['cause_rebut_id'] for c in causes)
operateur_ids = set(o['operateur_id'] for o in operateurs)
prog_ids = set(p['programme_id'] for p in programmes)

errors = 0

for m in machines:
    if m['secteur_id'] not in secteur_ids:
        errors += 1

for p in pieces:
    if p['matiere_id'] and p['matiere_id'] not in matiere_ids:
        errors += 1

for g in gammes:
    if g['piece_id'] not in piece_ids:
        errors += 1

for p in phases:
    if p['gamme_id'] not in gamme_ids:
        errors += 1
    if p['machine_id'] not in machine_ids:
        errors += 1
    if p['outil_id'] not in outil_ids:
        errors += 1

for o in ofs:
    if o['piece_id'] not in piece_ids:
        errors += 1
    if o['gamme_id'] not in gamme_ids:
        errors += 1

for e in execs:
    if e['ordre_fabrication_id'] not in of_ids:
        errors += 1
    if e['phase_gamme_id'] not in phase_ids:
        errors += 1
    if e['machine_id'] not in machine_ids:
        errors += 1
    if e['outil_id'] and e['outil_id'] not in outil_ids:
        errors += 1
    if e['operateur_id'] and e['operateur_id'] not in operateur_ids:
        errors += 1

for eo in exec_outils:
    if eo['execution_id'] not in exec_ids:
        errors += 1
    if eo['outil_id'] not in outil_ids:
        errors += 1

for c in controles:
    if c['execution_id'] not in exec_ids:
        errors += 1
    if c['cause_rebut_id'] and c['cause_rebut_id'] not in cause_ids:
        errors += 1

for m in maints:
    if m['machine_id'] not in machine_ids:
        errors += 1
    if m['operateur_id'] and m['operateur_id'] not in operateur_ids:
        errors += 1

for s in sensors:
    if s['machine_id'] not in machine_ids:
        errors += 1

if errors == 0:
    print('ALL FOREIGN KEYS VALIDATED SUCCESSFULLY')
else:
    print(f'{errors} FK ERRORS FOUND')

print()
print('=== ROW COUNTS ===')
total = 0
for name in ['secteur','machine','operateur','matiere','outil','stock_outil','piece','programme_usinage','gamme_usinage','phase_gamme','ordre_fabrication','execution_phase','execution_outil','cause_rebut','controle_qualite','maintenance','sensor_data','stock_piece','stock_matiere']:
    rows = read_csv(name)
    total += len(rows)
    print(f'  {name:25s} {len(rows):>8d}')
print(f'  {"TOTAL":25s} {total:>8d}')
