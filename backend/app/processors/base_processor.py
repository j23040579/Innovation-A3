from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd

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
    def transform(self, weather_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Transforms raw weather dictionary into a one-row DataFrame whose
        columns match the training feature names and order.
        """
        pass
