"""Command-line interface for Marvel Rivals Analytics."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analytics.maps import MapsDataError, analyze_maps_to_csv
from .api_client import ApiClient, ApiClientError
from .raw_saver import save_raw_json, save_request_metadata
from .utils.config import get_settings
from .utils.files import FileDiscoveryError, find_latest_raw_file
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

    fetch_parser = subparsers.add_parser("fetch", help="Fetch raw endpoint JSON and save it")
    fetch_parser.add_argument("path", help="Endpoint path such as /maps or maps")
    fetch_parser.add_argument(
        "--params",
        nargs="*",
        default=[],
        metavar="KEY=VALUE",
        help="Query parameters as key=value entries",
    )
    fetch_parser.add_argument(
        "--outdir",
        default="data/raw",
        help="Directory for raw output files (default: data/raw)",
    )
    fetch_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print request details without making an API call",
    )
    fetch_parser.set_defaults(func=cmd_fetch)

    analyze_parser = subparsers.add_parser("analyze", help="Analyze saved raw JSON files")
    analyze_subparsers = analyze_parser.add_subparsers(dest="analyze_target")

    analyze_maps_parser = analyze_subparsers.add_parser(
        "maps", help="Transform saved /maps payloads into CSV tables"
    )
    analyze_maps_parser.add_argument(
        "--latest",
        action="store_true",
        help="Use latest maps_*.json from data/raw (default behavior)",
    )
    analyze_maps_parser.add_argument(
        "--infile",
        type=Path,
        help="Path to a specific raw maps JSON file",
    )
    analyze_maps_parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("data/raw"),
        help="Directory containing raw files (default: data/raw)",
    )
    analyze_maps_parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("data/processed"),
        help="Directory for processed outputs (default: data/processed)",
    )
    analyze_maps_parser.set_defaults(func=cmd_analyze_maps)

    return parser


def _parse_params(items: list[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid --params entry '{item}'. Expected key=value.")
        key, value = item.split("=", 1)
        if not key:
            raise ValueError(f"Invalid --params entry '{item}'. Key cannot be empty.")
        params[key] = value
    return params


def cmd_ping(_: argparse.Namespace) -> int:
    """Handle the `ping` command."""
    settings = get_settings()
    print("pong")
    if settings.api_base_url:
        print(f"api_base_url={settings.api_base_url}")
    else:
        print("api_base_url=<not set>")
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    """Handle the `fetch` command."""
    settings = get_settings()
    if not settings.api_base_url:
        raise ValueError("MR_API_BASE_URL must be set")

    params = _parse_params(args.params)
    api_key_set = bool(settings.api_key)

    client = ApiClient(base_url=settings.api_base_url, api_key=settings.api_key or "")
    final_url = client.build_url(args.path)

    print(f"url={final_url}")
    print(f"x-api-key={'set' if api_key_set else 'missing'}")
    if params:
        print(f"params={params}")

    if args.dry_run:
        return 0

    outdir = Path(args.outdir)
    result = client.request(args.path, params=params or None)

    if result.status_code != 200:
        metadata_path = save_request_metadata(
            outdir=outdir,
            endpoint=args.path,
            url=result.url,
            params=params or None,
            status_code=result.status_code,
            response_text=result.response_text,
            saved_file=None,
        )
        raise ApiClientError(
            f"API request failed ({result.status_code}) for {result.url}. "
            f"Metadata saved to {metadata_path}."
        )

    if result.json_data is None:
        raise ApiClientError(f"API returned empty JSON payload for {result.url}")

    data_path, metadata_path = save_raw_json(
        outdir=outdir,
        endpoint=args.path,
        payload=result.json_data,
        url=result.url,
        params=params or None,
        status_code=result.status_code,
    )
    print(f"saved_json={data_path}")
    print(f"saved_metadata={metadata_path}")
    return 0


def cmd_analyze_maps(args: argparse.Namespace) -> int:
    """Handle the `analyze maps` command."""
    infile = args.infile
    if infile is None or args.latest:
        infile = find_latest_raw_file(endpoint_slug="maps", raw_dir=args.raw_dir)

    maps_csv, summary_csv, row_count = analyze_maps_to_csv(infile=infile, processed_dir=args.outdir)

    print(f"input_file={infile}")
    print(f"maps_rows={row_count}")
    print(f"saved_table={maps_csv}")
    print(f"saved_summary={summary_csv}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    setup_logging(args.log_level)

    try:
        if hasattr(args, "func"):
            return args.func(args)
    except (ValueError, ApiClientError, FileDiscoveryError, MapsDataError) as exc:
        parser.error(str(exc))

    parser.print_help()
    return 0
