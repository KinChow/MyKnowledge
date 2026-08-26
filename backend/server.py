"""Reproducible loopback runner for the F006 local API."""
from __future__ import annotations

import argparse
import ipaddress
from pathlib import Path

from .app import create_app


def _loopback_host(value: str) -> str:
    """Accept only loopback bind addresses; the API is never a public server."""
    if value == "localhost":
        return value
    try:
        address = ipaddress.ip_address(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("host must be localhost or a loopback IP") from exc
    if not address.is_loopback:
        raise argparse.ArgumentTypeError("remote bind is disabled; use 127.0.0.1")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the MyKnowledge local API")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--host", type=_loopback_host, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")

    import uvicorn

    uvicorn.run(create_app(root=args.root), host=args.host, port=args.port,
                log_level="info", reload=False, proxy_headers=False)
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised by network integration test
    raise SystemExit(main())
