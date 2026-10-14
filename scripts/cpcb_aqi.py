"""Official CPCB National Air Quality Index (NAQI) Calculation Engine.

Implements the official Indian Central Pollution Control Board (CPCB) methodology:
- Breakpoints and linear segmented sub-index formula
- Mandatory data validity rules (>= 3 criteria pollutants, mandatory PM2.5 or PM10)
- Prominent pollutant identification
- Dimensionless AQI and categorical health tier assignment
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

# CPCB Breakpoints: (B_lo, B_hi, I_lo, I_hi)
# Concentrations for PM10, PM2.5, NO2, SO2, O3 in µg/m³; CO in mg/m³
BREAKPOINTS: Dict[str, List[Tuple[float, float, float, float]]] = {
    "pm10": [
        (0.0, 50.0, 0.0, 50.0),
        (51.0, 100.0, 51.0, 100.0),
        (101.0, 250.0, 101.0, 200.0),
        (251.0, 350.0, 201.0, 300.0),
        (351.0, 430.0, 301.0, 400.0),
        (431.0, 600.0, 401.0, 500.0),
    ],
    "pm25": [
        (0.0, 30.0, 0.0, 50.0),
        (31.0, 60.0, 51.0, 100.0),
        (61.0, 90.0, 101.0, 200.0),
        (91.0, 120.0, 201.0, 300.0),
        (121.0, 250.0, 301.0, 400.0),
        (251.0, 500.0, 401.0, 500.0),
    ],
    "no2": [
        (0.0, 40.0, 0.0, 50.0),
        (41.0, 80.0, 51.0, 100.0),
        (81.0, 180.0, 101.0, 200.0),
        (181.0, 280.0, 201.0, 300.0),
        (281.0, 400.0, 301.0, 400.0),
        (401.0, 600.0, 401.0, 500.0),
    ],
    "so2": [
        (0.0, 40.0, 0.0, 50.0),
        (41.0, 80.0, 51.0, 100.0),
        (81.0, 380.0, 101.0, 200.0),
        (381.0, 800.0, 201.0, 300.0),
        (801.0, 1600.0, 301.0, 400.0),
        (1601.0, 2000.0, 401.0, 500.0),
    ],
    "co": [
        (0.0, 1.0, 0.0, 50.0),
        (1.1, 2.0, 51.0, 100.0),
        (2.1, 10.0, 101.0, 200.0),
        (10.1, 17.0, 201.0, 300.0),
        (17.1, 34.0, 301.0, 400.0),
        (34.1, 50.0, 401.0, 500.0),
    ],
    "o3": [
        (0.0, 50.0, 0.0, 50.0),
        (51.0, 100.0, 51.0, 100.0),
        (101.0, 168.0, 101.0, 200.0),
        (169.0, 208.0, 201.0, 300.0),
        (209.0, 748.0, 301.0, 400.0),
        (749.0, 1000.0, 401.0, 500.0),
    ],
}

HEALTH_CATEGORIES = [
    (0, 50, "Good", 0),
    (51, 100, "Satisfactory", 1),
    (101, 200, "Moderate", 2),
    (201, 300, "Poor", 3),
    (301, 400, "Very Poor", 4),
    (401, 500, "Severe", 5),
]


def calculate_sub_index(parameter: str, concentration: Optional[float]) -> Optional[float]:
    """Calculate the sub-index for a specific pollutant using linear segmented interpolation."""
    if concentration is None or concentration < 0:
        return None

    param = parameter.lower()
    brackets = BREAKPOINTS.get(param)
    if not brackets:
        return None

    # Handle concentrations exceeding the top breakpoint
    max_b_hi = brackets[-1][1]
    if concentration >= max_b_hi:
        return 500.0

    for b_lo, b_hi, i_lo, i_hi in brackets:
        if b_lo <= concentration <= b_hi:
            sub_index = ((i_hi - i_lo) / (b_hi - b_lo)) * (concentration - b_lo) + i_lo
            return round(sub_index, 2)

    return None


def calculate_cpcb_aqi(
    concentrations: Dict[str, Optional[float]],
) -> Tuple[Optional[float], Optional[str], Optional[str], Optional[int], Dict[str, float]]:
    """Compute overall CPCB NAQI following regulatory completeness rules.

    Returns:
        (aqi_value, health_category, prominent_pollutant, category_code, sub_indices_dict)
    """
    sub_indices: Dict[str, float] = {}

    for param, conc in concentrations.items():
        sub_idx = calculate_sub_index(param, conc)
        if sub_idx is not None:
            sub_indices[param] = sub_idx

    # CPCB Rule 1: Minimum of 3 criteria pollutants required
    if len(sub_indices) < 3:
        return (None, None, None, None, sub_indices)

    # CPCB Rule 2: At least one must be PM2.5 or PM10
    if "pm25" not in sub_indices and "pm10" not in sub_indices:
        return (None, None, None, None, sub_indices)

    # CPCB Rule 3: Overall AQI is the maximum of the sub-indices
    prominent_pollutant, max_sub_idx = max(sub_indices.items(), key=lambda kv: kv[1])
    aqi_value = round(max_sub_idx, 1)

    # Category determination
    health_category = "Severe"
    category_code = 5
    for lo, hi, label, code in HEALTH_CATEGORIES:
        if lo <= round(aqi_value) <= hi:
            health_category = label
            category_code = code
            break

    return (aqi_value, health_category, prominent_pollutant, category_code, sub_indices)
