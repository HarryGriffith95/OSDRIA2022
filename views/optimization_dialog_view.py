from PySide2.QtCore import Qt, QObject, QSize, QModelIndex, Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QDialog, QStyledItemDelegate, QPushButton, QWidget, QStyle, QHeaderView, QFileDialog

from views.optimization_dialog_view_ui import Ui_OptimizationDialog


class OptimizationDialogView(QDialog):
    """Optimization Dialog View"""

    def __init__(self, dialog_model, dialog_controller):
        settings = Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        super(OptimizationDialogView, self).__init__(None, settings)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._model = dialog_model
        self._ctrl = dialog_controller
        self._ui = Ui_OptimizationDialog()
        self._ui.setupUi(self)

        """connect widgets to controller"""
        self._ui.cancel_button.clicked.connect(self.reject)
        self.rejected.connect(self._ctrl.cancel_optimization)

        """listen for model event signals"""
        self._model.text_changed.connect(self._ui.information_text.setText)

        """initialize view"""
        self._model.optimization_text = "Optimization Started"

    def show(self):
        super().show()
        self.setModal(True)
        self._ctrl.run_optimization()
        self.close()

    def keyPressEvent(self, event):
        """prevent dialog closing with enter or return key"""
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return
        elif event.matches(QKeySequence.Print):
            file_name = QFileDialog.getSaveFileName(self, "Export Pyomo Model", "model.txt")[0]
            file = open(file_name, "w")
            file.write(self._ctrl.get_model())
            file.close()
        super().keyPressEvent(event)
