# setup.py
import os
import sys
import shutil
import sysconfig

# Updated from deprecated distutils/Cython.Distutils to setuptools and Cython.Build.cythonize
from setuptools import setup, Extension
from Cython.Build import cythonize

def check_system_requirements():
    missing = []

    # 1. Check for C compiler
    has_compiler = any(shutil.which(cc) for cc in ["gcc", "clang", "cc", "cl"])
    if not has_compiler:
        missing.append("- C compiler (e.g. gcc, clang, or MSVC)")

    # 2. Check for Python C header (Python.h)
    inc_dir = sysconfig.get_path('include')
    if not (inc_dir and os.path.exists(os.path.join(inc_dir, 'Python.h'))):
        missing.append(f"- Python development headers (Python.h not found in {inc_dir})")

    if missing:
        msg = (
            "\n" + "=" * 70 + "\n"
            "ERROR: Missing required system dependencies to build GPMsDB_tk:\n"
            + "\n".join(missing) + "\n\n"
            "Please install the appropriate development packages:\n"
            "  - Ubuntu/Debian:  sudo apt-get install gcc python3-dev\n"
            "  - RHEL/Fedora:    sudo dnf install gcc python3-devel\n"
            "  - macOS:          xcode-select --install\n"
            + "=" * 70 + "\n"
        )
        sys.stderr.write(msg)
        sys.exit(1)

check_system_requirements()

# reads the version number from the VERSION file in /GPMSDB_tk
def version():
    setup_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(setup_dir, 'GPMsDB_tk', 'VERSION'), 'r') as f:
        return f.readline().strip()

# define the extension modules
ext_modules = [
    Extension('GPMsDB_tk.calc', sources=['GPMsDB_tk/calc.pyx'])
]

# run the setup (consolidated duplicate setup() calls and replaced cmdclass with cythonize)
setup(
    name='GPMsDB_tk',
    python_requires='>=3.6',
    version=version(),
    author='Yuji Sekiguchi; Manuel Escalera',
    author_email='y.sekiguchi@aist.go.jp; escaleram.dev@gmail.com',
    packages=['GPMsDB_tk'],
    scripts=['bin/GPMsDB_tk'],
    package_data={'GPMsDB_tk': ['VERSION']},
    url='https://github.com/typhoidManny/GPMsDB-tk',
    ext_modules=cythonize(ext_modules, language_level="3"),
    description='Toolkit for bacterial and archaeal identification based on genomically-based MALDI-TOF MS peak lists.'
)

