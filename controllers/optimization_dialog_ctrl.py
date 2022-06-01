from PySide2.QtCore import QObject, QCoreApplication

from core.optimization_tool import Optimizer


class OptimizationDialogCtrl(QObject):
    """controller for property dialog view"""
    def __init__(self, project_elements, project_file):
        super(OptimizationDialogCtrl, self).__init__()
        self._optimizer = None
        self._model = project_elements
        self._project_file = project_file

    def run_optimization(self):
        self._optimizer = Optimizer(self._model.process_list, self._model.commodity_list)
        self._optimizer.progress_text_sent.connect(self.assign)

        self.assign("Converting Optimization Code")
        self._optimizer.translate()

        #self._optimizer.get_model(self._project_file.fileName())
        #self._optimizer.relax()
        #self._optimizer.write(self._project_file.fileName())

        self.assign("Running Optimization")
        results = self._optimizer.solve(self._project_file.fileName())
        self.assign(results.solver.termination_condition)

        self.assign("Retrieving Results")
        self._optimizer.set_results()

        self._optimizer.get_sensitivities(self._project_file.fileName())

    def get_model(self):
        return self._optimizer.get_model()

    def assign(self, text):
        QCoreApplication.processEvents()
        print(text)
        self._model.optimization_text = text
        QCoreApplication.processEvents()

    def cancel_optimization(self):
        self._optimizer.cancel()
