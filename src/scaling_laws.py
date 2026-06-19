"""
Quantum Metrology Scaling Laws
Standard Quantum Limit (SQL) vs Heisenberg Limit (HL)
"""

import numpy as np


def sql_scaling(N):
    """Standard Quantum Limit: Δφ ∝ 1/√N"""
    return 1.0 / np.sqrt(N)


def heisenberg_scaling(N):
    """Heisenberg Limit: Δφ ∝ 1/N"""
    return 1.0 / N


def squeezed_scaling(N, r, N_max=1e6):
    """
    Squeezed state scaling interpolates between SQL and HL.
    
    For moderate squeezing: Δφ ≈ e^{-r}/√N
    Saturates at HL for large N or strong squeezing.
    """
    squeezed = sql_scaling(N) * np.exp(-r)
    return np.maximum(squeezed, heisenberg_scaling(N))


def wineland_parameter(r):
    """
    Wineland spin squeezing parameter ξ² = e^{-2r} for ideal squeezing.
    
    ξ² < 1 indicates squeezing below SQL.
    ξ² = 1/N would reach HL.
    """
    return np.exp(-2 * r)


def quantum_fisher_info(N, state_type='separable', r=0):
    """
    Quantum Fisher Information for different states.
    
    Parameters:
    -----------
    N : int
        Number of particles
    state_type : str
        'separable', 'squeezed', or 'GHZ'
    r : float
        Squeezing parameter (for squeezed states)
    
    Returns:
    --------
    F_Q : float
        Quantum Fisher Information
    """
    if state_type == 'separable':
        return N
    elif state_type == 'squeezed':
        return N * np.exp(2 * r)
    elif state_type == 'GHZ':
        return N ** 2
    else:
        raise ValueError(f"Unknown state_type: {state_type}")


def cramerrao_bound(F_Q):
    """Cramér-Rao lower bound on phase estimation precision."""
    return 1.0 / np.sqrt(F_Q)
