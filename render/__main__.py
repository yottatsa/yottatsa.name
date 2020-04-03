import sys
from . import render

if len(sys.argv) > 2:
    render.render(sys.argv[1], sys.argv[2:])
