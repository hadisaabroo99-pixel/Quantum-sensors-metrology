"""
Ramsey Interferometry Simulation
Demonstrates population oscillations P_|1⟩ = cos²(Δω·τ/2)
"""

import numpy as np
import matplotlib.pyplot as plt


def ramsey_fringe(tau, detuning, phase_offset=0):
    """
    Calculate Ramsey fringe population P_|1⟩.
    
    Parameters:
    -----------
    tau : float or array
        Interrogation time
    detuning : float
        Frequency detuning Δω
    phase_offset : float
        Additional phase offset
    
    Returns:
    --------
    P1 : array
        Population in |1⟩ state
    """
    phi = detuning * tau + phase_offset
    return np.cos(phi / 2) ** 2


def phase_sensitivity(tau, detuning):
    """
    Calculate phase sensitivity |dP/dφ| = |sin(φ)|.
    
    Maximum sensitivity occurs at φ = π/2, 3π/2 (steepest slope)
    """
    phi = detuning * tau
    return np.abs(np.sin(phi))


def simulate_shot_noise(N_atoms, N_trials, detuning, tau):
    """
    Simulate binomial shot noise in Ramsey measurements.
    
    Parameters:
    -----------
    N_atoms : int
        Number of atoms per trial
    N_trials : int
        Number of measurement trials
    detuning : float
        Frequency detuning
    tau : float
        Interrogation time
    
    Returns:
    --------
    mean_P1 : float
        Mean population
    std_P1 : float
        Standard deviation (shot noise = √(P(1-P)/N))
    """
    P1_theory = ramsey_fringe(tau, detuning)
    counts = np.random.binomial(N_atoms, P1_theory, N_trials)
    P1_measured = counts / N_atoms
    return np.mean(P1_measured), np.std(P1_measured)


if __name__ == "__main__":
    # Example usage
    tau = np.linspace(0, 4*np.pi, 1000)
    detunings = [0.2, 0.5, 1.0, 2.0]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    for dw in detunings:
        P1 = ramsey_fringe(tau, dw)
        ax.plot(tau, P1, linewidth=2, label=f'Δω = {dw}')
    
    ax.set_xlabel('Interrogation Time τ')
    ax.set_ylabel('P_|1⟩ = cos²(Δω·τ/2)')
    ax.set_title('Ramsey Interferometry Fringes')
    ax.legend()
    ax.set_xlim(0, 4*np.pi)
    ax.set_ylim(-0.05, 1.05)
    plt.tight_layout()
    plt.savefig('figures/ramsey_example.png', dpi=150)
    plt.show()
