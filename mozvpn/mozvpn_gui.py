"""Qt6 based GUI frontend for mozilla VPN."""
import csv
import threading
import time

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QComboBox, QMessageBox, QSizePolicy, QMainWindow

from mozvpn import wireguard


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
        vlayout.addWidget(QLabel('<h2>MozillaVPN Connector</h2>'))

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
        iface = wireguard.interface()
        if iface:
            self.wireguard_interface = iface
            self.update_gui_activity_status()
            QMessageBox.information(self, 'Information', 'VPN is already running')

        self.update_thread = threading.Thread(target=self._update_connect_in_thread, daemon=True)
        # self.update_thread.run()  ----- must us Qt6 threads instead!!!

    def _fill_vpn_choice_combo(self):
        """Fill the VPN server combobox from geolocation csv file."""
        fp = open('server-locations.csv')
        server_locations = csv.DictReader(fp)
        for loc in server_locations:
            loc_str = '{country} - {region} - {city}'.format(**loc)
            self.combo.addItem(loc_str, loc['interface'])

    def closeEvent(self, event):
        """Catch close event. If active VPN connection, ask for confirmation."""
        if self.wireguard_interface:
            reply = QMessageBox.question(
                self, 'Quit', 'Are you sure you want to quit and stop the active VPN?'
            )
            if reply == QMessageBox.StandardButtons.Yes:
                vpn_config_file = self.combo.currentData()
                wireguard.disconnect(vpn_config_file)
            else:
                event.ignore()

    def _update_connect_in_thread(self):
        """Running in background thread for checking current VPN connectivty situation."""
        while True:
            time.sleep(.25)
            print('updating in thread')
            self.update_connect()

    def update_connect(self):
        """Find out which VPN connection currently exists, and update GUI accordingly."""
        iface = wireguard.interface()
        if iface != self.wireguard_interface:
            self.wireguard_interface = iface
            self.update_gui_activity_status()
            QMessageBox.warning(self, 'Warning', 'VPN connection got changed!')

    def update_gui_activity_status(self):
        if not self.wireguard_interface:
            button_text = 'Connect'
            button_color = 'none'
        else:
            button_text = 'Disconnect'
            button_color = 'red'
        self.connect_button.setText(button_text)
        self.connect_button.setStyleSheet(f"background-color: {button_color}")
        self.combo.setEnabled(self.wireguard_interface is None)

    def toggle_connect(self):
        """Toggle (connect or disconnect) Mozilla VPN connection."""
        try:
            if not self.wireguard_interface:
                iface = wireguard.interface()
                if iface:
                    QMessageBox.warning(self, 'Warning', 'VPN has been turned on already!')
                else:
                    iface = self.combo.currentData()
                    wireguard.connect(iface)
            else:
                iface = wireguard.interface()
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
    MainWindow()
    app.exec()
