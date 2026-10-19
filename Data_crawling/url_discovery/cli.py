"""Standalone CLI: validate first, save partial discoveries on interruption."""

import argparse
import json
import os
import sys
import uuid
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from .core import Inventory, load_config, workspace_path
from .providers import collect_map, run_browser


def main(argv=None, *, workspace: Path | None = None) -> int:
    workspace = (workspace or Path(__file__).resolve().parents[1]).resolve()
    parser = argparse.ArgumentParser(
        description="Discover public company URLs; exports URLs and discovery metadata only."
    )
    parser.add_argument(
        "--config",
        default="configs/cellphones.toml",
        help="TOML path relative to this standalone workspace",
    )
    parser.add_argument("--mode", choices=["map", "browser", "combined"], default="map")
    parser.add_argument(
        "--output-dir", help="Override the output parent directory, inside this workspace"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and show configuration without network calls or file writes",
    )
    args = parser.parse_args(argv)
    try:
        config = load_config(workspace, args.config)
        output_parent = workspace_path(workspace, args.output_dir or config.output_dir)
    except (OSError, ValueError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2
    if args.dry_run:
        print(
            json.dumps(
                {
                    "mode": args.mode,
                    "workspace": str(workspace),
                    "output_parent": str(output_parent),
                    "config": asdict(config),
                    "network_requests": 0,
                },
                indent=2,
            )
        )
        return 0
    api_key = os.environ.get("FIRECRAWL_API_KEY", "").strip()
    if args.mode in {"map", "combined"} and not api_key:
        print(
            "Set FIRECRAWL_API_KEY in your terminal environment before using map or combined mode. No .env files are loaded automatically.",
            file=sys.stderr,
        )
        return 2

    # Ubuntu's trust store may be newer than the base Anaconda interpreter's.
    # These defaults affect this process and its Playwright child only.
    system_ca = Path("/etc/ssl/certs/ca-certificates.crt")
    if system_ca.is_file():
        os.environ.setdefault("SSL_CERT_FILE", str(system_ca))
        os.environ.setdefault("NODE_EXTRA_CA_CERTS", str(system_ca))

    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    directory = output_parent / run_id
    try:
        directory.mkdir(parents=True, exist_ok=False)
    except OSError as error:
        print(f"Cannot create output directory ({type(error).__name__}).", file=sys.stderr)
        return 2
    inventory = Inventory(config.allowed_hosts)
    report = {
        "run_id": run_id,
        "mode": args.mode,
        "started_at": datetime.now(UTC).isoformat(),
        "configuration": asdict(config),
        "stages": [],
        "errors": [],
        "coverage_complete": False,
    }
    exit_code = 0
    stage = "setup"
    try:
        if args.mode in {"map", "combined"}:
            stage = "firecrawl"
            print("Discovering URLs with Firecrawl Map...", file=sys.stderr)
            report["stages"].append(collect_map(config, inventory, api_key))
            # Persist Map output before starting the longer browser phase.
            inventory.write(
                directory, {**report, "status": "running", "url_count": len(inventory.urls)}
            )
        if args.mode in {"browser", "combined"}:
            stage = "playwright"
            print(
                f"Discovering rendered links with Playwright (up to {config.browser_max_pages} pages)...",
                file=sys.stderr,
            )
            report["stages"].append(run_browser(config, inventory, workspace))
        report["errors"].extend(
            error for result in report["stages"] for error in result.get("errors", [])
        )
        limited = any(result.get("limit_reached") for result in report["stages"])
        report["status"] = "partial" if report["errors"] else "limited" if limited else "completed"
        exit_code = 1 if report["errors"] else 0
    except KeyboardInterrupt:
        report["status"] = "interrupted"
        exit_code = 130
    except Exception as error:
        report["status"] = "partial" if inventory.urls else "failed"
        message = str(error) if isinstance(error, RuntimeError) else type(error).__name__
        report["errors"].append({"stage": stage, "error": message})
        print(message, file=sys.stderr)
        exit_code = 1
    finally:
        stage_errors = [error for result in report["stages"] for error in result.get("errors", [])]
        report["errors"] = stage_errors + [
            error for error in report["errors"] if error not in stage_errors
        ]
        report["finished_at"] = datetime.now(UTC).isoformat()
        report["url_count"] = len(inventory.urls)
        saved = True
        try:
            inventory.write(directory, report)
        except OSError as error:
            print(f"Could not save all outputs ({type(error).__name__}).", file=sys.stderr)
            report["status"] = "failed"
            saved = False
            exit_code = 1
    output_label = "Output" if saved else "Output not fully saved"
    print(f"{report['status']}: {len(inventory.urls)} unique URLs. {output_label}: {directory}")
    print("This is a discovery inventory, not proof of complete website coverage.")
    return exit_code
