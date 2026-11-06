"""Command-line entry point for the Air Quality baseline pipeline."""

import argparse
import json

from air_quality.workflows import PipelineConfig, run_baseline, run_advanced, AdvancedPipelineConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Air Quality baseline pipeline")
    parser.add_argument("--train-city", default="Kampala")
    parser.add_argument("--test-city", default="Nairobi")
    parser.add_argument("--advanced", action="store_true",help="run the advanced pipeline (run_advanced) instead of the baseline",)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.advanced:
        metrics = run_advanced()
    else:
        config = PipelineConfig(train_city=args.train_city, test_city=args.test_city)
        metrics = run_baseline(config)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
