import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from models.fair_model import FAIRModel, TEFInput, VulnerabilityInput, LossInput

class MonteCarloSimulation:
    """Performs Monte Carlo simulations for the FAIR model"""
    
    def __init__(self, fair_model: FAIRModel, num_simulations: int = 10000):
        """
        Initialize the Monte Carlo simulation.
        
        Args:
            fair_model: The configured FAIR model with all parameters
            num_simulations: Number of simulations to run (default: 10000)
        """
        self.fair_model = fair_model
        self.num_simulations = num_simulations
        self.results = None
        
    def _generate_distribution_sample(self, param, size=1):
        """Generate random samples from the specified distribution"""
        distribution = param.distribution.lower()
        
        if distribution == "uniform":
            return np.random.uniform(param.min_value, param.max_value, size)
        
        elif distribution == "triangular":
            return np.random.triangular(
                param.min_value, 
                param.most_likely, 
                param.max_value, 
                size
            )
            
        elif distribution == "pert":
            # PERT distribution approximation using Beta distribution
            # Calculate alpha and beta parameters for Beta distribution
            if param.most_likely is None:
                param.most_likely = (param.min_value + param.max_value) / 2
                
            # PERT uses a modified beta distribution
            range_val = param.max_value - param.min_value
            if range_val == 0:
                return np.ones(size) * param.min_value
                
            # Calculate shape parameters
            mu = (param.min_value + 4 * param.most_likely + param.max_value) / 6
            
            # If mu is equal to min or max, avoid division by zero
            if mu == param.min_value or mu == param.max_value:
                return np.ones(size) * mu
                
            v = (mu - param.min_value) * (param.max_value - mu) / (
                (param.max_value - param.min_value) ** 2
            )
            
            w = ((mu - param.min_value) / (param.max_value - param.min_value)) * (
                (1 / v) - 1
            )
            
            alpha = w
            beta = (1 - (mu - param.min_value) / (param.max_value - param.min_value)) * (
                (1 / v) - 1
            )
            
            # Generate beta samples and scale to the min-max range
            beta_samples = np.random.beta(alpha, beta, size)
            return param.min_value + beta_samples * range_val
            
        elif distribution == "lognormal":
            # For lognormal, we interpret min/max as 5th and 95th percentiles
            # (Appropriate for modeling losses that can be very large)
            ln_min = np.log(param.min_value)
            ln_max = np.log(param.max_value)
            
            # Estimate mu and sigma for the lognormal distribution
            # using the 5th and 95th percentiles
            z_95 = 1.645  # Z-score for 95th percentile
            sigma = (ln_max - ln_min) / (2 * z_95)
            mu = (ln_min + ln_max) / 2
            
            return np.random.lognormal(mu, sigma, size)
        
        else:
            # Default to uniform distribution
            return np.random.uniform(param.min_value, param.max_value, size)
    
    def run_simulation(self):
        """Run the Monte Carlo simulation and store the results"""
        # Validate that all inputs are set
        self.fair_model.validate_inputs()
        
        # Generate random samples for each input
        tef_samples = self._generate_distribution_sample(
            self.fair_model.tef, self.num_simulations
        )
        
        vulnerability_samples = self._generate_distribution_sample(
            self.fair_model.vulnerability, self.num_simulations
        )
        
        loss_magnitude_samples = self._generate_distribution_sample(
            self.fair_model.loss_magnitude, self.num_simulations
        )
        
        # Calculate Loss Event Frequency (LEF)
        lef_samples = tef_samples * vulnerability_samples
        
        # Calculate Annual Loss Expectancy (ALE)
        ale_samples = lef_samples * loss_magnitude_samples
        
        # Store results in a DataFrame
        self.results = pd.DataFrame({
            'TEF': tef_samples,
            'Vulnerability': vulnerability_samples,
            'LEF': lef_samples,
            'Loss Magnitude': loss_magnitude_samples,
            'ALE': ale_samples
        })
        
        return self.results
    
    def get_summary_statistics(self) -> Dict:
        """Calculate summary statistics from the simulation results"""
        if self.results is None:
            raise ValueError("Simulation hasn't been run yet. Call run_simulation() first.")
        
        # Calculate statistics for ALE
        ale_percentiles = {
            'min': self.results['ALE'].min(),
            'max': self.results['ALE'].max(),
            'mean': self.results['ALE'].mean(),
            'median': self.results['ALE'].median(),
            'std': self.results['ALE'].std(),
            'percentile_10': self.results['ALE'].quantile(0.1),
            'percentile_25': self.results['ALE'].quantile(0.25), 
            'percentile_75': self.results['ALE'].quantile(0.75),
            'percentile_90': self.results['ALE'].quantile(0.9),
            'percentile_95': self.results['ALE'].quantile(0.95),
            'percentile_99': self.results['ALE'].quantile(0.99)
        }
        
        # Calculate statistics for LEF
        lef_stats = {
            'min': self.results['LEF'].min(),
            'max': self.results['LEF'].max(),
            'mean': self.results['LEF'].mean(),
            'median': self.results['LEF'].median(),
            'std': self.results['LEF'].std()
        }
        
        # Calculate statistics for Loss Magnitude
        lm_stats = {
            'min': self.results['Loss Magnitude'].min(),
            'max': self.results['Loss Magnitude'].max(),
            'mean': self.results['Loss Magnitude'].mean(),
            'median': self.results['Loss Magnitude'].median(),
            'std': self.results['Loss Magnitude'].std()
        }
        
        return {
            'ALE': ale_percentiles,
            'LEF': lef_stats,
            'Loss_Magnitude': lm_stats
        }
    
    def get_value_at_risk(self, confidence_level: float = 0.95) -> float:
        """
        Calculate the Value at Risk (VaR) at the specified confidence level.
        
        Args:
            confidence_level: The confidence level (e.g., 0.95 for 95% VaR)
            
        Returns:
            The Value at Risk at the specified confidence level
        """
        if self.results is None:
            raise ValueError("Simulation hasn't been run yet. Call run_simulation() first.")
        
        return self.results['ALE'].quantile(confidence_level)
