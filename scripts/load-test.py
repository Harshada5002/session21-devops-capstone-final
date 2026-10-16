"""
Load-testing script for TaskBoard
-----------------------------------
Sends controlled HTTP traffic to the backend to trigger HPA scaling.
Uses only the Python standard library – no extra dependencies required.

Usage (PowerShell):
  python scripts\load-test.py --url http://localhost:8000 --rps 10 --duration 60

Usage (Linux/WSL):
  python scripts/load-test.py --url http://localhost:8000 --rps 10 --duration 60

For Kubernetes port-forward:
  kubectl port-forward svc/taskboard-backend 8000:8000 -n taskboard
  python scripts/load-test.py --url http://localhost:8000 --rps 20 --duration 120
"""

from __future__ import annotations

import argparse
import json
import random
import signal
import sys
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import List


# ── CLI arguments ─────────────────────────────────────────────────────────────
def parse_args():
    p = argparse.ArgumentParser(description="TaskBoard load tester")
    p.add_argument("--url",      default="http://localhost:8000", help="Base URL of the backend")
    p.add_argument("--rps",      type=float, default=5,           help="Requests per second")
    p.add_argument("--duration", type=int,   default=60,          help="Test duration in seconds")
    p.add_argument("--workers",  type=int,   default=4,           help="Concurrent worker threads")
    return p.parse_args()


# ── Statistics collector ──────────────────────────────────────────────────────
@dataclass
class Stats:
    lock: threading.Lock = field(default_factory=threading.Lock)
    total: int = 0
    ok: int = 0
    errors: int = 0
    latencies: List[float] = field(default_factory=list)

    def record(self, ok: bool, latency: float):
        with self.lock:
            self.total += 1
            if ok:
                self.ok += 1
            else:
                self.errors += 1
            self.latencies.append(latency)

    def summary(self) -> dict:
        with self.lock:
            lats = sorted(self.latencies)
            n = len(lats)
            return {
                "total":    self.total,
                "ok":       self.ok,
                "errors":   self.errors,
                "avg_ms":   round(sum(lats) / n * 1000, 1) if n else 0,
                "p95_ms":   round(lats[int(n * 0.95)] * 1000, 1) if n else 0,
                "p99_ms":   round(lats[int(n * 0.99)] * 1000, 1) if n else 0,
                "max_ms":   round(max(lats) * 1000, 1) if n else 0,
            }


# ── Request targets ───────────────────────────────────────────────────────────
def get_endpoints(base_url: str) -> List[dict]:
    return [
        {"method": "GET",  "path": "/health"},
        {"method": "GET",  "path": "/api/tasks"},
        {"method": "GET",  "path": "/api/tasks/stats"},
        {"method": "GET",  "path": "/api/tasks?status=TODO"},
        {"method": "GET",  "path": "/api/tasks?priority=HIGH"},
        {"method": "POST", "path": "/api/tasks", "body": {
            "title":    f"Load test task {random.randint(1000, 9999)}",
            "status":   random.choice(["TODO", "IN_PROGRESS"]),
            "priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
        }},
    ]


def do_request(base_url: str, endpoint: dict, stats: Stats):
    url = f"{base_url}{endpoint['path']}"
    method = endpoint["method"]
    body = endpoint.get("body")

    try:
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(
            url, data=data, method=method,
            headers={"Content-Type": "application/json"} if data else {},
        )
        start = time.perf_counter()
        with urllib.request.urlopen(req, timeout=5) as resp:
            resp.read()
            ok = resp.status < 400
        latency = time.perf_counter() - start
        stats.record(ok, latency)
    except urllib.error.HTTPError as e:
        # 4xx errors are expected (e.g. 404) – not a load test failure
        ok = e.code < 500
        stats.record(ok, 0.0)
    except Exception:
        stats.record(False, 0.0)


# ── Worker thread ─────────────────────────────────────────────────────────────
def worker(base_url: str, stats: Stats, stop_event: threading.Event,
           interval: float):
    endpoints = get_endpoints(base_url)
    while not stop_event.is_set():
        endpoint = random.choice(endpoints)
        do_request(base_url, endpoint, stats)
        time.sleep(interval)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    args = parse_args()
    stats = Stats()
    stop_event = threading.Event()
    interval = args.workers / args.rps  # each worker's sleep between requests

    print(f"\n{'='*55}")
    print(f"  TaskBoard Load Test")
    print(f"{'='*55}")
    print(f"  Target:   {args.url}")
    print(f"  RPS:      {args.rps} (approx)")
    print(f"  Duration: {args.duration}s")
    print(f"  Workers:  {args.workers}")
    print(f"{'='*55}\n")
    print("Starting… Press Ctrl+C to stop early.\n")

    def handle_signal(sig, frame):
        print("\nStopping…")
        stop_event.set()

    signal.signal(signal.SIGINT, handle_signal)

    threads = [
        threading.Thread(target=worker, args=(args.url, stats, stop_event, interval), daemon=True)
        for _ in range(args.workers)
    ]
    for t in threads:
        t.start()

    start_time = time.time()
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        if elapsed >= args.duration:
            stop_event.set()
            break
        s = stats.summary()
        print(
            f"\r  [{elapsed:5.1f}s] Requests: {s['total']:5d} | "
            f"OK: {s['ok']:5d} | Errors: {s['errors']:3d} | "
            f"Avg: {s['avg_ms']:6.1f}ms | P95: {s['p95_ms']:6.1f}ms",
            end="", flush=True
        )
        time.sleep(0.5)

    for t in threads:
        t.join(timeout=2)

    s = stats.summary()
    print(f"\n\n{'='*55}")
    print("  Load Test Complete")
    print(f"{'='*55}")
    print(f"  Total requests : {s['total']}")
    print(f"  Successful     : {s['ok']}")
    print(f"  Errors         : {s['errors']}")
    print(f"  Avg latency    : {s['avg_ms']} ms")
    print(f"  P95 latency    : {s['p95_ms']} ms")
    print(f"  P99 latency    : {s['p99_ms']} ms")
    print(f"  Max latency    : {s['max_ms']} ms")
    print(f"{'='*55}\n")

    if s['errors'] > s['total'] * 0.1:
        print("⚠  WARNING: Error rate > 10%. Check backend logs.")
        sys.exit(1)


if __name__ == "__main__":
    main()
