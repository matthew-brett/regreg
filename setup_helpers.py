''' Distutils / setuptools helpers

'''
import sys

from distutils.version import LooseVersion


def get_pkg_version(pkg_name):
    """ Return package version for `pkg_name` if installed

    Returns
    -------
    pkg_version : str or None
        Return None if package not importable.  Return 'unknown' if standard
        ``__version__`` string not present. Otherwise return version string.
    """
    try:
        pkg = __import__(pkg_name)
    except ImportError:
        return None
    try:
        return pkg.__version__
    except AttributeError:
        return 'unknown'


def version_error_msg(pkg_name, found_ver, min_ver):
    """ Return informative error message for version or None
    """
    if found_ver is None:
        return 'We need package {0}, but not importable'.format(pkg_name)
    if found_ver == 'unknown':
        return 'We need {0} version {1}, but cannot get version'.format(
            pkg_name, min_ver)
    if LooseVersion(found_ver) >= LooseVersion(min_ver):
        return None
    return 'We need {0} version {1}, but found version {2}'.format(
        pkg_name, found_ver, min_ver)


class SetupDependency(object):
    """ SetupDependency class

    Parameters
    ----------
    import_name : str
        Name with which required package should be ``import``ed.
    min_ver : str
        Distutils version string giving minimum version for package.
    req_type : {'install_requires', 'setup_requires'}, optional
        Setuptools dependency type.
    heavy : {False, True}, optional
        If True, and package is already installed (importable), then do not add
        to the setuptools dependency lists.  This prevents setuptools
        reinstalling big packages when the package was installed without using
        setuptools, or this is an upgrade, and we want to avoid the pip default
        behavior of upgrading all dependencies.
    install_name : str, optional
        Name identifying package to install from pypi etc, if different from
        `import_name`.
    """

    def __init__(self, import_name,
                 min_ver,
                 req_type='install_requires',
                 heavy=False,
                 install_name=None):
        self.import_name = import_name
        self.min_ver = min_ver
        self.req_type = req_type
        self.heavy = heavy
        self.install_name = (import_name if install_name is None
                             else install_name)

    def check_fill(self, setuptools_kwargs):
        """ Process this dependency, maybe filling `setuptools_kwargs`

        Run checks on this dependency.  If not using setuptools, then raise
        error for unmet dependencies.  If using setuptools, add missing or
        not-heavy dependencies to `setuptools_kwargs`.

        A heavy dependency is one that is inconvenient to install
        automatically, such as numpy or (particularly) scipy, matplotlib.

        Parameters
        ----------
        setuptools_kwargs : dict
            Dictionary of setuptools keyword arguments that may be modified
            in-place while checking dependencies.
        """
        found_ver = get_pkg_version(self.import_name)
        ver_err_msg = version_error_msg(self.import_name,
                                        found_ver,
                                        self.min_ver)
        if not 'setuptools' in sys.modules:
            # Not using setuptools; raise error for any unmet dependencies
            if ver_err_msg is not None:
                raise RuntimeError(ver_err_msg)
            return
        # Using setuptools; add packages to given section of
        # setup/install_requires, unless it's a heavy dependency for which we
        # already have an acceptable importable version.
        if self.heavy and ver_err_msg:
            return
        new_req = '{0}>={1}'.format(self.import_name, self.min_ver)
        old_reqs = setuptools_kwargs.get(self.req_type, [])
        setuptools_kwargs[self.req_type] = old_reqs + [new_req]


class Bunch(object):
    def __init__(self, vars):
        for key, name in vars.items():
            if key.startswith('__'):
                continue
            self.__dict__[key] = name


def read_vars_from(ver_file):
    """ Read variables from Python text file

    Parameters
    ----------
    ver_file : str
        Filename of file to read

    Returns
    -------
    info_vars : Bunch instance
        Bunch object where variables read from `ver_file` appear as
        attributes
    """
    # Use exec for compabibility with Python 3
    ns = {}
    with open(ver_file, 'rt') as fobj:
        exec(fobj.read(), ns)
    return Bunch(ns)
