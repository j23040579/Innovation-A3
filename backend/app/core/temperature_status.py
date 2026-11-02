"""Meteorological temperature status labels used beside predicted °C values."""

from typing import Optional

# Rank is used only so freeze/heat statuses can still contribute to overall risk.
STATUS_SEVERITY = {
    "Frozen": 3,
    "Severe Cold": 2,
    "Hard Freeze": 2,
    "Light Freeze": 1,
    "Cold": 0,
    "Mild": 0,
    "Warm": 1,
}


def classify_temperature(temp_c: Optional[float]) -> str:
    """
    Classify a temperature in °C.

    Frozen: commercial frozen-storage threshold at or below -18°C.
    Severe Cold: official severe-cold threshold at or below -5°C.
    Hard Freeze: below -2.2°C (28°F).
    Light Freeze: -2.2°C through 0°C.
    Cold: above freezing through 16°C.
    Mild: above 16°C and below 27°C.
    Warm: 27°C and above.
    """
    if temp_c is None:
        return "Unknown"
    temp = float(temp_c)
    if temp <= -18:
        return "Frozen"
    if temp <= -5:
        return "Severe Cold"
    if temp < -2.2:
        return "Hard Freeze"
    if temp <= 0:
        return "Light Freeze"
    if temp <= 16:
        return "Cold"
    if temp < 27:
        return "Mild"
    return "Warm"


def temperature_alert(status: str) -> str:
    messages = {
        "Frozen": "Well below freezing; equivalent to commercial frozen-storage temperatures.",
        "Severe Cold": "Severe cold: ambient temperature at or below -5°C.",
        "Hard Freeze": "Hard freeze: temperature is below -2.2°C (28°F).",
        "Light Freeze": "Light freeze: temperature is at or below 0°C.",
        "Cold": "Cold conditions approaching or hovering above freezing.",
        "Mild": "Mild temperature, between cold and warm thresholds.",
        "Warm": "Warm conditions at or above 27°C.",
    }
    return messages.get(status, "Temperature status unavailable.")
