# Screening runtime

A portable Python with every library the **Balance Check** and the **Sharps
Screening Tool** need: numpy, scipy, trimesh, fast_simplification and PySide6.
Nothing is installed. Unzip it next to the tools and their launchers use it.
Running `install_windows.bat` / `install_mac.command` is no longer needed.

Only the libraries are packed in here. The tools' own code stays in their git
folders, so `git pull` still updates them. A new runtime is only needed when a
tool's requirements change.

## Get it

[Releases → latest](../../releases/latest):

- **ScreeningRuntime-windows-x64.zip**: Windows 10/11, 64-bit Intel/AMD.
- **ScreeningRuntime-macos-arm64.zip**: Apple Silicon Macs (M1 and later).

## Put it in place

Unzip so the `ScreeningRuntime` folder sits **next to the tool folders**. The
launchers look for it in two places, relative to their data folder:

```
ZPlugs64\                         <- or wherever the tools live
  BalanceCheckTool.txt
  BalanceCheckData\
  SharpsScreeningTool_v32_33.txt
  SharpsScreeningData\
  ScreeningRuntime\               <- here, shared by both  (..\ScreeningRuntime)
```

or one level up, when each tool is its own git folder:

```
Documents\
  balance-checking-tool\          (BalanceCheckTool.txt, BalanceCheckData\)
  sharps-checking-tool\
  ScreeningRuntime\               <- here                  (..\..\ScreeningRuntime)
```

**Windows:** before unzipping, right-click the zip → Properties → tick
**Unblock** → OK. Otherwise Windows marks every file as "from the internet" and
may ask before running the viewer.

**macOS:** nothing extra. The launchers clear the "downloaded from the internet"
flag on the runtime the first time they use it.

## What's inside, and why

- **Windows:** the official *embeddable* Python from python.org, which is signed
  by the Python Software Foundation and made to be shipped inside other apps.
  The libraries are unpacked into `Lib\site-packages` beside it. Its
  `python313._pth` file fixes its search path to its own folder, so an installed
  Python or a `PYTHONPATH` on the machine can't interfere.
- **macOS:** a standalone, relocatable Python (python-build-standalone) with
  the libraries installed into it.
- `sitecustomize.py` puts a script's own folder on its search path, as a normal
  Python does. The embeddable Python leaves it off, and the tools import their
  sibling files.
- `RUNTIME_VERSION.txt` lists the exact Python and library versions.

## How it's built

`.github/workflows/build.yml`, on every push to `main`. It builds both zips,
unpacks each on a clean machine with no other Python on the path, and runs
`tests/check_runtime.py`, which covers the libraries, a Qt window, script
imports and isolation. It then replaces the `latest` release.
`requirements.txt` holds the exact versions.
