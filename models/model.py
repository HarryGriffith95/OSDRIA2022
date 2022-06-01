from PySide2.QtCore import QObject, Signal

from models.constants import OverviewSelection, PageType, SelectConnect, ZoomType
from models.scenario import Scenario
from models.element import *
from models.data_structure import *
from models.model_template import *

# set unique identifier for OSDRIA file
FILE_TYPE = 0x4F534452


class Model(QObject):
    """application model
    @param: filename
    @param: newProject
    @function: save()
    @function: load()
    @signal: filename_changed(str)
    @signal: current_page_changed(OverviewType)
    @signal: overview_selection_changed(str)
    @signal: overview_properties_changed(List)
    @signal: scenarios_changed()
    @signal: current_section_changed()
    @signal: project_elements_changed()
    @signal: overview_sidebar_out_changed(Boolean)
    @signal: sections_sidebar_out_changed(Boolean)
    @signal: draft_sidebar_out_changed(Boolean)
    @signal: current_commodity_changed(Commodity)
    @signal: current_process_changed(Process)
    @signal: draft_select_mode_changed(SelectConnect)
    @signal: graph_zoom_mode_changed(ZoomType)
    """
    filename_changed = Signal(str)
    overview_selection_changed = Signal(int)
    overview_properties_changed = Signal(List)
    scenarios_changed = Signal()
    current_section_changed = Signal(int)
    current_page_changed = Signal(int)
    project_elements_changed = Signal()
    overview_sidebar_out_changed = Signal(bool)
    sections_sidebar_out_changed = Signal(bool)
    draft_sidebar_out_changed = Signal(bool)
    current_commodity_changed = Signal(QObject)
    current_process_changed = Signal(QObject)
    draft_select_mode_changed = Signal(int)
    graph_zoom_mode_changed = Signal(int)

    def __init__(self, file_name, new_project=False):
        """initialise new or load existing model"""
        super(Model, self).__init__()

        self._current_page = PageType.OVERVIEW
        self._current_section = self._current_page
        self._overview_selection = OverviewSelection.OVERVIEW
        self._overview_properties = ModelTemplate.overview_properties()
        self.scenarios = ModelTemplate.scenarios()
        self.commodities = ModelTemplate.commodities()
        self.time_series = ModelTemplate.time_series()
        self.process_cores = ModelTemplate.process_cores(self.commodities, self.time_series)
        self.project_elements = ModelTemplate.project_elements()
        self._overview_sidebar_out = True
        self._sections_sidebar_out = True
        self._draft_sidebar_out = True

        self._project_file = QFile(file_name)
        if new_project is True:
            self.save()
        else:
            self.load()

    def save(self):
        """save model to file"""
        self._project_file.open(QIODevice.WriteOnly)
        data_output = QDataStream(self._project_file)

        # set checkable data
        data_output.setVersion(QDataStream.Qt_5_12)
        data_output.writeUInt32(FILE_TYPE)

        # write model data to file
        data_output.writeUInt32(self._current_page.value)
        data_output.writeUInt32(self._overview_selection.value)
        self._overview_properties.write(data_output)
        self.commodities.write(data_output)
        self.time_series.write(data_output)
        self.process_cores.write(data_output)
        self.project_elements.write(data_output)
        self._project_file.close()

    def load(self):
        """load model to file"""
        self._project_file.open(QIODevice.ReadOnly)
        data_input = QDataStream(self._project_file)

        # check for correct file
        version = data_input.version()
        file_type = data_input.readUInt32()
        if data_input.version() != QDataStream.Qt_5_12:
            raise RuntimeError
        if file_type != FILE_TYPE:
            raise RuntimeError

        # read file data to model
        self._current_page = PageType(data_input.readUInt32())
        self._current_section = self._current_page.name.title()
        self._overview_selection = OverviewSelection(data_input.readUInt32())
        self._overview_properties.read(data_input)
        self.commodities.read(data_input)
        self.time_series.read(data_input)
        self.process_cores.read(data_input)
        self.project_elements.read(data_input)
        self._project_file.close()

    @property
    def project_file(self):
        return self._project_file

    @property
    def current_page(self):
        return self._current_page

    @current_page.setter
    def current_page(self, value):
        if value in PageType:
            self._current_page = value
            self.current_page_changed.emit(value.value)
        else:
            raise AttributeError

    @property
    def overview_selection(self):
        return self._overview_selection

    @overview_selection.setter
    def overview_selection(self, value):
        self._overview_selection = value
        self.overview_selection_changed.emit(value.value)

    @property
    def overview_properties(self):
        return self._overview_properties

    @overview_properties.setter
    def overview_properties(self, value):
        self._overview_properties = value
        self.overview_properties_changed.emit(value)

    @property
    def current_section(self):
        return self._current_section

    @current_section.setter
    def current_section(self, value):
        if value in OverviewSelection:
            self._current_section = value
            self.current_section_changed.emit(value.value)
        else:
            raise AttributeError

    @property
    def overview_sidebar_out(self):
        return self._overview_sidebar_out

    @overview_sidebar_out.setter
    def overview_sidebar_out(self, value):
        self._overview_sidebar_out = value
        self.overview_sidebar_out_changed.emit(value)

    @property
    def sections_sidebar_out(self):
        return self._sections_sidebar_out

    @sections_sidebar_out.setter
    def sections_sidebar_out(self, value):
        self._sections_sidebar_out = value
        self.sections_sidebar_out_changed.emit(value)

    @property
    def draft_sidebar_out(self):
        return self._draft_sidebar_out

    @draft_sidebar_out.setter
    def draft_sidebar_out(self, value):
        self._draft_sidebar_out = value
        self.draft_sidebar_out_changed.emit(value)

    @property
    def current_commodity(self):
        return self._current_commodity

    @current_commodity.setter
    def current_commodity(self, value):
        self._current_commodity = value
        self.current_commodity_changed.emit(value)

    @property
    def current_process(self):
        return self._current_process

    @current_process.setter
    def current_process(self, value):
        self._current_process = value
        self.current_process_changed(value)

    @property
    def draft_select_mode(self):
        return self._draft_select_mode

    @draft_select_mode.setter
    def draft_select_mode(self, value):
        if value in SelectConnect:
            self._draft_select_mode = value
            self.draft_select_mode_changed.emit(value.value)
        else:
            raise AttributeError

    @property
    def graph_zoom_mode(self):
        return self._graph_zoom_mode

    @graph_zoom_mode.setter
    def graph_zoom_mode(self, value):
        if value in ZoomType:
            self._graph_zoom_mode = value
            self.graph_zoom_mode_changed.emit(value.value)
        else:
            raise AttributeError

    @property
    def current_graph_commodity(self):
        return self._current_graph_commodity

    @current_graph_commodity.setter
    def current_graph_commodity(self, value):
        self._current_graph_commodity = value
        self.current_graph_commodity_changed.emit(value.value)
