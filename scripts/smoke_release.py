"""Smoke test read-only cho CourseHub qua Nginx (Buổi 7)."""
import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def get_json(base_url: str, path: str):
    url = base_url.rstrip("/") + path
    with urlopen(url, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(f"GET {path}: HTTP {response.status}")
        return json.load(response)


def run(base_url: str):
    health = get_json(base_url, "/api/health")
    if not isinstance(health, dict):
        raise AssertionError("/api/health phải trả JSON object")
    print("PASS GET /api/health (HTTP 200 + JSON object)")
    sections = get_json(base_url, "/api/sections?available_only=true")
    if not isinstance(sections, list):
        raise AssertionError("/api/sections phải trả JSON array")
    if not all(isinstance(row, dict) and int(row["remaining"]) > 0
               for row in sections):
        raise AssertionError("Có lớp hết chỗ trong kết quả available_only=true")
    print(f"PASS GET /api/sections?available_only=true ({len(sections)} lớp)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CourseHub read-only smoke test")
    parser.add_argument(
        "--base-url",
        default=os.getenv("COURSEHUB_BASE_URL", "http://127.0.0.1:8080"),
    )
    args = parser.parse_args()
    try:
        run(args.base_url)
    except (HTTPError, URLError, ValueError, KeyError,
            AssertionError, RuntimeError, TimeoutError) as exc:
        print(f"FAIL smoke test: {exc}", file=sys.stderr)
        sys.exit(1)
