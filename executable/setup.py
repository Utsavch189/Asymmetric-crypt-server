import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.

build_exe_options = {"packages": ["requests","rsa","pyasn1","os","socket","time","fnmatch","json","win32api"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "crypt",
    version = "0.1",
    description = "Silent Killer!",
    options = {"build_exe": build_exe_options},
    executables = [Executable("crypt.py", base=base)]
)
