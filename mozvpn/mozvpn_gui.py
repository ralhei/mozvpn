"""Qt6 based GUI frontend for mozilla VPN."""
import csv
import subprocess

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QComboBox, QMessageBox, QSizePolicy, QMainWindow


class MainWindow(QMainWindow):
    """
    MozVPN GUI window.
    """
    def __init__(self):
        """Compose main window widgets."""
        super().__init__()
        self.vpn_active = False

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

    def _fill_vpn_choice_combo(self):
        """Fill the VPN server combobox from geolocation csv file."""
        fp = open('server-locations.csv')
        server_locations = csv.DictReader(fp)
        for loc in server_locations:
            loc_str = '{country} - {region} - {city}'.format(**loc)
            self.combo.addItem(loc_str, loc['conf'])

    def closeEvent(self, event):
        """Catch close event. If active VPN connection, ask for confirmation."""
        if self.vpn_active:
            reply = QMessageBox.question(
                self, 'Quit', 'Are you sure you want to quit and stop the active VPN?'
            )
            if reply == QMessageBox.StandardButtons.Yes:
                self.run_wg_quick_cmd('down')
            else:
                event.ignore()

    def toggle_connect(self):
        """Toggle (connect or disconnect) Mozilla VPN connection."""
        if self.vpn_active:
            button_text = 'Connect'
            button_color = 'none'
            vpn_cmd_arg = 'down'
        else:
            button_text = 'Disconnect'
            button_color = 'red'
            vpn_cmd_arg = 'up'

        if not self.run_wg_quick_cmd(vpn_cmd_arg):
            # Running the VPN command was not successful!
            return

        self.vpn_active = not self.vpn_active
        self.connect_button.setText(button_text)
        self.connect_button.setStyleSheet(f"background-color: {button_color}")
        self.combo.setEnabled(not self.vpn_active)

    def run_wg_quick_cmd(self, vpn_cmd_arg: str):
        """Run the external 'sudo wg-quick <up/down> cfg-file command.

        Args:
            vpn_cmd_arg: either 'up' or 'down'
        Returns:
            True if successful, else False
        """
        vpn_config_file = self.combo.currentData()
        wg_quick_cmd = f'xecho sudo -n wg-quick {vpn_cmd_arg} {vpn_config_file}'.split()
        try:
            proc = subprocess.run(wg_quick_cmd, timeout=10, capture_output=True)
        except FileNotFoundError as exc:
            QMessageBox.critical(self, 'Error', str(exc))
            return False
        if proc.returncode:
            QMessageBox.critical(self, 'Error', proc.stderr.decode('utf8'))
            return False
        return True


def gui():
    """Main gui function, to be called from cli.py"""
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
