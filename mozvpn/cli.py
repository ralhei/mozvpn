"""Console script for mozvpn."""
import os
import sys
import csv
import click
import logging

from mozvpn import mozvpn, mozvpn_gui, wireguard

logger = logging.getLogger('mozvpn')
logging.basicConfig(level=logging.WARNING, stream=sys.stdout)

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
    try:
        print(wireguard.status(ip=ip))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


@main.command()
def ip():
    """Show externally visible ip address."""
    print(wireguard.ipinfo()['ip'])


@main.command()
def gui():
    """Start graphical user interface for mozvpn."""
    try:
        mozvpn_gui.gui()
    except wireguard.ControlledExit:
        sys.exit(1)


@click.argument('config_paths', nargs=-1)
@click.option('-o', '--output', type=click.File('w'), default='-')
@main.command()
def geolocate(config_paths, output):
    """Determine geographic location for server configurations.

    Write the csv-formatted vpn geo-information to output file, or to stdout,
    if 'output' was not provided or is a dash ('-').
    """
    vpn_configs = mozvpn.find_vpn_server_locations(config_paths)
    fieldnames = ['interface', 'ip', 'country', 'region', 'city']
    writer = csv.DictWriter(output, fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(vpn_configs)


@click.option('--verbose', '-v', is_flag=True, default=False)
@click.option('--dry-run', '-m', is_flag=True, default=False,
              help='Print all commands to the shell without executing them.')
@click.option('--user', '-u', default=os.getlogin())
@main.command()
def setup(user, dry_run, verbose):
    """Setup the configuration necessary to run MozillaVPN"""
    try:
        wireguard.setup_wireguard_configuration(user, verbose, dry_run)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    except wireguard.ControlledExit:
        sys.exit(1)


@click.command()
def xmozvpn():
    """Start graphical user interface for mozvpn."""
    # This is an alternative for 'mozvpn gui' above.
    try:
        mozvpn_gui.gui()
    except wireguard.ControlledExit:
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
