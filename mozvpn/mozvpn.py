"""Main module."""
import re
import pathlib
import logging
from typing import List, Dict

import requests

logger = logging.getLogger(__name__)

ENDPOINT_RE = re.compile(r'Endpoint\s*=\s*(?P<ip>\d+\.\d+\.\d+\.\d+)')
IPINFO_URL = 'https://ipinfo.io'


def determine_ip_location(ip: str) -> Dict:
    """Determine location of IP address.

    Args:
        ip: IP address
    Returns:
        dict containing (among others) fields country, region, city
    """
    req = requests.get(f'{IPINFO_URL}/{ip}')
    return req.json()


def find_vpn_server_locations(wg_config_files: List[str]):
    """Find geographic locations of wireguard VPN server endpoints.

    Args:
        wg_config_files: list of wireguard config files/directories
    Returns:
        list of dictionaries containing configuration/location data.
    """
    wg_configs = []
    for conf_path in wg_config_files:
        p_conf_path = pathlib.Path(conf_path)
        if p_conf_path.is_dir():
            # Find all wireguard config files in given directory:
            wg_configs.extend(
                {'conf': gp for gp in p_conf_path.glob('*.conf')}
            )
        else:
            # The file itself is assumed to be a wireguard config file:
            wg_configs.append({'conf': p_conf_path})

    # Extract IP addresses of server endpoints from wireguard config files
    # and determine their geographic location:
    for wg_config in wg_configs:
        conf = wg_config['conf'].read_text()
        match = ENDPOINT_RE.search(conf)
        if match:
            ip = match.group('ip')
            wg_config.update(determine_ip_location(ip))
        else:
            wg_config['ip'] = None
            logger.warning(
                'Cannot find endpoint IP in wireguard configfile %s', wg_config['conf']
            )
    return wg_configs
