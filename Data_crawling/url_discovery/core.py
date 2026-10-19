"""Configuration, URL identity, inventory, and local-only exports."""

import json
import math
import re
import tomllib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import quote, unquote_plus, urljoin, urlsplit, urlunsplit

TRACKING_KEYS = {"fbclid", "gclid", "dclid", "msclkid"}


def normalize_url(value: str, base: str = "") -> str | None:
    """Normalize identity without collapsing meaningful paths or query ordering."""
    if not isinstance(value, str) or any(ord(char) < 32 for char in value) or "\\" in value:
        return None
    try:
        parts = urlsplit(urljoin(base, value.strip()))
        if (
            parts.scheme not in {"http", "https"}
            or not parts.hostname
            or parts.username is not None
            or parts.password is not None
        ):
            return None
        host = parts.hostname.encode("idna").decode("ascii").lower()
        if any(char.isspace() for char in host):
            return None
        port = parts.port
        if ":" in host:
            host = f"[{host}]"
        if port is not None and port != {"http": 80, "https": 443}[parts.scheme]:
            host = f"{host}:{port}"
        query = []
        for component in parts.query.split("&") if parts.query else []:
            key = unquote_plus(component.split("=", 1)[0]).lower()
            if not key.startswith("utm_") and key not in TRACKING_KEYS:
                query.append(component)
        return urlunsplit(
            (
                parts.scheme,
                host,
                quote(parts.path or "/", safe="/%:@!$&'()*+,;=-._~"),
                quote("&".join(query), safe="%=&/:?@!$'()*+,;~-._"),
                "",
            )
        )
    except (ValueError, UnicodeError):
        return None


def workspace_path(workspace: Path, value: str) -> Path:
    root = workspace.resolve()
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Configuration and output paths must stay inside Data_crawling.")
    return path


@dataclass
class Config:
    allowed_hosts: list[str]
    seed_urls: list[str]
    output_dir: str = "outputs"
    browser_seed_urls: list[str] = field(default_factory=list)
    map_limit: int = 100000
    map_timeout: float = 60
    browser_max_pages: int = 100
    browser_delay: float = 1
    browser_timeout: float = 30
    render_wait_ms: int = 750
    scroll_steps: int = 2
    hover_selectors: list[str] = field(default_factory=list)


def load_config(workspace: Path, filename: str) -> Config:
    with workspace_path(workspace, filename).open("rb") as stream:
        data = tomllib.load(stream)
    hosts = data.get("allowed_hosts", [])
    if (
        not isinstance(hosts, list)
        or not hosts
        or any(
            not isinstance(host, str)
            or not re.fullmatch(r"[a-z0-9]+(?:[a-z0-9.-]*[a-z0-9])?", host)
            for host in hosts
        )
    ):
        raise ValueError(
            "allowed_hosts must contain exact lowercase hostnames, without schemes or ports."
        )
    firecrawl = data.get("firecrawl", {})
    browser = data.get("browser", {})
    if not isinstance(firecrawl, dict) or not isinstance(browser, dict):
        raise ValueError("firecrawl and browser must be TOML tables.")
    known_root = {"allowed_hosts", "seed_urls", "output_dir", "firecrawl", "browser"}
    if (
        data.keys() - known_root
        or firecrawl.keys() - {"limit", "timeout_seconds"}
        or browser.keys()
        - {
            "seed_urls",
            "max_pages",
            "delay_seconds",
            "timeout_seconds",
            "render_wait_ms",
            "scroll_steps",
            "hover_selectors",
        }
    ):
        raise ValueError(
            "Unknown configuration setting; check configs/cellphones.toml for supported keys."
        )
    config = Config(
        allowed_hosts=hosts,
        seed_urls=data.get("seed_urls", []),
        output_dir=data.get("output_dir", "outputs"),
        browser_seed_urls=browser.get("seed_urls", []),
        map_limit=firecrawl.get("limit", 100000),
        map_timeout=firecrawl.get("timeout_seconds", 60),
        browser_max_pages=browser.get("max_pages", 100),
        browser_delay=browser.get("delay_seconds", 1),
        browser_timeout=browser.get("timeout_seconds", 30),
        render_wait_ms=browser.get("render_wait_ms", 750),
        scroll_steps=browser.get("scroll_steps", 2),
        hover_selectors=browser.get("hover_selectors", []),
    )
    scope = Inventory(hosts)
    for name in ("seed_urls", "browser_seed_urls"):
        seeds = getattr(config, name)
        if (
            not isinstance(seeds, list)
            or (name == "seed_urls" and not seeds)
            or any(not isinstance(url, str) or not scope.accepts(url) for url in seeds)
        ):
            raise ValueError(f"{name} must contain HTTP(S) URLs within allowed_hosts.")
        setattr(config, name, list(dict.fromkeys(normalize_url(url) for url in seeds)))
    for name, minimum, maximum in (
        ("map_limit", 1, 100000),
        ("browser_max_pages", 1, 1000000),
        ("render_wait_ms", 0, 60000),
        ("scroll_steps", 0, 100),
    ):
        value = getattr(config, name)
        if type(value) is not int or not minimum <= value <= maximum:
            raise ValueError(f"{name} must be an integer between {minimum} and {maximum}.")
    for name, minimum in (("map_timeout", 1), ("browser_timeout", 1), ("browser_delay", 0)):
        value = getattr(config, name)
        if type(value) not in (int, float) or not math.isfinite(value) or value < minimum:
            raise ValueError(f"{name} must be a finite number >= {minimum}.")
    if not isinstance(config.hover_selectors, list) or any(
        not isinstance(selector, str) or not selector.strip() for selector in config.hover_selectors
    ):
        raise ValueError("hover_selectors must be a list of nonempty CSS selectors.")
    if not isinstance(config.output_dir, str):
        raise ValueError("output_dir must be a local path.")
    workspace_path(workspace, config.output_dir)
    return config


class Inventory:
    def __init__(self, allowed_hosts: list[str]):
        self.allowed_hosts = set(allowed_hosts)
        self._entries: dict[str, dict] = {}

    def accepts(self, url: str) -> bool:
        normalized = normalize_url(url)
        if not normalized:
            return False
        parts = urlsplit(normalized)
        return parts.hostname in self.allowed_hosts and parts.port is None

    def add(self, url: str, source: str, discovered_from: str = "") -> str | None:
        normalized = normalize_url(url, discovered_from)
        if not normalized or not self.accepts(normalized):
            return None
        entry = self._entries.setdefault(
            normalized,
            {
                "url": normalized,
                "sources": set(),
                "first_discovered_at": datetime.now(UTC).isoformat(),
                "discovered_from": discovered_from,
            },
        )
        entry["sources"].add(source)
        return normalized

    @property
    def urls(self) -> list[str]:
        return sorted(self._entries)

    def records(self) -> list[dict]:
        return [
            {**self._entries[url], "sources": sorted(self._entries[url]["sources"])}
            for url in self.urls
        ]

    def write(self, directory: Path, report: dict) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "urls.txt").write_text(
            "".join(url + "\n" for url in self.urls), encoding="utf-8"
        )
        with (directory / "urls.jsonl").open("w", encoding="utf-8") as stream:
            for record in self.records():
                stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        (directory / "report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
