"""
Bayesian Phase Estimation with Adaptive Measurements
"""

import numpy as np


class BayesianPhaseEstimator:
    """
    Adaptive Bayesian phase estimation for quantum metrology.
    
    Uses measurement outcomes to update posterior distribution
    and adaptively choose next measurement phase.
    """
    
    def __init__(self, N_atoms, phi_grid=None):
        self.N_atoms = N_atoms
        if phi_grid is None:
            self.phi_grid = np.linspace(0, 2*np.pi, 1000)
        else:
            self.phi_grid = phi_grid
        self.prior = np.ones_like(self.phi_grid) / (2 * np.pi)
        self.posterior = self.prior.copy()
        self.measurements = []
        
    def likelihood(self, phi, theta, outcome):
        """
        Likelihood function for Ramsey measurement.
        
        P(outcome|φ,θ) = cos²((φ-θ)/2) for outcome=1
                       = sin²((φ-θ)/2) for outcome=0
        """
        phase = phi - theta
        if outcome == 1:
            return np.cos(phase / 2) ** 2
        else:
            return np.sin(phase / 2) ** 2
    
    def update(self, theta, outcome):
        """
        Bayesian update: posterior ∝ likelihood × prior
        """
        lik = self.likelihood(self.phi_grid, theta, outcome)
        self.posterior = lik * self.posterior
        self.posterior /= np.trapezoid(self.posterior, self.phi_grid)
        self.measurements.append((theta, outcome))
        
    def map_estimate(self):
        """Maximum a posteriori (MAP) estimate."""
        return self.phi_grid[np.argmax(self.posterior)]
    
    def mean_estimate(self):
        """Mean of posterior distribution."""
        return np.trapezoid(self.phi_grid * self.posterior, self.phi_grid)
    
    def std_estimate(self):
        """Standard deviation of posterior (estimation error)."""
        mean = self.mean_estimate()
        var = np.trapezoid((self.phi_grid - mean)**2 * self.posterior, self.phi_grid)
        return np.sqrt(var)
    
    def adaptive_theta(self):
        """
        Choose next measurement phase to maximize Fisher information.
        For large N, optimal is θ ≈ φ_MAP ± π/2.
        """
        phi_map = self.map_estimate()
        # Alternate between ±π/2 to maximize sensitivity
        if len(self.measurements) % 2 == 0:
            return phi_map + np.pi / 2
        else:
            return phi_map - np.pi / 2
    
    def run_adaptive_estimation(self, phi_true, n_measurements):
        """
        Run full adaptive estimation protocol.
        """
        errors = []
        for m in range(n_measurements):
            if m == 0:
                theta = 0
            else:
                theta = self.adaptive_theta()
            
            # Simulate measurement
            p1 = np.cos((phi_true - theta) / 2) ** 2
            outcome = np.random.random() < p1
            
            self.update(theta, outcome)
            errors.append(self.std_estimate())
            
        return np.array(errors)
