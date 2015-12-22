.. _release-guide:

**********************************
A guide to making a regreg release
**********************************

A guide for developers who are doing a regreg release

.. _release-checklist:

Release checklist
=================

* Review the open list of `regreg issues`_.  Check whether there are
  outstanding issues that can be closed, and whether there are any issues that
  should delay the release.  Label them !

* Review and update the release notes.  Review and update the :file:`Changelog`
  file.  Get a partial list of contributors with something like::

      git log 0.2.0.. | grep '^Author' | cut -d' ' -f 2- | sort | uniq

  where ``0.2.0`` was the last release tag name.

  Then manually go over ``git shortlog 0.2.0..`` to make sure the release notes
  are as complete as possible and that every contributor was recognized.

* Use the opportunity to update the ``.mailmap`` file if there are any
  duplicate authors listed from ``git shortlog -ns``.

* Add any new authors to the ``AUTHORS`` file.  Add any new entries to the
  ``THANKS`` file.

* Check the copyright years in ``doc/conf.py`` and ``LICENSE``

* Review the ``README.rst``.  Check the output of::

    rst2html.py README.rst > ~/tmp/readme.html

  because this will be the output used by pypi_

* Check the dependencies listed in ``regreg/info.py`` (e.g.
  ``NUMPY_MIN_VERSION``) and in ``requirements.txt``.  They should at least
  match. Do they still hold?  Make sure ``.travis.yml`` is testing these
  minimum dependencies specifically.

* Do a final check on the regreg buildbot builds on the `nipy buildbot`_.  If
  you have any local edits, try them on the buildbots using `try_branch.py`_.

* If you have travis-ci_ building set up on your own fork of regreg you might
  want to push the code in its current state to a branch that will build,
  e.g::

    git branch -D pre-release-test # in case branch already exists
    git co -b pre-release-test
    git push your-github-user pre-release-test

Doing the release
=================

* The release should now be ready.

* Edit :file:`regreg/info.py` to set ``_version_extra`` to ``''``; commit.
  Then try building the source distribution with::

    python setup.py sdist

* Once everything looks good, you are ready to upload the source release to
  PyPi.  See `setuptools intro`_.  Make sure you have a file
  ``\$HOME/.pypirc``, of form::

    [distutils]
    index-servers =
        pypi

    [pypi]
    username:your.pypi.username
    password:your-password

    [server-login]
    username:your.pypi.username
    password:your-password

* Once everything looks good, upload the source release to PyPi.  See
  `setuptools intro`_::

    python setup.py register
    python setup.py sdist --formats=gztar,zip upload

* Trigger binary builds for OSX from travis-ci:

    * https://travis-ci.org/MacPython/regreg-wheels
    * https://github.com/MacPython/regreg-wheels

  Upload the resulting wheels to pypi from http://wheels.scipy.org;

* Tag the release with tag of form ``0.5.0``::

    git tag -am 'Second main release' 0.5.0

* Now the version number is OK, push the docs to github pages with::

    cd doc
    make github

* Set up maintenance / development branches

  If this is this is a full release you need to set up two branches, one for
  further substantial development (often called 'trunk') and another for
  maintenance releases.

  * Branch to maintenance::

      git co -b maint/0.5.x

    Set ``_version_extra`` back to ``.dev`` and bump ``_version_micro`` by 1.
    Thus the maintenance series will have version numbers like - say - '0.5.1.dev'
    until the next maintenance release - say '0.5.1'.  Commit. Don't forget to
    push upstream with something like::

      git push upstream maint/0.2.x --set-upstream

  * Start next development series::

      git co main-master

    then restore ``.dev`` to ``_version_extra``, and bump ``_version_minor``
    by 1.  Thus the development series ('trunk') will have a version number
    here of '0.3.0.dev' and the next full release will be '0.3.0'.

  * Merge ``-s ours`` the version number changes from the maint release, e.g::

      git merge -s ours maint/0.3.x

    This marks the version number changes commit as merged, so we can merge any
    changes we need from the maintenance branch without merge conflicts.

  If this is just a maintenance release from ``maint/0.2.x`` or similar, just
  tag and set the version number to - say - ``0.2.1.dev``.

* Push tags::

    git push --tags

* Announce to the any mailing lists that might be interested.

.. _setuptools intro: http://packages.python.org/an_example_pypi_project/setuptools.html

.. include:: ../links_names.inc
