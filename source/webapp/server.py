"""The local HTTP server behind the Hull Cut Workbench.

Standard library only -- the workbench should start on a bare Python with
nothing but this repository checked out.
"""

import json
import os
import posixpath
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from source.webapp import tsp_service
from source.webapp.jobs import JobManager

STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}

DEFAULT_TIME_LIMIT = 120


class WorkbenchHandler(BaseHTTPRequestHandler):
    server_version = "HullCutWorkbench/1.0"
    protocol_version = "HTTP/1.1"

    # Quiet by default: main.pyw runs windowless, where there is no console to
    # log to. --verbose flips this on.
    def log_message(self, fmt, *args):
        if getattr(self.server, "verbose", False):
            BaseHTTPRequestHandler.log_message(self, fmt, *args)

    # ---- plumbing ----------------------------------------------------

    def _send(self, status, body, content_type):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, payload, status=200):
        self._send(status, json.dumps(payload), "application/json; charset=utf-8")

    def _error(self, status, message):
        self._json({"error": message}, status=status)

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    # ---- routes ------------------------------------------------------

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/config":
            return self._json(
                {
                    "strategies": tsp_service.strategy_catalogue(),
                    "minCities": tsp_service.MIN_CITIES,
                    "maxCities": tsp_service.MAX_CITIES,
                    "bruteForceLimit": tsp_service.BRUTE_FORCE_LIMIT,
                    "defaultTimeLimit": DEFAULT_TIME_LIMIT,
                }
            )
        if path.startswith("/api/job/"):
            job = self.server.jobs.get(path[len("/api/job/"):])
            if job is None:
                return self._error(404, "That job is no longer being tracked.")
            return self._json(job.snapshot())
        if path.startswith("/api/"):
            return self._error(404, "No such endpoint.")
        return self._serve_static(path)

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        try:
            payload = self._read_json()
        except ValueError:
            return self._error(400, "The request body was not valid JSON.")

        if path == "/api/instance":
            return self._make_instance(payload)
        if path == "/api/solve":
            return self._start(payload, "solve")
        if path == "/api/suite":
            return self._start(payload, "suite")
        if path.startswith("/api/cancel/"):
            cancelled = self.server.jobs.cancel(path[len("/api/cancel/"):])
            return self._json({"cancelled": cancelled})
        if path == "/api/shutdown":
            self._json({"stopping": True})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return None
        return self._error(404, "No such endpoint.")

    # ---- handlers ----------------------------------------------------

    def _make_instance(self, payload):
        """Points only, no solve -- so the plot can react as parameters change."""
        try:
            if payload.get("mode") == "custom":
                points, _ = tsp_service.build_instance_from_points(payload["coords"])
            else:
                points, _ = tsp_service.build_random_instance(
                    payload.get("size", 8), payload.get("seed", 1)
                )
        except tsp_service.InstanceError as error:
            return self._error(400, str(error))
        except (KeyError, TypeError, ValueError):
            return self._error(400, "The instance parameters were incomplete.")
        return self._json({"points": points})

    def _start(self, payload, kind):
        payload["kind"] = kind
        try:
            limit = float(payload.get("timeLimit") or 0) or None
        except (TypeError, ValueError):
            limit = DEFAULT_TIME_LIMIT
        job = self.server.jobs.start(payload, time_limit=limit)
        return self._json(job.snapshot(), status=202)

    def _serve_static(self, path):
        if path in ("/", ""):
            path = "/index.html"
        clean = posixpath.normpath(path).lstrip("/")
        target = os.path.join(STATIC_ROOT, *clean.split("/"))
        if not os.path.abspath(target).startswith(os.path.abspath(STATIC_ROOT)):
            return self._error(403, "Forbidden.")
        if not os.path.isfile(target):
            return self._error(404, "Not found.")
        extension = os.path.splitext(target)[1].lower()
        with open(target, "rb") as handle:
            body = handle.read()
        return self._send(200, body, CONTENT_TYPES.get(extension, "application/octet-stream"))


class Workbench(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address, verbose=False):
        ThreadingHTTPServer.__init__(self, address, WorkbenchHandler)
        self.jobs = JobManager()
        self.verbose = verbose


def find_free_port(preferred, host="127.0.0.1"):
    """Use the preferred port when it is free, otherwise let the OS pick one."""
    for candidate in (preferred, 0):
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            probe.bind((host, candidate))
            return probe.getsockname()[1]
        except OSError:
            continue
        finally:
            probe.close()
    return preferred


def serve(host="127.0.0.1", port=8731, verbose=False):
    server = Workbench((host, port), verbose=verbose)
    return server
