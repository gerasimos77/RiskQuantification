import numpy as np
import pandas as pd
import os

class GeometricBM:
    """Class Constructing & Simulating a Geometric Brownian Motion Stochastic Process."""
    def __init__(self, mu: float, sigma: float,
                 horizon: int, num_steps: int, num_simulations:int , initial_value:float,
                 save_results: bool = False, output_dir=None):
        self.mu = mu # Drift (Expected return)
        self.sigma = sigma # Volatility
        self.horizon = horizon # Horizon of simulations (in Years)
        self.num_steps = num_steps # Number of steps (number of RVs in the process)
        self.num_simulations = num_simulations # Number of paths (scenarios)
        self.initial_value = initial_value # Initial value of simulated instance
        self.save_results = save_results
        self.output_dir = output_dir

    def simulate(self):
        """Performs Monte Carlo Simulation of Geometric Brownian Motion."""
        # Define the time distance between random variables in process
        dt = self.horizon / self.num_steps

        # Define the time-steps array
        t = np.linspace(0, self.horizon, self.num_steps)
        # Reshape time-array to allow broadcasting
        t = t.reshape(self.num_steps, 1)

        # Sample Brownian Motion Terms
        w = np.random.normal(loc=0, scale=1, size=(self.num_steps, self.num_simulations))
        w = np.cumsum(w, axis=0)
        w = w * np.sqrt(dt)

        # Calculate Samples in a single array
        s = self.initial_value * np.exp(
            (self.mu - 0.5 * self.sigma**2) * t + self.sigma * w)

        if self.save_results:
            pd.DataFrame(s).to_csv(os.path.join(self.output_dir, "GBM_simulation_results.csv"))

        return t, s




