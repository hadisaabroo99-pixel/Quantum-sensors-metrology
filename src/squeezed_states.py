"""
Squeezed State Wigner Functions and Quadrature Analysis
W(x,p) = (1/π) exp(-e^{-2r}x² - e^{2r}p²)
"""

import numpy as np


def wigner_squeezed_vacuum(x, p, r):
    """
    Wigner function for squeezed vacuum state.
    
    Parameters:
    -----------
    x, p : float or array
        Phase space coordinates
    r : float
        Squeezing parameter
    
    Returns:
    --------
    W : array
        Wigner function values
    """
    X, P = np.meshgrid(x, p)
    W = (1 / np.pi) * np.exp(
        -np.exp(-2 * r) * X**2 
        - np.exp(2 * r) * P**2
    )
    return W


def quadrature_variances(r):
    """
    Quadrature variances for squeezed vacuum.
    
    σ_x² = (1/2)e^{-2r}  (squeezed quadrature)
    σ_p² = (1/2)e^{2r}   (anti-squeezed quadrature)
    
    Product σ_x²·σ_p² = 1/4 (saturates uncertainty principle)
    """
    var_x = 0.5 * np.exp(-2 * r)
    var_p = 0.5 * np.exp(2 * r)
    return var_x, var_p


def squeezing_to_db(r):
    """Convert squeezing parameter r to decibels."""
    return -10 * np.log10(np.exp(-2 * r))  # ≈ 8.686 * r


def db_to_squeezing(db):
    """Convert decibels to squeezing parameter."""
    return -0.5 * np.log10(10**(-db / 10))


def noise_spectrum_squeezed(frequency, r, gamma=1.0):
    """
    Squeezed light noise spectrum with Lorentzian cavity response.
    
    S_sq(Ω) = 0.5 · e^{-2r} / (1 + (Ω/γ)²)
    """
    return 0.5 * np.exp(-2 * r) / (1 + (frequency / gamma)**2)
