"""The redo."""
from src import app
import sys

try:
    app.run(sys.argv[1], int(sys.argv[2]), True)
except:
    app.run(debug=True)
