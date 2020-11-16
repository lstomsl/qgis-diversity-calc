from qgis.PyQt.QtWidgets import *
from .diversity_results_dialog_ui import Ui_dlgResults


class DlgResults(QDialog, Ui_dlgResults):
    def __init__(self):
        super(DlgResults, self).__init__()
        self.setupUi(self)

        self.setLayout(self.lytMain)
        self.trwResults.setColumnWidth(0, 250)
        self.trwResults.setColumnWidth(1, 80)
        self.trwResults.setColumnWidth(2, 80)
        self.trwResults.setColumnWidth(3, 80)
        self.trwResults.setColumnWidth(4, 80)
        self.trwResults.setColumnWidth(5, 80)
