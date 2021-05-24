.. highlight:: shell

============
Setup
============

Get a subscription for MozillaVPN
---------------------------------
Now it is time to get a subscription for MozillaVPN, if you don't have one already.
Without a subscription you won't be able to setup
VPN connections via MozillaVPN. Details can be found at
https://www.mozilla.org/en-US/products/vpn/.

The following step will require you to enter your username and password for
MozillaVPN, so make sure you saved them somewhere (e.g. in a password manager).


Setting up MozillaVPN access Linux
----------------------------------
Luckily MozVPN has built in a setup feature which does the following steps for you.
This setup has to be run only once. It might be required to be run later again, e.g.
if your MozillaVPN subscription has expired and you have renewed it. But for now
running this once is sufficient.

.. Note:
   The following command has only been implemented and checked on (OpenSuse) Linux
   so far. It should probably run without changes on MacOS. Unfortunately Windows
   users have to perform the steps manually and adapt them for Windows.

The command to run is::

    mozvpn setup

or::

    mozvpn setup --verbose

if you'd like to see the details.

You are required to enter two sets of credentials in this process (one for MozillaVPN
and one for `root`), so please read the following descriptions (if you are interested
in the details) or just follow the what is happening in your browser and in the shell
where you started ``mozvpn setup``.

The steps performed by ``mozpvn setup`` are:

1. It runs MozWire, which itself opens a page in your Firefox (or possibly other browser)
   asking for your MozillaVPN credentials. **Type them into the MozillaVPN login page
   if your are not already logged in.**

   This stage of the setup will download approx. 400 WireGuard configuration and
   credential files into a local directory on your computer.

2. Because these WireGuard configuration files do not contain detailed information
   about their server geo-locations a little script is run to determine those
   locations for each WireGuard configuration file. This geo-location information
   is stored in one single ``locations.csv`` file for you. No interaction required
   here from your side.

3. The WireGuard configuration files and the ``locations.csv`` file have to be
   installed in ``/etc/wireguard`` on Linux-like or MacOS systems. This requires
   root permissions.

4. To allow MozVPN to run as normal user ``sudo``-privileges have to be setup
   for the WireGuard tools. This is achieved by creating a new Linux group ``mozvpn``
   and adding those users to it who should be allowed to run MozVPN on your computer.
   Note that - after this is done - all affected users have to logout and login again
   to activate this new group membership for them. You will be told later when to
   do this.

5. A new ``sudo``-file will be created in ``/etc/sudoers.d/mozvpn`` giving all members
   of group ``mozvpn`` the privileges to run ``wg-quick`` with root privileges.
   This is the tool that actually sets up and tears down the VPN connection under the hood.

You can check the commands for all five steps beforehand by running ``mozpvn setup --dry_run``.
This will print the commands to the shell only without actually executing them.
If you have security concerns you can then
run those commands yourself without going through ``mozpvn setup``. This also allows
you do adapt them if you prefer or require an alternative setup on your computer.

Testing
-------
Once everything is in place you should be able to activate and tear down a connection
to one of Mozilla's VPN servers through the command line, simply by running the
following commands from the shell::

    $ mozvpn status
    Not connected
    $ mozpvn up de4-wireguard   # must match a file in /etc/wireguard/*.conf
    Connected to: de4-wireguard
    $ mozvpn status
    Connected to: de4-wireguard
    $ mozpvn down de4-wireguard
    Disconnected from: de4-wireguard
    $ mozvpn status
    Not connected
