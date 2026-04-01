import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re

lines = open('detailed.out').readlines()

# --- Parse atomic gross charges ---
charges = []
atom_ids = []
in_charges = False
for line in lines:
    if 'Atomic gross charges (e)' in line:
        in_charges = True
        continue
    if in_charges:
        if re.match(r'\s*\d+\s+-?\d+\.\d+', line):
            parts = line.split()
            atom_ids.append(int(parts[0]))
            charges.append(float(parts[1]))
        elif charges:
            break

# --- Parse energy components ---
energy_labels = []
energy_values = []
targets = {
    'Energy H0:': 'H0',
    'Energy SCC:': 'SCC',
    'Repulsive energy:': 'Repulsive',
    'Total energy:': 'Total',
}
for line in lines:
    for key, label in targets.items():
        if line.strip().startswith(key):
            val = float(line.split()[-2])  # eV value is second to last
            energy_labels.append(label)
            energy_values.append(val)

# --- Plot 1: Atomic charges ---
colors = ['red' if c < 0 else 'steelblue' for c in charges]
plt.figure(figsize=(14, 5))
plt.bar(atom_ids, charges, color=colors, width=0.8)
plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('Atom index', fontsize=12)
plt.ylabel('Gross charge (e)', fontsize=12)
plt.title('Atomic Gross Charges — Water System\n(red = O, blue = H)', fontsize=13)
plt.tight_layout()
plt.savefig('charges_plot.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: charges_plot.png  ({len(charges)} atoms parsed)")

# --- Plot 2: Energy breakdown ---
plt.figure(figsize=(7, 5))
bar_colors = ['#e07b54', '#5b8db8', '#6abf69', '#333333']
bars = plt.bar(energy_labels, energy_values, color=bar_colors)
plt.ylabel('Energy (eV)', fontsize=12)
plt.title('Energy Components', fontsize=13)
for bar, val in zip(bars, energy_values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             f'{val:.1f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('energy_plot.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: energy_plot.png   ({len(energy_values)} components parsed)")
