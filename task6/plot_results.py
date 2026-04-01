import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- Plot 1: DOS ---
dos_data = np.loadtxt('dos_total.dat')

plt.figure(figsize=(10, 6))
plt.plot(dos_data[:, 0], dos_data[:, 1], 'b-', linewidth=1.2)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=0.8, label='Fermi level')
plt.xlabel('Energy (eV)', fontsize=13)
plt.ylabel('DOS (states/eV)', fontsize=13)
plt.title('Density of States — Water System', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('dos_plot.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: dos_plot.png  ({len(dos_data)} points)")

# --- Plot 2: Band structure ---
bands_data = np.loadtxt('water_bands_tot.dat')

plt.figure(figsize=(12, 8))
for i in range(1, bands_data.shape[1]):
    plt.plot(bands_data[:, 0], bands_data[:, i], 'b-', linewidth=0.6)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, label='Fermi level')
plt.xlabel('k-points', fontsize=13)
plt.ylabel('Energy (eV)', fontsize=13)
plt.title('Band Structure — Water System', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('bands_plot.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: bands_plot.png  ({bands_data.shape[1]-1} bands)")
