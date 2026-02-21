"""Core risk model for pulse and blood pressure inputs."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RiskAssessment:
    """Represents model output for cardiovascular risk screening."""

    risk_score: int
    risk_level: str
    reasons: List[str]


def _bp_category(systolic: int, diastolic: int) -> str:
    """Return a blood pressure category string based on threshold checks."""
    if systolic >= 140 or diastolic >= 90:
        return "stage_2"
    if 130 <= systolic <= 139 or 80 <= diastolic <= 89:
        return "stage_1"
    if 120 <= systolic <= 129 and diastolic < 80:
        return "elevated"
    return "normal"


def assess_cardiovascular_risk(
    heart_rate: int,
    systolic_bp: int,
    diastolic_bp: int,
) -> RiskAssessment:
    """
    Compute a simple rule-based risk assessment.

    Parameters
    ----------
    heart_rate:
        Resting pulse in beats per minute.
    systolic_bp:
        Systolic blood pressure in mmHg.
    diastolic_bp:
        Diastolic blood pressure in mmHg.
    """
    if heart_rate <= 0 or systolic_bp <= 0 or diastolic_bp <= 0:
        raise ValueError("All inputs must be positive integers.")

    score = 0
    reasons: List[str] = []

    if heart_rate >= 120:
        score += 3
        reasons.append("Very high resting heart rate (>= 120 bpm)")
    elif heart_rate >= 100:
        score += 2
        reasons.append("High resting heart rate (>= 100 bpm)")
    elif heart_rate < 50:
        score += 2
        reasons.append("Low pulse/bradycardia range (< 50 bpm)")

    category = _bp_category(systolic_bp, diastolic_bp)
    if category == "stage_2":
        score += 3
        reasons.append("Stage 2 hypertension threshold reached")
    elif category == "stage_1":
        score += 2
        reasons.append("Stage 1 hypertension threshold reached")
    elif category == "elevated":
        score += 1
        reasons.append("Elevated blood pressure range")

    if heart_rate >= 100 and category == "stage_2":
        score += 1
        reasons.append("Combined pulse and blood pressure stress")

    if score <= 1:
        level = "low"
    elif score <= 3:
        level = "moderate"
    else:
        level = "high"

    if not reasons:
        reasons.append("Vitals within nominal screening ranges")

    return RiskAssessment(risk_score=score, risk_level=level, reasons=reasons)
