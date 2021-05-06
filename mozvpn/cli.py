"""Console script for mozvpn."""
import sys
import csv
import click

from mozvpn import mozvpn, mozvpn_gui


@click.group()
def main():
    ...


@main.command()
def gui():
    mozvpn_gui.gui()


@click.argument('config_paths', nargs=-1)
@click.option('-o', '--output', type=click.File('w'), default='-')
@main.command()
def geolocate(config_paths, output):
    """Determine geographic location for server endpoints in given config files or directories.

    Write the csv-formatted vpn server information to output file, or to stdout,
    if 'output' was not provided or is a dash ('-').
    """
    vpn_configs = mozvpn.find_vpn_server_locations(config_paths)
    fieldnames = ['conf', 'ip', 'country', 'region', 'city']
    writer = csv.DictWriter(output, fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(vpn_configs)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
