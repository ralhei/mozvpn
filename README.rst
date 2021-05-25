======
MozVPN
======


..
  .. image:: https://img.shields.io/pypi/v/mozvpn.svg
       :target: https://pypi.python.org/pypi/mozvpn

.. image:: https://img.shields.io/travis/ralhei/mozvpn.svg
        :target: https://travis-ci.com/ralhei/mozvpn

.. image:: https://readthedocs.org/projects/mozvpn/badge/?version=latest
        :target: https://mozvpn.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

MozVPN is an alternative CLI and GUI client for MozillaVPN.

When MozillaVPN showed up in May 2021 Mozilla published clients for Ubuntu
Linux only, which didn't run on my OpenSuse machine. This was the motivation
to implement this alternative client.

Short Usage
-----------
The following instructions assume that everything is installed and setup
(incl. ``wireguard`` and ``wireguard-tools``)
and you have a subscription for MozillaVPN. For details see the
complete documentation on https://mozvpn.readthedocs.io.

Graphical User Interface (GUI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To start the GUI for mozvpn just run::

    $ mozvpn gui
    (or alternatively)
    $ xmozvpn

A window should open and allow you to select the desired VPN server endpoint
from a choice of cities in various countries. Then just click the ``connect``
button, and you should have a running VPN.

Command Line Interface (CLI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The command line interface can be used to connect or disconnect to MozillaVPN
from a linux or windows shell. Also the current status of the connection can be obtained.

Examples::

    $ mozvpn status
    Not connected
    $ mozpvn up de4-wireguard   # must match files in /etc/wireguard/*.conf
    Connected to: de4-wireguard
    $ mozvpn status
    Connected to: de4-wireguard
    $ mozpvn down de4-wireguard
    Disconnected from: de4-wireguard
    $ mozvpn status
    Not connected

License
-------
* Free software: GNU General Public License v3
* Documentation: https://mozvpn.readthedocs.io. (to be done).


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
