# setup.py
import os

# Updated from deprecated distutils/Cython.Distutils to setuptools and Cython.Build.cythonize
from setuptools import setup, Extension
from Cython.Build import cythonize

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

