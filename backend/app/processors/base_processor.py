from abc import ABC, abstractmethod
from typing import Dict, Any, List
import numpy as np

class BaseProcessor(ABC):
    """
    Abstract Base Class for all Disaster Feature Processors.
    Backend 2 developers will inherit from this class to implement feature transformations.
    """

    @property
    @abstractmethod
    def required_features(self) -> List[str]:
        """List of meteorological features required in exact model input order."""
        pass

    @abstractmethod
    def transform(self, weather_data: Dict[str, Any]) -> np.ndarray:
        """
        Transforms raw weather dictionary into a 2D numpy array [1, num_features]
        ready for model.predict() or model.predict_proba().
        """
        pass
