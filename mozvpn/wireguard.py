"""
Functions for interacting with wireguard command line tools.
"""
import shutil
import logging
import tempfile
import subprocess

import requests

logger = logging.getLogger(__name__)

# ### The following setup currently works for Linux (and probably MacOS) only.
# ### This should be refactored in order to support Windows as well.
# Wireguard commands:
WIREGUARD_QUICK_CMD = 'sudo -n wg-quick {cmd} {cfg}'
# 'wg show' requires sudo:
# WIREGUARD_SHOW_CMD = 'sudo -n wg show'
# 'wg show interfaces' does not require sudo:
WIREGUARD_SHOW_INTERFACES_CMD = 'wg show interfaces'
WIREGUARD_ETC_DIR = '/etc/wireguard'
WIREGUARD_LOCATIONS_FILE = '/etc/wireguard/locations.csv'


class WireguardError(Exception):
    """Raised when external wireguard or wg-quick command reported an error."""


class CommandError(Exception):
    def __init__(self, msg, cmd):
        super().__init__(msg)
        self.cmd = cmd

    @property
    def msg(self):
        return f'Command failed:\n"{self.cmd}"\nMessage: {str(self)}'


class ControlledExit(Exception):
    """Raise when error handling is finished and program can gracefully exit."""


def run_command(cmd: str, shell: bool = False, verbose: bool = False, dry_run: bool = False) -> str:
    """Run external command, and collect results or errors.

    Args:
        cmd: The command to be executed
        shell: if True run command via shell.
        verbose: if True print command to stdout.
        dry_run: if True then the commands will only be written to stdout only.
            and not executed.

    Raises:
        CommandError in case of failling command execution.
    """
    run_cmd = cmd if shell else cmd.split()
    if verbose or dry_run:
        print(cmd)
    if dry_run:
        return
    try:
        proc = subprocess.run(run_cmd, timeout=20, shell=shell, capture_output=True)
    except FileNotFoundError as exc:
        logger.exception(f'Running "{cmd}" failed. Details:')
        raise CommandError(exc, cmd) from exc
    except subprocess.SubprocessError as exc:
        logger.exception(exc)
        raise CommandError(f'Unexpected error: {str(exc)}', cmd) from exc
    if proc.returncode:
        err = proc.stderr.decode('utf8')
        logger.error('Command "%s" failed: %s', cmd, err)
        raise CommandError(err, cmd)
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
    run_command(wg_quick_cmd)


def disconnect(conf_or_if: str):
    """Shut down connection to VPN server via wg-quick command.

    Args:
        conf_or_if: Either
            - Path to wireguard conf file, e.g. "/path/to/us122-wireguard.conf"
            - Name of wireguard interface, e.g. "us122-wireguard"
              In this case the corresponding configuration file has to exist
              at /etc/wireguard/INTERFACE.conf.
    """
    wg_quick_cmd = WIREGUARD_QUICK_CMD.format(cmd='down', cfg=conf_or_if)
    run_command(wg_quick_cmd)


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


def mullvad_info():
    """Obtain externally visible IP information from https://am.i.mullvad.net/json

    Note: Mullvad is the provider behind MozillaVPN.

    Returns: JSON like
        {
          "ip": "212.14.256.33",
          "country": "Germany",
          "city": "Stadt",
          "longitude": 8.2,
          "latitude": 44.4,
          "mullvad_exit_ip": false,
          "blacklisted": { ... },
          "organization": "Telecom"
        }
    """
    res = requests.get('https://am.i.mullvad.net/json')
    return res.json()


def status(ip: bool = False) -> str:
    """Show status of VPN connection.

    Args:
        ip: if given add currenlty visible external IP address to connection status.
    Returns:
        String telling if VPN connection is up, and if so, which server is currently
        is used. The IP address will optionally be added.
        Examples:
        - 'Not connected'
        - 'Connected to de10-wireguard'
        - 'Connected to de10-wireguard, ip: 234.12.642.0'
    """
    iface = interface()
    if iface:
        if ip:
            ip_addr = ipinfo()["ip"]
            ip_info = f', ip: {ip_addr}'
        else:
            ip_info = ''
        stat_info = f'Connected to: {iface}{ip_info}'
    else:
        stat_info = 'Not connected'
    return stat_info


def interface() -> str:
    """Return interface of VPN connection, if available.

    Returns:
        Name of connected interface (e.g. 'de12-wireguard), otherwise None, if not connected.
    """
    iface = run_command(WIREGUARD_SHOW_INTERFACES_CMD)
    return iface if iface else None


def check_wireguard_commands() -> dict:
    """Check absolute path to 'wg' and 'wg-quick' commands if they are installed
       and executable.

    Returns:
        {'wg': '/usr/bin/wg', 'wg-quick': '/usr/bin/wg-quick'}
    Raises:
        RuntimeError if path to wireguard command could not be determined.
    """
    # Restrict possible path names to secure ones on Linux/macOS systems. This
    # prevents that a user has a local program called 'wg' to which 'sudo root'
    # would be granted.
    allowed_cmd_paths = "/usr/bin:/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin"
    cmds = ['wg', 'wg-quick']
    full_cmds = {}
    for cmd in cmds:
        cmd_path = shutil.which(cmd, path=allowed_cmd_paths)
        if not cmd_path:
            logger.error('Could not find wireguard command %s', cmd)
            raise RuntimeError('Could not find wireguard command "%s"' % cmd)
        full_cmds[cmd] = cmd_path
    return full_cmds


NON_ROOT_SETUP_COMMANDS_LINUX = [
    'chmod 700 {tmp_dir}',
    ('echo "%mozvpn ALL = (root) NOPASSWD: {wg-quick} up, {wg-quick} down" '
     '> {tmp_dir}/mozvpn.sudo'),
    'mozwire relay save -o {tmp_dir} -n 3',
    'mozvpn geolocate {tmp_dir} -o {tmp_dir}/locations.csv',
]
ROOT_SETUP_COMMANDS_LINUX = [
    'groupadd -f mozvpn',
    'usermod -a -G mozvpn {user}',
    'mv {tmp_dir}/mozvpn.sudo /etc/sudoers.d/mozvpn',
    'chmod 440 /etc/sudoers.d/mozvpn',
    'mkdir -p /etc/wireguard',
    'mv {tmp_dir}/* {wireguard_etc_dir}',
    'chown root.root {wireguard_etc_dir}/*',
    'chmod 440 {wireguard_etc_dir}/*.conf',
]


def setup_wireguard_configuration(user: str, verbose: bool, dry_run: bool):
    """Setup configurations needed to operate wireguard.

    Args:
        user: name of primary user who should be allowed to use MozVPN.
        verbose: if True print command to stdout.
        dry_run: if True then the commands will only be written to stdout only.
            and not executed.
    """
    params = check_wireguard_commands()
    params['user'] = user
    params['wireguard_etc_dir'] = WIREGUARD_ETC_DIR

    with tempfile.TemporaryDirectory() as tmp_dir:
        params['tmp_dir'] = tmp_dir

        for cmd in NON_ROOT_SETUP_COMMANDS_LINUX:
            scmd = cmd.format(**params)
            run_command(scmd, shell=True, verbose=verbose, dry_run=dry_run)

        for cmd in ROOT_SETUP_COMMANDS_LINUX:
            scmd = 'sudo ' + cmd.format(**params)
            run_command(scmd, shell=True, verbose=verbose, dry_run=dry_run)

    print(
        "Please add more users to group 'mozvpn' for those who should be allowe to use mozvpn. "
        "You and all added users have logout and login again in order to activate this new group."
    )
