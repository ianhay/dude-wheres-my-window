import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon


class DudeWheresMyWindowPlugin:

    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        self.action = QAction(
            QIcon(icon_path),
            "Dude, where's my window?",
            self.iface.mainWindow()
        )
        self.action.setToolTip(
            "Round up all floating QGIS windows and bring them onto the map canvas screen"
        )
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Dude, where's my window?", self.action)

    def unload(self):
        self.iface.removePluginMenu("&Dude, where's my window?", self.action)
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        from .bring_windows_home import bring_windows_home
        bring_windows_home(self.iface)  # pass iface explicitly, no globals needed
