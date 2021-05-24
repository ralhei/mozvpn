"""Qt6 based GUI frontend for mozilla VPN."""
import csv
import logging

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QComboBox, QMessageBox, QSizePolicy, QMainWindow

from mozvpn import wireguard

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    MozVPN GUI window.
    """
    def __init__(self):
        """Compose main window widgets."""
        super().__init__()
        self.wireguard_interface = None

        self.setWindowTitle('MozVPN')

        vlayout = QVBoxLayout()
        vlayout.addWidget(QLabel('<h2>MozVPN</h2>'))

        self.combo = QComboBox()
        self._fill_vpn_choice_combo()
        vlayout.addWidget(self.combo)

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.toggle_connect)
        self.connect_button.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum
        )
        hlayout = QHBoxLayout()
        hlayout.addStretch()
        hlayout.addWidget(self.connect_button)
        hlayout.addStretch()
        vlayout.addLayout(hlayout)

        container = QWidget()
        container.setLayout(vlayout)
        self.setCentralWidget(container)

        self.show()

        # Check whether VPN is already running:
        try:
            iface = wireguard.interface()
        except wireguard.CommandError as exc:
            QMessageBox.critical(self, 'Error', exc.msg)
            raise wireguard.ControlledExit()
        if iface:
            # VPN is already up when GUI was started:
            self.wireguard_interface = iface
            self.update_gui_activity_status()
            QMessageBox.information(self, 'Information', 'VPN is already running')

        # Create timer to regularly check the underlying VPN connectivity:
        self.connectivity_update_timer = QTimer()
        self.connectivity_update_timer.setInterval(1000)  # fire every 1000ms
        self.connectivity_update_timer.timeout.connect(self.update_connectivity)
        self.connectivity_update_timer.start()

    def _fill_vpn_choice_combo(self):
        """Fill the VPN server combobox from geolocation csv file."""
        try:
            fp = open(wireguard.WIREGUARD_LOCATIONS_FILE)
        except FileNotFoundError:
            QMessageBox.critical(
                self, 'Error',
                'File "locations.csv" could not be found.\nDid you run "mozvpn setup"?')
            raise wireguard.ControlledExit()
        server_locations = csv.DictReader(fp)
        for loc in server_locations:
            # Split an interface name like 'de4-wireguard' and only save the 'de4'-part:
            loc['iface'] = loc['interface'].split('-')[0]
            loc_str = '{country} - {region} - {city} ({iface})'.format(**loc)
            self.combo.addItem(loc_str, loc['interface'])

    def closeEvent(self, event):
        """Catch close event. If active VPN connection, ask for confirmation."""
        if self.wireguard_interface:
            reply = QMessageBox.question(
                self, 'Quit', 'Are you sure you want to quit and stop the active VPN?'
            )
            if reply == QMessageBox.StandardButtons.Yes:
                self.toggle_connect(force_off=True)
            else:
                event.ignore()

    def update_connectivity(self):
        """Find out which VPN connection currently exists, and update GUI accordingly.

        This method will be called regularly via self.connectivity_update_timer.
        Background: The VPN connection cannot only be changed thru the MozVPN GUI,
        but also via the command line tools. This method syncs the state of the GUI
        with the real actual VPN situation of the system.
        """
        logger.debug('Updatting connectivity status via timer.')
        iface = wireguard.interface()
        if iface != self.wireguard_interface:
            self.wireguard_interface = iface
            self.update_gui_activity_status()
            QMessageBox.warning(self, 'Warning', 'VPN connection got changed!')

    def update_gui_activity_status(self):
        """Update the GUI according to the current VPN connectivity settings."""
        if not self.wireguard_interface:
            button_text = 'Connect'
            button_color = 'none'
        else:
            button_text = 'Disconnect'
            button_color = 'red'
            idx = self.combo.findData(self.wireguard_interface)
            self.combo.setCurrentIndex(idx)
        self.connect_button.setText(button_text)
        self.connect_button.setStyleSheet(f"background-color: {button_color}")
        self.combo.setEnabled(self.wireguard_interface is None)

    def toggle_connect(self, force_off: bool = False):
        """Toggle (connect or disconnect) Mozilla VPN connection.

        Args:
            force_off: if True this command only works for turning off VPN.
        """
        try:
            if not self.wireguard_interface and not force_off:
                iface = wireguard.interface()
                if iface:
                    QMessageBox.warning(self, 'Warning', 'VPN is already running!')
                else:
                    iface = self.combo.currentData()
                    wireguard.connect(iface)
            else:
                iface = wireguard.interface()
                if iface != self.wireguard_interface:
                    # This should actually not happen: The GUI shows a different VPN
                    # interface than the one reported by wireguard. This can only happen
                    # if the VPN was changed outside the GUI, e.g. via mozpvn command line.
                    logger.warning(f'wireguard interface shown in GUI ({self.wireguard_interface}) '
                                   f'does not match interface reported by "wg show" command ({iface}).')
                if iface:
                    # Could be None if VPN connection was already down or turned off otherwise.
                    wireguard.disconnect(iface)
                iface = None
        except wireguard.WireguardError as exc:
            QMessageBox.critical(self, 'Error', str(exc))
        else:
            self.wireguard_interface = iface
            self.update_gui_activity_status()


def gui():
    """Main gui function, to be called from cli.py"""
    app = QApplication([])
    _ = MainWindow()
    app.exec()
