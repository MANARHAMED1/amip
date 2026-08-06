import csv
with open(r'D:\amip\generated_data\gamme_usinage.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
zero = sum(1 for r in rows if r['duree_totale_estimee'] == '0')
non_zero = sum(1 for r in rows if r['duree_totale_estimee'] != '0')
print(f'Total: {len(rows)}')
print(f'With duration: {non_zero}')
print(f'Zeros: {zero}')
print()
for r in rows[:5]:
    print(f"  {r['code']:10s} phases={r['nb_phases']}  duree_totale={r['duree_totale_estimee']} min")
