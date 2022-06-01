import sys

from PySide2.QtCore import QFile, Qt
from PySide2.QtWidgets import QApplication

from models.model import Model
from controllers.welcome_ctrl import WelcomeCtrl
from controllers.project_ctrl import ProjectCtrl
from views.welcome_view import WelcomeView
from views.project_view import ProjectView


class App(QApplication):
    """top-level class of app"""

    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        # setting high DPI support
        self.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        self.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        # load stylesheet
        with open('resources/style.css') as style_file:
            self.setStyleSheet(style_file.read())
            style_file.close()

        # display welcome dialog
        self.welcome_controller = WelcomeCtrl()
        self.welcome_view = WelcomeView(self.welcome_controller)
        if not self.welcome_view.exec_():
            sys.exit(0)

        # create new or open existing model
        self.model = Model(
            self.welcome_controller.filename,
            self.welcome_controller.new_project)

        # display project window
        self.project_controller = ProjectCtrl(self.model)
        self.project_view = ProjectView(self.model, self.project_controller)
        self.project_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
