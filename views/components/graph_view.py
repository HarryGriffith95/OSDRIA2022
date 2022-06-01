from PySide2.QtCharts import QtCharts


class GraphView(QtCharts.QChartView):
    """define functionality of chart view in dataset dialog"""
    def __init__(self, parent):
        super(GraphView, self).__init__(parent)
        self._model = None
        self._series = QtCharts.QLineSeries()

    def set_model(self, model):
        """set dataset model for displaying in line chart"""
        self._model = model
        model.dataChanged.connect(self.reset_chart)
        model.modelReset.connect(self.reset_chart)

        chart = QtCharts.QChart()
        self.setChart(chart)

    def reset_chart(self, start_index=0, end_index=0):
        self.chart().removeAllSeries()
        self._series = QtCharts.QLineSeries()
        for index, data in enumerate(self._model.retrieve_data()):
            try:
                self._series.append(index, float(data))
            except ValueError:
                pass
        self.chart().addSeries(self._series)
        self.chart().createDefaultAxes()
        self.chart().legend().hide()
