"""The redo."""
from waitress import serve
from src import create_app
import socket as s
import sys


ADDR = s.gethostbyname(s.gethostname())
app = create_app()

if len(sys.argv) > 1:
    deploy = sys.argv[1]
else:
    deploy = None


def run() -> None:
    if deploy:
        serve(app, port=80)

    else:
        app.run(host=ADDR, port=80)


run()
