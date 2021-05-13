"""
Functions for interacting with wireguard command line tools.
"""
import logging
import subprocess

import requests

logger = logging.getLogger(__name__)
WIREGUARD_QUICK_CMD = 'sudo -n wg-quick {cmd} {cfg}'
WIREGUARD_CMD = 'sudo -n wg {cmd}'


class WireguardError(Exception):
    """Raised when external wireguard or wg-quick command reported an error."""


def run_wireguard_command(cmd):
    """Run external wireguard command, and collect results or errors."""
    try:
        proc = subprocess.run(cmd.split(), timeout=10, capture_output=True)
    except FileNotFoundError as exc:
        logger.exception(exc)
        raise WireguardError() from exc
    except subprocess.SubprocessError as exc:
        logger.exception(exc)
        raise WireguardError(f'Unexpected error: {str(exc)}') from exc
    if proc.returncode:
        err = proc.stderr.decode('utf8')
        logger.error('Command %s gave error: %s', cmd, err)
        raise WireguardError(err)
    return proc.stdout.decode('utf8').strip()


def connect(conf_or_if: str):
    """Establish connection to VPN server via wg-quick command.

    Args:
        conf_or_if: Either
            - Name of wireguard conf file, e.g. "/path/to/us122-wireguard.conf"
            - Name of wireguard interface, e.g. "us122-wireguard"
              In this case the corresponding configuration file has to exist
              in the /etc/wireguard/ directory.
    """
    wg_quick_cmd = WIREGUARD_QUICK_CMD.format(cmd='up', cfg=conf_or_if)
    run_wireguard_command(wg_quick_cmd)


def disconnect(conf_or_if: str):
    """Shut down connection to VPN server via wg-quick command.

    Args:
        conf_or_if: Either
            - Name of wireguard conf file, e.g. "/path/to/us122-wireguard.conf"
            - Name of wireguard interface, e.g. "us122-wireguard"
              In this case the corresponding configuration file has to exist
              at /etc/wireguard/INTERFACE.conf.
    """
    wg_quick_cmd = WIREGUARD_QUICK_CMD.format(cmd='down', cfg=conf_or_if)
    run_wireguard_command(wg_quick_cmd)


def ipinfo():
    """Obtain externally visible IP information from https://ipinfo.io

    Returns: JSON like
        {
          "ip": "185.213.155.160",
          "city": "Frankfurt am Main",
          "region": "Hesse",
          "country": "DE",
          "loc": "50.1155,8.6842",
          "org": "AS39351 31173 Services AB",
          "postal": "60311",
          "timezone": "Europe/Berlin",
          "readme": "https://ipinfo.io/missingauth"
        }
    """
    res = requests.get('https://ipinfo.io')
    return res.json()


def status(ip=False):
    """Show status of VPN connection."""
    iface = interface()
    if iface:
        if ip:
            ip_addr = ipinfo()["ip"]
            ip_info = f', externally visible ip: {ip_addr}'
        else:
            ip_info = ''
        stat_info = f'Connected to: {iface}{ip_info}'
    else:
        stat_info = 'Not connected'
    return stat_info


def interface():
    """Show interface of VPN connection, if available.

    Returns:
        Name of connected interface, otherwise None, if not connected.
    """
    wg_cmd = WIREGUARD_CMD.format(cmd='show interfaces')
    iface = run_wireguard_command(wg_cmd)
    return iface if iface else None
