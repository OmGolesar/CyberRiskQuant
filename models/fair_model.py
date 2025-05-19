import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


@dataclass
class TEFInput:
    """Threat Event Frequency input parameters"""
    min_value: float  # Minimum expected events per year
    max_value: float  # Maximum expected events per year
    most_likely: Optional[float] = None  # Most likely value (for triangular distribution)
    distribution: str = "uniform"  # Can be 'uniform', 'triangular', 'pert', etc.
    
    def __post_init__(self):
        if self.min_value < 0:
            raise ValueError("Minimum value cannot be negative")
        if self.max_value < self.min_value:
            raise ValueError("Maximum value must be greater than minimum value")
        if self.distribution in ["triangular", "pert"] and self.most_likely is None:
            self.most_likely = (self.min_value + self.max_value) / 2


@dataclass
class VulnerabilityInput:
    """Vulnerability input parameters (probability of threat event becoming loss event)"""
    min_value: float  # Minimum probability (0-1)
    max_value: float  # Maximum probability (0-1)
    most_likely: Optional[float] = None  # Most likely value (for triangular distribution)
    distribution: str = "uniform"  # Can be 'uniform', 'triangular', 'pert', etc.
    
    def __post_init__(self):
        if not 0 <= self.min_value <= 1:
            raise ValueError("Minimum probability must be between 0 and 1")
        if not 0 <= self.max_value <= 1:
            raise ValueError("Maximum probability must be between 0 and 1")
        if self.max_value < self.min_value:
            raise ValueError("Maximum value must be greater than minimum value")
        if self.distribution in ["triangular", "pert"] and self.most_likely is None:
            self.most_likely = (self.min_value + self.max_value) / 2


@dataclass
class LossInput:
    """Loss magnitude input parameters"""
    min_value: float  # Minimum loss amount
    max_value: float  # Maximum loss amount
    most_likely: Optional[float] = None  # Most likely value (for triangular distribution)
    distribution: str = "uniform"  # Can be 'uniform', 'triangular', 'pert', etc.
    
    def __post_init__(self):
        if self.min_value < 0:
            raise ValueError("Minimum value cannot be negative")
        if self.max_value < self.min_value:
            raise ValueError("Maximum value must be greater than minimum value")
        if self.distribution in ["triangular", "pert"] and self.most_likely is None:
            self.most_likely = (self.min_value + self.max_value) / 2


class FAIRModel:
    """Implementation of the FAIR (Factor Analysis of Information Risk) model"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.tef = None  # Threat Event Frequency
        self.vulnerability = None  # Vulnerability
        self.loss_magnitude = None  # Loss Magnitude
        
    def set_threat_event_frequency(self, tef: TEFInput):
        """Set the threat event frequency parameters"""
        self.tef = tef
        
    def set_vulnerability(self, vulnerability: VulnerabilityInput):
        """Set the vulnerability parameters"""
        self.vulnerability = vulnerability
        
    def set_loss_magnitude(self, loss_magnitude: LossInput):
        """Set the loss magnitude parameters"""
        self.loss_magnitude = loss_magnitude
        
    def validate_inputs(self) -> bool:
        """Validate that all required inputs are set"""
        if self.tef is None:
            raise ValueError("Threat Event Frequency not set")
        if self.vulnerability is None:
            raise ValueError("Vulnerability not set")
        if self.loss_magnitude is None:
            raise ValueError("Loss Magnitude not set")
        return True
    
    def calculate_loss_event_frequency(self, tef_value: float, vulnerability_value: float) -> float:
        """Calculate the Loss Event Frequency (LEF) from TEF and Vulnerability"""
        return tef_value * vulnerability_value
    
    def calculate_risk(self, lef: float, loss_magnitude: float) -> float:
        """Calculate the risk (Annual Loss Expectancy) from LEF and Loss Magnitude"""
        return lef * loss_magnitude
    
    def calculate_single_loss_expectancy(self, loss_magnitude: float) -> float:
        """Calculate a single loss expectancy"""
        return loss_magnitude
    
    def to_dict(self) -> Dict:
        """Convert the model to a dictionary for storage/serialization"""
        return {
            "name": self.name,
            "description": self.description,
            "tef": {
                "min_value": self.tef.min_value,
                "max_value": self.tef.max_value,
                "most_likely": self.tef.most_likely,
                "distribution": self.tef.distribution
            } if self.tef else None,
            "vulnerability": {
                "min_value": self.vulnerability.min_value,
                "max_value": self.vulnerability.max_value,
                "most_likely": self.vulnerability.most_likely,
                "distribution": self.vulnerability.distribution
            } if self.vulnerability else None,
            "loss_magnitude": {
                "min_value": self.loss_magnitude.min_value,
                "max_value": self.loss_magnitude.max_value,
                "most_likely": self.loss_magnitude.most_likely,
                "distribution": self.loss_magnitude.distribution
            } if self.loss_magnitude else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FAIRModel':
        """Create a FAIR model from a dictionary"""
        model = cls(data["name"], data["description"])
        
        if data["tef"]:
            model.set_threat_event_frequency(TEFInput(
                min_value=data["tef"]["min_value"],
                max_value=data["tef"]["max_value"],
                most_likely=data["tef"]["most_likely"],
                distribution=data["tef"]["distribution"]
            ))
        
        if data["vulnerability"]:
            model.set_vulnerability(VulnerabilityInput(
                min_value=data["vulnerability"]["min_value"],
                max_value=data["vulnerability"]["max_value"],
                most_likely=data["vulnerability"]["most_likely"],
                distribution=data["vulnerability"]["distribution"]
            ))
        
        if data["loss_magnitude"]:
            model.set_loss_magnitude(LossInput(
                min_value=data["loss_magnitude"]["min_value"],
                max_value=data["loss_magnitude"]["max_value"],
                most_likely=data["loss_magnitude"]["most_likely"],
                distribution=data["loss_magnitude"]["distribution"]
            ))
        
        return model
