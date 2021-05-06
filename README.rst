======
mozvpn
======


.. image:: https://img.shields.io/pypi/v/mozvpn.svg
        :target: https://pypi.python.org/pypi/mozvpn

.. image:: https://img.shields.io/travis/ralhei/mozvpn.svg
        :target: https://travis-ci.com/ralhei/mozvpn

.. image:: https://readthedocs.org/projects/mozvpn/badge/?version=latest
        :target: https://mozvpn.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

Tools and GUI for MozillaVPN.


* Free software: GNU General Public License v3
* Documentation: https://mozvpn.readthedocs.io. (to be done).


Features
--------

* Provide alternative GUI frontend for Mozilla VPN.

Short Usage
-----------
Once everything is installed (incl. ``wireguard`` and ``wireguard-tools``)
and you have a subscription for MozillaVPN, then just run::

    $ mozvpn gui

A window should open and allow you to select the desired VPN server endpoint
from a choice of cities in various countries. Then just click the ``connect``
button, and you should have a running VPN.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
