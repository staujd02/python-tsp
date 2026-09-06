"""Tracks the solver subprocesses so the UI can watch, cancel, and time them out."""

import json
import os
import subprocess
import sys
import threading
import time
from uuid import uuid4

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _worker_python():
    """Prefer python.exe over pythonw.exe so the child keeps usable pipes."""
    executable = sys.executable
    directory, name = os.path.split(executable)
    if name.lower() == "pythonw.exe":
        console = os.path.join(directory, "python.exe")
        if os.path.exists(console):
            return console
    return executable


def _no_window_flags():
    if os.name == "nt":
        return getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    return 0


class Job(object):
    def __init__(self, kind):
        self.id = uuid4().hex[:12]
        self.kind = kind
        self.state = "running"
        self.progress = {"done": 0, "total": 0, "message": "Starting"}
        self.result = None
        self.error = None
        self.detail = None
        self.points = None
        self.started = time.time()
        self.finished = None
        self.process = None
        self.lock = threading.Lock()

    def snapshot(self):
        with self.lock:
            elapsed = (self.finished or time.time()) - self.started
            return {
                "id": self.id,
                "kind": self.kind,
                "state": self.state,
                "progress": dict(self.progress),
                "result": self.result,
                "error": self.error,
                "detail": self.detail,
                "points": self.points,
                "elapsed": elapsed,
            }


class JobManager(object):
    """One job at a time -- the workbench runs a single experiment."""

    def __init__(self):
        self.jobs = {}
        self.lock = threading.Lock()

    def get(self, job_id):
        with self.lock:
            return self.jobs.get(job_id)

    def start(self, description, time_limit=None):
        job = Job(description.get("kind", "solve"))
        with self.lock:
            self.jobs[job.id] = job
            self._forget_stale()
        thread = threading.Thread(
            target=self._run, args=(job, description, time_limit), daemon=True
        )
        thread.start()
        return job

    def cancel(self, job_id):
        job = self.get(job_id)
        if job is None:
            return False
        with job.lock:
            if job.state != "running":
                return False
            job.state = "cancelled"
            job.error = "Cancelled."
            job.finished = time.time()
            process = job.process
        if process is not None and process.poll() is None:
            process.kill()
        return True

    def _forget_stale(self):
        """Keep the most recent handful; everything else is history."""
        finished = [j for j in self.jobs.values() if j.state != "running"]
        finished.sort(key=lambda j: j.finished or 0)
        for job in finished[:-8]:
            self.jobs.pop(job.id, None)

    def _run(self, job, description, time_limit):
        command = [_worker_python(), "-u", "-m", "source.webapp.worker"]
        environment = dict(os.environ)
        environment["PYTHONPATH"] = REPO_ROOT + os.pathsep + environment.get("PYTHONPATH", "")
        try:
            process = subprocess.Popen(
                command,
                cwd=REPO_ROOT,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=environment,
                creationflags=_no_window_flags(),
            )
        except OSError as error:
            self._fail(job, "Could not start the solver process: %s" % error)
            return

        with job.lock:
            job.process = process

        timer = None
        if time_limit:
            timer = threading.Timer(time_limit, self._time_out, args=(job, time_limit))
            timer.daemon = True
            timer.start()

        try:
            process.stdin.write(json.dumps(description).encode("utf-8"))
            process.stdin.close()
        except (OSError, ValueError):
            pass

        for raw in iter(process.stdout.readline, b""):
            line = raw.decode("utf-8", "replace").strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except ValueError:
                continue
            self._apply(job, event)

        stderr = process.stderr.read().decode("utf-8", "replace").strip()
        process.wait()
        if timer is not None:
            timer.cancel()

        with job.lock:
            if job.state == "running":
                if job.result is not None:
                    job.state = "done"
                else:
                    job.state = "failed"
                    job.error = job.error or "The solver exited without a result."
                    job.detail = job.detail or stderr or None
                job.finished = time.time()

    def _apply(self, job, event):
        kind = event.get("event")
        with job.lock:
            if job.state != "running":
                return
            if kind == "progress":
                job.progress = {
                    "done": event.get("done", 0),
                    "total": event.get("total", 0),
                    "message": event.get("message", ""),
                }
            elif kind == "instance":
                job.points = event.get("points")
            elif kind == "result":
                job.result = event.get("data")
            elif kind == "error":
                job.error = event.get("message")
                job.detail = event.get("detail")

    def _fail(self, job, message):
        with job.lock:
            job.state = "failed"
            job.error = message
            job.finished = time.time()

    def _time_out(self, job, limit):
        with job.lock:
            if job.state != "running":
                return
            job.state = "timeout"
            job.error = (
                "Stopped at the %ds limit. The search space grows roughly sixfold "
                "per extra city -- try fewer cities or a deeper cut." % int(limit)
            )
            job.finished = time.time()
            process = job.process
        if process is not None and process.poll() is None:
            process.kill()
