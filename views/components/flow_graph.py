from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy as np

from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QCursor, QPixmap
from PySide2.QtWidgets import QWidget, QVBoxLayout

from models.constants import ZoomType


class FlowGraph(QWidget):
    """define functionality of chart view in dataset dialog"""
    def __init__(self, parent):
        super(FlowGraph, self).__init__(parent)
        self.cursor_shape = {
            ZoomType.SELECT: Qt.ArrowCursor,
            ZoomType.ZOOM_IN: QCursor(QPixmap(":/icons/img/zoom-in_normal@2x.png")),
            ZoomType.ZOOM_OUT: QCursor(QPixmap(":/icons/img/zoom-out_normal@2x.png")),
            ZoomType.ZOOM_RANGE: QCursor(QPixmap(":/icons/img/zoom-range_normal@2x.png"))
        }
        self._model = None
        self._drag = None
        self._zoom_type = ZoomType.SELECT

        self._canvas = FigureCanvasQTAgg(Figure())
        self._canvas.mpl_connect('button_press_event', self.on_press)
        self._canvas.mpl_connect('motion_notify_event', self.on_move)
        self._canvas.mpl_connect('button_release_event', self.on_release)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self._canvas)
        self._canvas.axes = self._canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

    def set_zoom_mode(self, zoom_mode):
        self._zoom_type = zoom_mode
        self.setCursor(self.cursor_shape[zoom_mode])

    def set_data(self, process_dict):
        self._canvas.axes.clear()
        self._canvas.axes.set_title("Commodity Flow")
        for direction, processes in process_dict.items():
            process_lines = []
            process_labels = []
            multiplier = 1
            if direction == "input_processes":
                multiplier = -1
            for process, commodity_flow in processes.items():
                repetition_array = np.repeat(int(8760/len(commodity_flow)), len(commodity_flow)-1)
                process_lines.append(multiplier * np.repeat(np.array(commodity_flow),
                                                            np.hstack([repetition_array, 8760-sum(repetition_array)])))
                process_labels.append(process)

            x_values = range(len(process_lines[0]))
            self._canvas.axes.stackplot(x_values, process_lines, labels=process_labels)

        self._canvas.axes.legend(loc='upper left')
        self._canvas.draw()

    def on_press(self, event):
        if event.button != 1:
            return

        left, right = self._canvas.axes.get_xlim()
        if self._zoom_type == ZoomType.ZOOM_IN:
            new_half_width = (right - left) / 4
            left = max(event.xdata - new_half_width, 0)
            right = min(event.xdata + new_half_width, 8760)
            self._canvas.axes.set_xlim(left, right)
            self._canvas.draw()
        elif self._zoom_type == ZoomType.ZOOM_OUT:
            new_half_width = right - left
            left = max(event.xdata - new_half_width, 0)
            right = min(event.xdata + new_half_width, 8760)
            self._canvas.axes.set_xlim(left, right)
            self._canvas.draw()
        elif self._zoom_type == ZoomType.SELECT:
            self._drag = event.xdata

    def on_move(self, event):
        if self._drag is None:
            return
        delta_x = event.xdata - self._drag
        left, right = self._canvas.axes.get_xlim()
        left -= delta_x
        right -= delta_x
        if (left >= 0) & (right <= 8760):
            self._canvas.axes.set_xlim(left, right)
            self._canvas.draw()

    def on_release(self, _):
        self._drag = None
