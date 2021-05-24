=====
Usage
=====

Using the graphical User Interface (GUI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
