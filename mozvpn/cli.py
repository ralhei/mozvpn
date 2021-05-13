"""Console script for mozvpn."""
import sys
import csv
import click

from mozvpn import mozvpn, mozvpn_gui, wireguard

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    ...


@click.option('-c', '--city')
@click.option('-C', '--country')
@click.option('-r', '--region')
@click.argument('conf_or_interface')
@main.command()
def up(city, country, region, conf_or_interface):
    """Setup connection to VPN server location or interface."""
    #
    # TODO: Allow to connect by city/country/region
    #
    iface = wireguard.interface()
    if iface:
        print(f'Error: already connected to {iface}')
    elif conf_or_interface:
        wireguard.connect(conf_or_interface)
        print(f'Connected to: {conf_or_interface}')


@click.option('-c', '--city')
@click.option('-C', '--country')
@click.option('-r', '--region')
@click.argument('conf_or_interface')
@main.command()
def down(city, country, region, conf_or_interface):
    """Shutdown currently active VPN server connection."""
    if not wireguard.interface():
        print('Error: not connected')
    elif conf_or_interface:
        wireguard.disconnect(conf_or_interface)
        print(f'Disconnected from: {conf_or_interface}')


@click.option('--ip', is_flag=True)
@main.command()
def status(ip):
    """Show status of current VPN server connection.

    Args:
        ip: If True, the externally visible IP address will also be returned.
    """
    print(wireguard.status(ip=ip))


@main.command()
def ip():
    """Show externally visible ip address."""
    print(wireguard.ipinfo()['ip'])


@main.command()
def gui():
    """Start graphical user interface for mozvpn."""
    mozvpn_gui.gui()


@click.argument('config_paths', nargs=-1)
@click.option('-o', '--output', type=click.File('w'), default='-')
@main.command()
def geolocate(config_paths, output):
    """Determine geographic location for server configurations.

    Write the csv-formatted vpn geo-information to output file, or to stdout,
    if 'output' was not provided or is a dash ('-').
    """
    vpn_configs = mozvpn.find_vpn_server_locations(config_paths)
    fieldnames = ['conf', 'ip', 'country', 'region', 'city']
    writer = csv.DictWriter(output, fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(vpn_configs)


@main.command()
def install():
    """Install all that is necessary to run MozillaVPN -- to be finished ..."""
    # cmd('groupadd mozvpn')
    # cmd('usermod -a -G mozvpn <user>')
    # cmd('echo "%mozvpn ALL = (root) NOPASSWD: /usr/bin/wg, /usr/bin/wg-quick" > /etc/sudoers.d/mozvpn')
    # cmd('chmod 440 /etc/sudoers.d/mozvpn')
    pass


@click.command()
def xmozvpn():
    """Start graphical user interface for mozvpn."""
    # This is an alternative for 'mozvpn gui' above.
    mozvpn_gui.gui()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
