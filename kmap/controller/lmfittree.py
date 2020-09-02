# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget, QHeaderView, QHBoxLayout

# Own Imports
from kmap import __directory__
from kmap.controller.orbitaltablerow import OrbitalTableRow
from kmap.controller.lmfittreeitems import (
    OrbitalTreeItem, OtherTreeItem, DataTreeItem)

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/lmfittree.ui')
LMFitTree_UI, _ = uic.loadUiType(UI_file)


class LMFitTree(QWidget, LMFitTree_UI):

    item_selected = pyqtSignal()

    def __init__(self, orbitals, *args, **kwargs):

        # Setup GUI
        super(LMFitTree, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup(orbitals)
        self._connect()

    def get_selected_orbital_ID(self):

        selected_items = self.tree.selectedItems()

        for item in selected_items:
            if isinstance(item, OrbitalTreeItem):
                return item.ID

            elif (isinstance(item, DataTreeItem) and
                  isinstance(item.parent(), OrbitalTreeItem)):
                return item.parent().ID

        return -1

    def get_parameters(self):

        parameters = [self.tree.topLevelItem(i).get_parameters()
                      for i in
                      range(self.tree.topLevelItemCount())]

        return parameters

    def _setup(self, orbitals):

        widths = [60, 0, 100, 80, 130, 130, 130, 200]

        for col, width in enumerate(widths):
            self.tree.setColumnWidth(col, width)

        self.tree.header().setResizeMode(1, QHeaderView.Stretch)
        self.tree.header().setDefaultAlignment(Qt.AlignCenter)

        # Add TreeItems
        self.tree.addTopLevelItem(OtherTreeItem(self.tree))
        for orbital in orbitals:
            self.tree.addTopLevelItem(OrbitalTreeItem(self.tree, orbital))

    def _item_selected(self):

        self.item_selected.emit()

    def _connect(self):

        self.tree.itemSelectionChanged.connect(self._item_selected)
