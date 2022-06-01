from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QCursor, QPixmap
from PySide2.QtCharts import QtCharts

from models.constants import ZoomType


class CommodityFlowGraph(QtCharts.QChartView):
    """define functionality of chart view in dataset dialog"""
    def __init__(self, parent):
        super(CommodityFlowGraph, self).__init__(parent)
        self.cursor_shape = {
            ZoomType.SELECT: Qt.ArrowCursor,
            ZoomType.ZOOM_IN: QCursor(QPixmap(":/icons/img/zoom-in_normal@2x.png")),
            ZoomType.ZOOM_OUT: QCursor(QPixmap(":/icons/img/zoom-out_normal@2x.png")),
            ZoomType.ZOOM_RANGE: QCursor(QPixmap(":/icons/img/zoom-range_normal@2x.png"))
        }
        self._model = None
        self._zoom_type = ZoomType.SELECT
        self._series = QtCharts.QLineSeries()
        self.setChart(QtCharts.QChart())
        self.chart().setTitle("Commodity Flow")

    def set_zoom_mode(self, zoom_mode):
        self._zoom_type = zoom_mode
        self.setCursor(self.cursor_shape[zoom_mode])

    def set_data(self, process_dict):
        self.chart().removeAllSeries()
        for direction, processes in process_dict.items():
            process_lines = []
            multiplier = 1
            if direction == "input_processes":
                multiplier = -1
            for process, commodity_flow in processes.items():
                # create line series for each process's commodity flow
                process_lines.append(QtCharts.QLineSeries())
                for index, flow_value in enumerate(commodity_flow):
                    last_line_y_value = process_lines[-2].at(index).y() if (len(process_lines) > 1) else 0
                    process_lines[-1].append(index, last_line_y_value + multiplier * flow_value)
                process_lines[-1].setName(process)
                self.chart().addSeries(process_lines[-1])

        self.chart().createDefaultAxes()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._zoom_type == ZoomType.ZOOM_IN:
                plot_rect = self.chart().plotArea()
                left_position = event.x() - plot_rect.width() / 4
                self.chart().zoomIn(QRectF(left_position, plot_rect.top(), plot_rect.width()/2, plot_rect.height()))
            elif self._zoom_type == ZoomType.ZOOM_OUT:
                self.chart().zoomReset()

        super().mouseReleaseEvent(event)
