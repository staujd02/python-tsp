"""Hull Cut Workbench -- the front end for this TSP research code.

Double-click this file (Windows runs .pyw without a console) or run it with any
Python 3.7+. It starts a local server and opens the workbench in your browser.

    python main.pyw                  open the workbench
    python main.pyw --no-browser     start the server only
    python main.pyw --port 9000      pin the port
    python main.pyw --verbose        log requests to the console

The original exploratory script is kept as research.py.
"""

import argparse
import os
import sys
import threading
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from source.webapp.server import find_free_port, serve  # noqa: E402


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog="main.pyw", description="Run the Hull Cut Workbench."
    )
    parser.add_argument("--port", type=int, default=8731, help="preferred port (default 8731)")
    parser.add_argument("--host", default="127.0.0.1", help="interface to bind (default localhost)")
    parser.add_argument("--no-browser", action="store_true", help="do not open a browser")
    parser.add_argument("--verbose", action="store_true", help="log every request")
    return parser.parse_args(argv)


def main(argv=None):
    options = parse_arguments(argv if argv is not None else sys.argv[1:])
    port = find_free_port(options.port, options.host)
    server = serve(host=options.host, port=port, verbose=options.verbose)
    address = "http://%s:%d/" % (options.host, port)

    if not options.no_browser:
        threading.Timer(0.4, webbrowser.open, args=(address,)).start()

    if options.verbose or options.no_browser:
        print("Hull Cut Workbench is running at " + address)
        print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
