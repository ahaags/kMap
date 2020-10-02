# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDir, pyqtSignal

# Own Imports
from kmap import __directory__
from kmap.config.config import config

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfitoptions.ui')
LMFitOptions_UI, _ = uic.loadUiType(UI_file)


class LMFitOptions(QWidget, LMFitOptions_UI):

    fit_triggered = pyqtSignal()
    region_changed = pyqtSignal(str, bool)
    background_changed = pyqtSignal(str, list)
    method_changed = pyqtSignal(str)
    slice_policy_changed = pyqtSignal(str)

    def __init__(self):

        # Setup GUI
        super(LMFitOptions, self).__init__()
        self.setupUi(self)
        self._setup()
        self._connect()

    def get_region(self):

        text = self.region_comboBox.currentText()

        if text == 'Entire kMap':
            region = 'all'
            inverted = False

        elif text == 'Only ROI':
            region = 'roi'
            inverted = False

        elif text == 'Only Annulus':
            region = 'ring'
            inverted = False

        elif text == 'Except ROI':
            region = 'roi'
            inverted = True

        elif text == 'Except Annulus':
            region = 'ring'
            inverted = True

        return region, inverted

    def get_method(self):

        text = self.method_combobox.currentText()

        return text[text.find("(") + 1:text.find(")")]

    def get_slice_policy(self):

        index = self.slice_combobox.currentIndex()

        if index == 0:
            return 'only one'

        elif index == 1:
            return 'all'

        else:
            return 'all combined'

    def get_background(self):

        equation = self.line_edit.text()
        variables = []

        return equation, variables

    def _change_region(self):

        region, inverted = self.get_region()

        self.region_changed.emit(region, inverted)

    def _change_method(self):

        method = self.get_method()

        self.method_changed.emit(method)

    def _change_slice_policy(self):

        slice_policy = self.get_slice_policy()

        self.slice_policy_changed.emit(slice_policy)

    def _change_background(self):

        equation, variables = self.get_background()
        self.background_changed.emit(equation, variables)

    def _setup(self):
        pass
        # TO DO: Get equations from config

    def _connect(self):

        self.fit_button.clicked.connect(self.fit_triggered.emit)
        self.region_comboBox.currentIndexChanged.connect(
            self._change_region)
        self.method_combobox.currentIndexChanged.connect(self._change_method)
        self.slice_combobox.currentIndexChanged.connect(
            self._change_slice_policy)
        self.line_edit.returnPressed.connect(self._change_background)