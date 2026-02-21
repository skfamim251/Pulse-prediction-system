from pulse_prediction.model import assess_cardiovascular_risk


def test_high_risk_for_tachycardia_and_stage2_hypertension() -> None:
    result = assess_cardiovascular_risk(heart_rate=112, systolic_bp=168, diastolic_bp=104)

    assert result.risk_level == "high"
    assert result.risk_score >= 5
    assert any("Combined pulse and blood pressure stress" in r for r in result.reasons)


def test_low_risk_in_normal_ranges() -> None:
    result = assess_cardiovascular_risk(heart_rate=72, systolic_bp=118, diastolic_bp=76)

    assert result.risk_level == "low"
    assert result.risk_score == 0


def test_invalid_inputs_raise() -> None:
    try:
        assess_cardiovascular_risk(heart_rate=0, systolic_bp=120, diastolic_bp=80)
    except ValueError as exc:
        assert "positive integers" in str(exc)
    else:
        raise AssertionError("Expected ValueError for zero heart rate")
