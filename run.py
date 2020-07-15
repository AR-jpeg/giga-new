"""The redo."""
from waitress import serve
from src import app
import socket


try:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    serve(app, host=ip_address, port=80)
except:
    serve(app)
