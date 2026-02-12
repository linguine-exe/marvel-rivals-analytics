"""Command-line interface for Marvel Rivals Analytics."""

from __future__ import annotations

import argparse

from .utils.config import get_settings
from .utils.logging import setup_logging


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="marvel_rivals_analytics",
        description="Marvel Rivals Analytics CLI",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (default: INFO)",
    )

    subparsers = parser.add_subparsers(dest="command")

    ping_parser = subparsers.add_parser("ping", help="Sanity-check the CLI wiring")
    ping_parser.set_defaults(func=cmd_ping)

    return parser


def cmd_ping(_: argparse.Namespace) -> int:
    """Handle the `ping` command."""
    settings = get_settings()
    print("pong")
    if settings.api_base_url:
        print(f"api_base_url={settings.api_base_url}")
    else:
        print("api_base_url=<not set>")
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    setup_logging(args.log_level)

    if hasattr(args, "func"):
        return args.func(args)

    parser.print_help()
    return 0
