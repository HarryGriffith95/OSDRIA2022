from PySide2.QtCore import QObject


class DraftbarElementCtrl(QObject):
    """controller for draft element category in sidebar"""
    def __init__(self, model):
        super(DraftbarElementCtrl, self).__init__()
        self._model = model

