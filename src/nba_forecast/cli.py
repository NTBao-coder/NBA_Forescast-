"""Command-line entry point for the NBA forecasting project."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="nba-forecast",
        description="Forecast the probability that the home NBA team wins.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    return parser


def main() -> None:
    """Run the command-line interface."""
    build_parser().parse_args()
