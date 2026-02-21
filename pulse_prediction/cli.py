"""Command-line interface for pulse prediction risk scoring."""

import argparse

from .model import assess_cardiovascular_risk


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pulse and BP risk screening tool")
    parser.add_argument("--heart-rate", type=int, required=True, help="Heart rate in bpm")
    parser.add_argument("--systolic", type=int, required=True, help="Systolic BP in mmHg")
    parser.add_argument("--diastolic", type=int, required=True, help="Diastolic BP in mmHg")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    assessment = assess_cardiovascular_risk(
        heart_rate=args.heart_rate,
        systolic_bp=args.systolic,
        diastolic_bp=args.diastolic,
    )

    print(f"Risk level : {assessment.risk_level}")
    print(f"Risk score : {assessment.risk_score}")
    print("Reasons:")
    for reason in assessment.reasons:
        print(f" - {reason}")


if __name__ == "__main__":
    main()
