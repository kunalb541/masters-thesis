#!/usr/bin/env python3
"""
Generate thesis-quality figures for Chapters 2, 4, and 5
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os

# Set publication-quality defaults
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 11
rcParams['axes.labelsize'] = 11
rcParams['axes.titlesize'] = 12
rcParams['xtick.labelsize'] = 10
rcParams['ytick.labelsize'] = 10
rcParams['legend.fontsize'] = 10
rcParams['figure.dpi'] = 300
rcParams['savefig.dpi'] = 300
rcParams['savefig.bbox'] = 'tight'
rcParams['savefig.pad_inches'] = 0.05

# Create output directory
os.makedirs('../figures/chapter2', exist_ok=True)
os.makedirs('../figures/chapter4', exist_ok=True)
os.makedirs('../figures/chapter5', exist_ok=True)


def pspl_magnification(u):
    """PSPL magnification formula"""
    return (u**2 + 2) / (u * np.sqrt(u**2 + 4))


def create_chapter2_pspl_figure():
    """Figure 2.1: PSPL geometry and light curve"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Panel A: Lens plane geometry
    theta = np.linspace(0, 2*np.pi, 100)
    einstein_ring_x = np.cos(theta)
    einstein_ring_y = np.sin(theta)
    
    ax1.plot(einstein_ring_x, einstein_ring_y, 'k--', linewidth=1.5, 
             label='Einstein ring', alpha=0.5)
    ax1.plot(0, 0, 'ko', markersize=10, label='Lens')
    
    # Source trajectory
    u0 = 0.3
    t_vals = np.linspace(-2, 2, 100)
    traj_x = t_vals
    traj_y = np.full_like(t_vals, u0)
    ax1.plot(traj_x, traj_y, 'b-', linewidth=2, label=f'Source trajectory ($u_0={u0}$)')
    ax1.plot(0, u0, 'b*', markersize=15, label='Closest approach')
    
    # Image positions at closest approach
    u = u0
    r1 = 0.5 * (u + np.sqrt(u**2 + 4))
    r2 = 0.5 * (u - np.sqrt(u**2 + 4))
    ax1.plot(0, r1, 'ro', markersize=8, label='Images')
    ax1.plot(0, r2, 'ro', markersize=8)
    
    ax1.set_xlim(-2.5, 2.5)
    ax1.set_ylim(-2.5, 2.5)
    ax1.set_xlabel('Position (θ$_E$)')
    ax1.set_ylabel('Position (θ$_E$)')
    ax1.set_aspect('equal')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_title('(a) Lens Plane Geometry')
    
    # Panel B: Light curve
    t = np.linspace(-50, 50, 500)
    u_t = np.sqrt(u0**2 + (t/25)**2)  # t_E = 25 days
    A_t = pspl_magnification(u_t)
    
    ax2.plot(t, A_t, 'b-', linewidth=2)
    ax2.axhline(1.0, color='k', linestyle=':', alpha=0.5, label='Baseline')
    ax2.axvline(0, color='gray', linestyle='--', alpha=0.3, label='$t_0$')
    
    # Mark peak
    A_max = pspl_magnification(u0)
    ax2.plot(0, A_max, 'ro', markersize=8, label=f'Peak: A$_{{max}}$={A_max:.2f}')
    
    ax2.set_xlabel('Time (days)')
    ax2.set_ylabel('Magnification')
    ax2.set_title(f'(b) PSPL Light Curve ($u_0={u0}$, $t_E=25$ days)')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0.9, A_max + 0.5)
    
    plt.tight_layout()
    plt.savefig('../figures/chapter2/pspl_geometry.pdf')
    plt.savefig('../figures/chapter2/pspl_geometry.png')
    plt.close()
    print("✓ Created Figure 2.1: PSPL geometry and light curve")


def create_chapter4_example_lightcurves():
    """Figure 4.1: Example light curves for each class"""
    np.random.seed(42)
    
    fig, axes = plt.subplots(3, 1, figsize=(8, 9), sharex=True)
    
    # Time array
    t = np.linspace(0, 72, 6912)  # 72 days, 15-min cadence
    
    # Random sampling indices (95% of data)
    n_obs = len(t)
    observed = np.random.random(n_obs) > 0.05
    t_obs = t[observed]
    
    # Noise model
    def add_noise(flux, sigma_rel=0.02):
        noise = np.random.normal(0, sigma_rel * flux, size=len(flux))
        return flux + noise
    
    # Panel A: Flat (no lensing)
    F_flat = np.full_like(t, 3000.0)
    F_flat_obs = add_noise(F_flat[observed], sigma_rel=0.03)
    
    axes[0].plot(t_obs, F_flat_obs, 'k.', markersize=1, alpha=0.5)
    axes[0].axhline(3000, color='red', linestyle='--', linewidth=1.5, 
                    label='Baseline flux', alpha=0.7)
    axes[0].set_ylabel('Flux (counts)')
    axes[0].set_title('(a) Flat: No Lensing Event')
    axes[0].legend(loc='upper right')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(2500, 3500)
    
    # Panel B: PSPL
    u0_pspl = 0.2
    t0_pspl = 36
    tE_pspl = 20
    u_pspl = np.sqrt(u0_pspl**2 + ((t - t0_pspl) / tE_pspl)**2)
    A_pspl = pspl_magnification(u_pspl)
    F_pspl = 3000 * A_pspl
    F_pspl_obs = add_noise(F_pspl[observed], sigma_rel=0.02)
    
    axes[1].plot(t_obs, F_pspl_obs, 'b.', markersize=1, alpha=0.5)
    axes[1].plot(t, F_pspl, 'r-', linewidth=1.5, alpha=0.7, 
                 label='True PSPL profile')
    axes[1].set_ylabel('Flux (counts)')
    axes[1].set_title(f'(b) PSPL: Single Lens ($u_0={u0_pspl}$, $t_E={tE_pspl}$ days)')
    axes[1].legend(loc='upper right')
    axes[1].grid(True, alpha=0.3)
    
    # Panel C: Binary (simplified caustic crossing)
    u0_bin = 0.15
    t0_bin = 36
    tE_bin = 25
    u_bin = np.sqrt(u0_bin**2 + ((t - t0_bin) / tE_bin)**2)
    A_bin_base = pspl_magnification(u_bin)
    
    # Add simulated caustic crossings
    caustic1 = 30 + np.exp(-((t - 32) / 0.5)**2) * 8  # Sharp spike at t=32
    caustic2 = 32 + np.exp(-((t - 40) / 0.7)**2) * 6  # Sharp spike at t=40
    
    F_bin = 3000 * (A_bin_base * (1 + 0.15*np.sin(2*np.pi*(t-t0_bin)/5)))
    # Add caustic spikes
    idx1 = np.abs(t - 32) < 2
    idx2 = np.abs(t - 40) < 2
    F_bin[idx1] += caustic1[idx1] * 100
    F_bin[idx2] += caustic2[idx2] * 100
    
    F_bin_obs = add_noise(F_bin[observed], sigma_rel=0.02)
    
    axes[2].plot(t_obs, F_bin_obs, 'g.', markersize=1, alpha=0.5, label='Observations')
    axes[2].plot(t, F_bin, 'r-', linewidth=1.5, alpha=0.7, 
                 label='True binary profile')
    # Highlight caustic crossings
    axes[2].axvline(32, color='orange', linestyle=':', alpha=0.7, linewidth=2)
    axes[2].axvline(40, color='orange', linestyle=':', alpha=0.7, linewidth=2)
    axes[2].annotate('Caustic\ncrossing', xy=(32, F_bin.max()*0.9), 
                    xytext=(28, F_bin.max()*0.7),
                    arrowprops=dict(arrowstyle='->', color='orange', lw=1.5),
                    fontsize=9, color='orange', ha='right')
    axes[2].set_xlabel('Time (days)')
    axes[2].set_ylabel('Flux (counts)')
    axes[2].set_title('(c) Binary: Caustic Crossings ($u_0=0.15$, $q=0.01$, $s=1.1$)')
    axes[2].legend(loc='upper right')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../figures/chapter4/example_light_curves.pdf')
    plt.savefig('../figures/chapter4/example_light_curves.png')
    plt.close()
    print("✓ Created Figure 4.1: Example light curves")


def create_chapter4_architecture_diagram():
    """Figure 4.2: CNN-GRU architecture diagram (text-based)"""
    # This is better done in a tool like draw.io or TikZ
    # But here's a matplotlib version
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Input layer
    ax.add_patch(plt.Rectangle((0.5, 2.5), 1, 1, 
                               facecolor='lightblue', edgecolor='black', linewidth=2))
    ax.text(1, 3, 'Input\nLight Curve\n(N×1)', ha='center', va='center', fontsize=9)
    
    # CNN layers
    ax.add_patch(plt.Rectangle((2, 2.3), 1, 1.4, 
                               facecolor='lightgreen', edgecolor='black', linewidth=2))
    ax.text(2.5, 3, 'Conv1D\n(32 filters)\n+ReLU', ha='center', va='center', fontsize=8)
    
    ax.add_patch(plt.Rectangle((3.5, 2.3), 1, 1.4, 
                               facecolor='lightgreen', edgecolor='black', linewidth=2))
    ax.text(4, 3, 'Conv1D\n(64 filters)\n+ReLU', ha='center', va='center', fontsize=8)
    
    # Pooling
    ax.add_patch(plt.Rectangle((5, 2.5), 0.7, 1, 
                               facecolor='yellow', edgecolor='black', linewidth=2))
    ax.text(5.35, 3, 'Max\nPool', ha='center', va='center', fontsize=8)
    
    # GRU layers
    ax.add_patch(plt.Rectangle((6.5, 2), 1, 2, 
                               facecolor='salmon', edgecolor='black', linewidth=2))
    ax.text(7, 3, 'GRU\n(128 units)\nBidirectional', ha='center', va='center', fontsize=8)
    
    ax.add_patch(plt.Rectangle((8, 2), 1, 2, 
                               facecolor='salmon', edgecolor='black', linewidth=2))
    ax.text(8.5, 3, 'GRU\n(64 units)', ha='center', va='center', fontsize=8)
    
    # Dense layers
    ax.add_patch(plt.Rectangle((9.5, 2.5), 0.8, 1, 
                               facecolor='lightcoral', edgecolor='black', linewidth=2))
    ax.text(9.9, 3, 'Dense\n(32)', ha='center', va='center', fontsize=8)
    
    # Output
    ax.add_patch(plt.Rectangle((10.8, 2.5), 0.8, 1, 
                               facecolor='lavender', edgecolor='black', linewidth=2))
    ax.text(11.2, 3, 'Output\n(3 classes)\nSoftmax', ha='center', va='center', fontsize=8)
    
    # Arrows
    for x_start in [1.5, 3, 4.5, 5.7, 7.5, 9, 10.3]:
        ax.annotate('', xy=(x_start+0.4, 3), xytext=(x_start, 3),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    # Labels
    ax.text(1, 5, 'Feature Extraction', fontsize=10, weight='bold', ha='center')
    ax.plot([2, 5.7], [4.8, 4.8], 'k-', linewidth=2)
    
    ax.text(7.25, 5, 'Temporal Integration', fontsize=10, weight='bold', ha='center')
    ax.plot([6.5, 9], [4.8, 4.8], 'k-', linewidth=2)
    
    ax.text(10.4, 5, 'Classification', fontsize=10, weight='bold', ha='center')
    ax.plot([9.5, 11.6], [4.8, 4.8], 'k-', linewidth=2)
    
    ax.text(6, 0.5, 'CNN-GRU Hierarchical Architecture', 
           fontsize=12, weight='bold', ha='center')
    
    plt.tight_layout()
    plt.savefig('../figures/chapter4/architecture_diagram.pdf')
    plt.savefig('../figures/chapter4/architecture_diagram.png')
    plt.close()
    print("✓ Created Figure 4.2: Architecture diagram")


if __name__ == '__main__':
    print("Generating thesis figures...")
    print()
    create_chapter2_pspl_figure()
    create_chapter4_example_lightcurves()
    create_chapter4_architecture_diagram()
    print()
    print("All figures generated successfully!")
    print("Figures saved to:")
    print("  - figures/chapter2/")
    print("  - figures/chapter4/")
