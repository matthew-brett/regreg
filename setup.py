#!/usr/bin/env python
''' Installation script for regreg package '''

import os
import sys
from os.path import join as pjoin, dirname

# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

import numpy as np

# Get version and release info, which is all stored in regreg/info.py
ver_file = os.path.join('regreg', 'info.py')
# Use exec for compabibility with Python 3
exec(open(ver_file).read())

# force_setuptools can be set from the setup_egg.py script
if not 'force_setuptools' in globals():
    # For some commands, use setuptools
    if len(set(('develop', 'bdist_egg', 'bdist_rpm', 'bdist', 'bdist_dumb',
                'bdist_mpkg', 'install_egg_info', 'egg_info',
                'easy_install')).intersection(sys.argv)) > 0:
        force_setuptools = True
    else:
        force_setuptools = False

if force_setuptools:
    import setuptools

# Import distutils _after_ potential setuptools import above, and after removing
# MANIFEST
from distutils.core import setup
from distutils.extension import Extension

from cythexts import cyproc_exts, get_pyx_sdist
from setup_helpers import (read_vars_from, SetupDependency, process_deps)

# Get version and release info, which is all stored in regreg/info.py
info = read_vars_from(pjoin('regreg', 'info.py'))

# We may just have imported setuptools, or we may have been exec'd from a
# setuptools environment like pip
using_setuptools = 'setuptools' in sys.modules
extra_setuptools_args = {}
if using_setuptools:
    # Try to preempt setuptools monkeypatching of Extension handling when Pyrex
    # is missing.  Otherwise the monkeypatched Extension will change .pyx
    # filenames to .c filenames, and we probably don't have the .c files.
    sys.path.insert(0, pjoin(dirname(__file__), 'fake_pyrex'))
    # Set setuptools extra arguments
    extra_setuptools_args = dict(
        tests_require=['nose'],
        test_suite='nose.collector',
        zip_safe=False,
        extras_require = dict(
            doc=['Sphinx>=1.0'],
            test=['nose>=0.10.1']))
    # numpy and scipy will get into setup_requires / install_requires via
    # "process_deps" call below.

# Define extensions
EXTS = []
for modulename, other_sources in (
    ('regreg.atoms.projl1_cython', []),
    ('regreg.atoms.mixed_lasso_cython', []),
    ('regreg.atoms.piecewise_linear', [])):
    pyx_src = pjoin(*modulename.split('.')) + '.pyx'
    EXTS.append(Extension(modulename,[pyx_src] + other_sources,
                          include_dirs = [np.get_include(),
                                         "src"]))

extbuilder, needs_cython = cyproc_exts(EXTS,
                                       info.CYTHON_MIN_VERSION,
                                       'pyx-stamps')

cython_dep = SetupDependency('Cython', info.CYTHON_MIN_VERSION,
                             req_type='setup_requires',
                             heavy=False)
numpy_dep = SetupDependency('numpy', info.NUMPY_MIN_VERSION,
                            req_type='setup_requires',
                            heavy=True)
scipy_dep = SetupDependency('scipy', info.SCIPY_MIN_VERSION,
                             req_type='install_requires',
                             heavy=True)

process_deps((cython_dep,) if needs_cython else () +
             (numpy_dep, scipy_dep), extra_setuptools_args)


cmdclass = dict(
    build_ext=extbuilder,
    sdist=get_pyx_sdist())


def main(**extra_args):
    setup(name=info.NAME,
          maintainer=info.MAINTAINER,
          maintainer_email=info.MAINTAINER_EMAIL,
          description=info.DESCRIPTION,
          long_description = open('README.rst', 'rt').read(),
          url=info.URL,
          download_url=info.DOWNLOAD_URL,
          license=info.LICENSE,
          classifiers=info.CLASSIFIERS,
          author=info.AUTHOR,
          author_email=info.AUTHOR_EMAIL,
          platforms=info.PLATFORMS,
          version=info.VERSION,
          requires=info.REQUIRES,
          provides=info.PROVIDES,
          packages     = ['regreg',
                          'regreg.tests',
                          'regreg.affine',
                          'regreg.affine.tests',
                          'regreg.atoms',
                          'regreg.atoms.tests',
                          'regreg.problems',
                          'regreg.problems.tests',
                          'regreg.smooth',
                          'regreg.smooth.tests',
                         ],
          ext_modules = EXTS,
          package_data = {},
          data_files=[],
          scripts= [],
          cmdclass = cmdclass,
          **extra_args
         )

#simple way to test what setup will do
#python setup.py install --prefix=/tmp
if __name__ == "__main__":
    main(**extra_setuptools_args)
