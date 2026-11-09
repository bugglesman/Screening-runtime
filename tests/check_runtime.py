"""Checks a built runtime works on its own: run with the runtime's Python.

    <runtime>/python.exe tests/check_runtime.py      (Windows)
    <runtime>/bin/python3 tests/check_runtime.py     (macOS)

Exits non-zero on the first failure, printing what failed.
"""
import os
import subprocess
import sys
import tempfile

ok = True


def check(name, cond, info=""):
    global ok
    print(("PASS  " if cond else "FAIL  ") + name + ("   " + str(info) if info else ""))
    ok = ok and bool(cond)


here = os.path.dirname(os.path.realpath(sys.executable))
prefix = os.path.realpath(sys.prefix)
check("runs from the runtime folder, not an installed Python",
      prefix in (here, os.path.dirname(here)), (sys.prefix, sys.executable))
check("Python 3.13", sys.version_info[:2] == (3, 13), sys.version)

import numpy as np                                   # noqa: E402
import scipy                                         # noqa: E402
from scipy import ndimage, spatial, sparse           # noqa: E402
import trimesh                                       # noqa: E402
import fast_simplification                           # noqa: E402
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6 import QtCore, QtGui, QtWidgets         # noqa: E402
check("versions", True, "numpy %s, scipy %s, trimesh %s, PySide6 %s" % (
    np.__version__, scipy.__version__, trimesh.__version__, QtCore.__version__))

a = np.zeros((20, 20, 20), bool); a[5:15, 5:15, 5:15] = True
check("scipy.ndimage distance transform", ndimage.distance_transform_edt(a).max() == 5.0)
check("scipy.ndimage label", ndimage.label(a)[1] == 1)
t = spatial.cKDTree(np.random.default_rng(0).random((1000, 3)))
check("scipy KD-tree", len(t.query_ball_point([0.5, 0.5, 0.5], 0.2)) > 0)
m = trimesh.creation.icosphere(subdivisions=3)
check("trimesh", m.is_watertight and len(m.faces) == 1280)
v2, f2 = fast_simplification.simplify(np.asarray(m.vertices, np.float32),
                                      np.asarray(m.faces, np.int64), target_reduction=0.5)
check("fast_simplification", 0 < len(f2) < len(m.faces), len(f2))
app = QtWidgets.QApplication([])
w = QtWidgets.QLabel("ok"); w.show(); app.processEvents()
img = w.grab().toImage()
check("Qt draws a window", img.width() > 0 and img.height() > 0)

# A tool script imports its sibling modules, as balance_viewer.py imports
# balance_core.py: the script's folder must be on sys.path, run from anywhere.
d = tempfile.mkdtemp()
os.makedirs(os.path.join(d, "tool"))
with open(os.path.join(d, "tool", "helper.py"), "w") as fh:
    fh.write("X = 42\n")
with open(os.path.join(d, "tool", "main.py"), "w") as fh:
    fh.write("import helper\nprint(helper.X)\n")
r = subprocess.run([sys.executable, os.path.join(d, "tool", "main.py")], cwd=d,
                   capture_output=True, text=True)
check("a script finds the modules next to it", r.returncode == 0 and r.stdout.strip() == "42",
      (r.stdout + r.stderr).strip()[-300:])
# An unrelated PYTHONPATH on the machine must not leak in.
env = dict(os.environ, PYTHONPATH=os.path.join(d, "tool"))
r = subprocess.run([sys.executable, "-c", "import sys; print(sys.prefix)"], env=env,
                   capture_output=True, text=True)
check("starts cleanly with a PYTHONPATH set", r.returncode == 0, r.stderr[-300:])

print("\nall good" if ok else "\nFAILED")
sys.exit(0 if ok else 1)
