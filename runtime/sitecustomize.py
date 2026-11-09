"""Screening runtime: run at every start of its Python.

The Windows embeddable Python is configured by its ._pth file, which (unlike a
normal Python) does not put a script's own folder on sys.path. The tools import
their sibling modules (balance_viewer.py imports balance_core.py), so this puts
the folder back. On a normal Python it is already there and this does nothing.
"""
import os
import sys


def _script_dir():
    argv = getattr(sys, "argv", None) or []
    if not argv or not argv[0] or argv[0] in ("-c", "-m", "-"):
        return
    path = os.path.abspath(argv[0])
    if os.path.isfile(path):
        d = os.path.dirname(path)
        if d not in sys.path:
            sys.path.insert(0, d)


_script_dir()
