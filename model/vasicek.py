import numpy as np
import pandas as pd
import os

class VasicekModel:
    """Class Constructing & Simulating a Vasicek Stochastic Process."""
    def __init__(self, long_term_mean: float, sigma: float, kappa: float,
                 horizon: int, num_steps: int, num_simulations:int , initial_value:float,
                 save_results: bool = False, output_dir=None):
        self.long_term_mean = long_term_mean  # Long-term mean of simulated instance
        self.sigma = sigma # Volatility
        self.kappa = kappa # Rate of mean-reversion of simulated instance
        self.horizon = horizon # Horizon of simulations (in Years)
        self.num_steps = num_steps # Number of steps (number of RVs in the process)
        self.num_simulations = num_simulations # Number of paths (scenarios)
        self.initial_value = initial_value # Initial value of simulated instance
        self.save_results = save_results
        self.output_dir = output_dir

    def simulate(self):
        """Performs Monte Carlo Simulation of Vasicek Model."""
        # Define the time distance between random variables in process
        dt = self.horizon / self.num_steps

        # Define the time-steps array
        t = np.linspace(0, self.horizon, self.num_steps)
        # Reshape time-array to allow broadcasting
        t = t.reshape(self.num_steps, 1)

        # Initialize simulated values' array
        r = np.zeros((self.num_steps, self.num_simulations))
        r[0, :] = self.initial_value

        # Analytical solution complex; we will add cumulative dr
        for i in range(1, self.num_steps):
            dr = (self.kappa * (self.long_term_mean - r[i, :]) * dt
                  + self.sigma * np.sqrt(dt) * np.random.normal(loc=0, scale=1, size=(1, self.num_simulations)))

            r[i, :] = r[i-1, :] + dr

        if self.save_results:
            pd.DataFrame(r).to_csv(os.path.join(self.output_dir, "Vasicek_simulation_results.csv"))

        return t, r




