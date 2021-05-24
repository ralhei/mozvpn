.. highlight:: shell

============
Installation
============

.. note::

    This installation was tested on Linux (opensuse) only so far. In principle
    it should work on most Linux variants without modifications. Also there is
    a good chance that MacOS could be supported.<br/>
    If you find problems please file an issue at the github repo, or even better
    submit a pull request with a decent solution to the problem.

.. warning::

    MozVPN should per se also work on Windows. The installation for
    required packages ``MozWire``, ``WireGuard``, and ``MozVPN`` should work just
    fine under Windows.<br/>
    However the setup of ``MozVPN``, i.e. the point where ``mozpvn setup`` is run
    (see below) currently only supports Linux-like systems.

    If you run ``mozpvn setup --dry-run`` you can see what commands would be run
    on Linux. If you could provide something similar for Windows this would be awesome.


Installing helper tools MozWire and wireguard
---------------------------------------------

MozVPN is based on two other applications that need to be installed first, namely MozWire
and wireguard.

MozWire
^^^^^^^
This tool has basically to be run once only. It connects to your MozillaVPN account
(subscription) and downloads a set of approx. 400 configuration files, each one
providing connection details and credentials for a VPN connection to a server
somewhere in the world. (MozVPN will do the actual download for you, so no worry here).

Installing MozWire
""""""""""""""""""
MozWire can be downloaded or downloaded as explained on https://github.com/NilsIrl/MozWire.
There you'll find binaries for Linux, MacOS, and Windows. Download the binary for your
operating system and install it in a place where it can be found when being called
from the command line, e.g. ``/usr/local/bin`` or ``~/bin`` in case of Linux or MacOS.
Just make sure that this path is contained in your shell's PATH variable. Do the
corresonding setup for Windows if that is your OS.

If nothing fits the MozWire homepage also explains how to compile it from sources. This
is basically a one line command and worked like a charm in my case. The only tool
required for compiling is ``cargo`` which is usually installed on Linux machines
with ``sudo zypper install cargo`` (OpenSuse) or ``sudo apt install cargo`` (Debian/Ubuntu).
Further explanations about installing cargo can be found at
https://doc.rust-lang.org/cargo/getting-started/installation.html.

Once installed you should find the ``mozwire`` executable in your PATH.

WireGuard
^^^^^^^^^
Because MozillaVPN is based on the WireGuard protocol the corresponding binary and
helper tools have to be installed as well.

WireGuard uses the configuration files provided by MozWire and uses those to
make the actual connection to the VPN servers.

Installing WireGuard
""""""""""""""""""""
The page https://www.wireguard.com/install/ describes this for more than 20 operating
systems. For Linuxes it is usually a command like ``sudo zypper install wireguard-tools``
(OpenSuse) or ``sudo apt install wireguard`` (Debian/Ubuntu).

Once installed you should find the two executables ``wg`` and ``wg-quick`` in your
PATH.


Installing a stable release of MozVPN
-------------------------------------
After having installed MozWire and WireGuard we finally can install MozVPN itself.

To install MozVPN, run this command in your terminal:

.. code-block:: console

    $ pip install mozvpn

This is the preferred method to install mozvpn, as it will always install the most
recent stable release. MozVPN requires Python3.6 or newer.

You can either install it in a local virtual environment somewhere in your home
directory, or system-wide (on a Linux like OS you need to be root or use sudo,
e.g. ``sudo pip install mozvpn``).

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Installing MozVPN from sources
------------------------------

The sources for MozVPN can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/ralhei/mozvpn

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/ralhei/mozvpn/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/ralhei/mozvpn
.. _tarball: https://github.com/ralhei/mozvpn/tarball/master

Congratulation! Now the software part is done. The next step will be to
setup the configuration, as explained in the next section :ref:`Setup`.
