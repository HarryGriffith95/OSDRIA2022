from PySide2.QtCore import QRect, Signal, QObject
from PySide2.QtWidgets import QGraphicsView, QAbstractScrollArea

from models.data_structure import List


class SceneView(QGraphicsView):
    """set scene rectangle at resize event of view"""
    sidebar_toggled = Signal(QObject)
    commodity_clicked = Signal(QObject)

    def __init__(self, parent):
        super().__init__(parent)
        self.draft_mode = False

    def resizeEvent(self, event):
        self.scene().setSceneRect(QRect(-self.width()/2, -self.height()/2, self.width(), self.height()))

        # adjust scrollbar ranges to viewport (display area) size
        if self.viewport().height() < self.sceneRect().height():
            self.verticalScrollBar().setPageStep(self.viewport().height())
            self.verticalScrollBar().setRange(self.sceneRect().top(),
                                              self.sceneRect().bottom() - self.viewport().height())
        # todo: reset verticalScrollBar
        if self.viewport().width() < self.sceneRect().width():
            self.horizontalScrollBar().setPageStep(self.viewport().width())
            self.horizontalScrollBar().setRange(self.sceneRect().left(),
                                                self.sceneRect().right() - self.viewport().width())
        # todo: reset horizontalScrollBar

    def showEvent(self, event):
        self.scene().draft_mode = self.draft_mode
