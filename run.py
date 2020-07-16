"""The redo."""
from waitress import serve
from src import create_app
import socket
import sys

app = create_app()

try:
    type_ = sys.argv[1]  # like python run.py flask
except IndexError:
    type_ = serve


try:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    if type_ == 'deploy':
        serve(app, host=ip_address, port=80)
    else:
        app.run(host=ip_address, port=80)
except:
    app.run(host=ip_address, port=80)
