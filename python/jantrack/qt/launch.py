



import sys
from PyQt5 import QtWidgets
from qt.jantrack import Jantrack


def run_jantrack():

    app = QtWidgets.QApplication(sys.argv)
    jantrack_ui = Jantrack()
    jantrack_ui.show()
    sys.exit(app.exec())