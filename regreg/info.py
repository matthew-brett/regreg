""" This file contains defines parameters for regreg that we use to fill
settings in setup.py, the regreg top-level docstring, and for building the docs.
In setup.py in particular, we exec this file, so it cannot import regreg
"""

# regreg version information.  An empty _version_extra corresponds to a
# full release.  '.dev' as a _version_extra string means this is a development
# version
_version_major = 0
_version_minor = 0
_version_micro = 1
_version_extra = '.dev'

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
__version__ = "%s.%s.%s%s" % (_version_major,
                              _version_minor,
                              _version_micro,
                              _version_extra)

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: BSD License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

description  = 'A multi-algorithm Python framework for regularized regression'

# Minimum versions
# Check these against requirements.txt and .travis.yml
NUMPY_MIN_VERSION='1.6.0'
SCIPY_MIN_VERSION = '0.9'
CYTHON_MIN_VERSION = '0.18'

NAME                = 'regreg'
MAINTAINER          = "regreg developers"
MAINTAINER_EMAIL    = ""
DESCRIPTION         = description
URL                 = "http://github.org/regreg/regreg"
DOWNLOAD_URL        = ""#"http://github.com/regreg/regreg/archives/master"
LICENSE             = "BSD license"
CLASSIFIERS         = CLASSIFIERS
AUTHOR              = "regreg developers"
AUTHOR_EMAIL        = ""#"regreg-devel@neuroimaging.scipy.org"
PLATFORMS           = "OS Independent"
MAJOR               = _version_major
MINOR               = _version_minor
MICRO               = _version_micro
ISRELEASE           = _version_extra == ''
VERSION             = __version__
STATUS              = 'alpha'
PROVIDES            = ["regreg"]
REQUIRES            = ["numpy (>=%s)" % NUMPY_MIN_VERSION,
                       "scipy (>=%s)" % SCIPY_MIN_VERSION]
