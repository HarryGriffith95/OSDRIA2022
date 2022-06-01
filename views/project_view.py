from PySide2.QtWidgets import *

from views.components.section_scene import SectionScene
from views.project_view_ui import Ui_MainWindow

from models.constants import *
from models.property import PropertyPopupMenu, PropertyLineEdit
from models.data_structure import List


class ProjectView(QMainWindow):
    """Main Project window"""

    def __init__(self, model, project_controller):
        super(ProjectView, self).__init__()

        self._model = model
        self._project_ctrl = project_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        """connect widgets to controller"""
        # menu bar
        self._ui.action_save.triggered.connect(self._project_ctrl.save_model)
        self._ui.action_close.triggered.connect(self.close)
        self._ui.action_commodities.triggered.connect(
            self._project_ctrl.open_commodity_dialog)
        self._ui.action_processes.triggered.connect(
            self._project_ctrl.open_process_dialog)
        self._ui.action_timeseries.triggered.connect(
            self._project_ctrl.open_time_series_dialog)
        self._ui.action_scenarios.triggered.connect(
            self._project_ctrl.open_scenario_dialog)
        self._ui.action_execute.triggered.connect(
            self._project_ctrl.run_optimization)
        # overview toolbar
        self._ui.tool_scenarios.clicked.connect(
            self._project_ctrl.open_scenario_dialog)
        self._ui.tool_run.clicked.connect(self._project_ctrl.run_optimization)
        self._ui.tool_export.clicked.connect(
            self._project_ctrl.open_export_dialog)
        self._ui.tool_sidebar_overview.clicked.connect(
            lambda: self._project_ctrl.toggle_sidebar(PageType.OVERVIEW))
        # overview content
        self._ui.logo.hovered.connect(self._project_ctrl.change_icon)
        self._ui.logo.clicked.connect(
            lambda: self._project_ctrl.change_page(PageType.SECTIONS))
        # sections toolbar
        self._ui.tool_back_sections.clicked.connect(
            lambda: self._project_ctrl.change_page(PageType.OVERVIEW))
        self._ui.tool_draft.clicked.connect(self.on_draft_mode)
        self._ui.tool_sidebar_sections.clicked.connect(
            lambda: self._project_ctrl.toggle_sidebar(PageType.SECTIONS))
        # sections content
        self._ui.section_view.sidebar_toggled.connect(self.show_section_sidebar)
        self._ui.section_view.commodity_clicked.connect(self._project_ctrl.set_current_commodity)

        # draft toolbar
        self._ui.tool_back_draft.clicked.connect(
            lambda: self._project_ctrl.change_page(PageType.SECTIONS))
        self._ui.tool_cursor.clicked.connect(
            lambda: self._project_ctrl.toggle_select_connect(
                SelectConnect.SELECT))
        self._ui.tool_connect.clicked.connect(
            lambda: self._project_ctrl.toggle_select_connect(
                SelectConnect.CONNECT))
        self._ui.tool_sidebar_draft.clicked.connect(
            lambda: self._project_ctrl.toggle_sidebar(PageType.DRAFT))
        # draft content

        # graph toolbar
        self._ui.tool_back_graph.clicked.connect(
            lambda: self._project_ctrl.change_page(PageType.SECTIONS))
        self._ui.tool_export_graph.clicked.connect(
            self._project_ctrl.open_export_dialog)
        self._ui.tool_cursor_graph.clicked.connect(
            lambda: self._project_ctrl.change_zoom_mode(ZoomType.SELECT))
        self._ui.tool_zoom_in.clicked.connect(
            lambda: self._project_ctrl.change_zoom_mode(ZoomType.ZOOM_IN))
        self._ui.tool_zoom_out.clicked.connect(
            lambda: self._project_ctrl.change_zoom_mode(ZoomType.ZOOM_OUT))
        self._ui.tool_zoom_range.clicked.connect(
            lambda: self._project_ctrl.change_zoom_mode(ZoomType.ZOOM_RANGE))
        # graph content

        """listen for model event signals"""
        # stacked pages
        self._model.current_page_changed.connect(
            self._ui.stacked_pages.setCurrentIndex)
        # overview page
        self._model.overview_selection_changed.connect(
            self.on_selection_change)
        self._model.overview_properties_changed.connect(
            self._ui.sidebar_overview.load_data)
        self._model.overview_sidebar_out_changed.connect(
            self._ui.sidebar_overview.toggle)

        # sections page
        self._model.current_section_changed.connect(
            self.on_section_change)
        self._model.sections_sidebar_out_changed.connect(
            self._ui.sidebar_sections.toggle)

        # draft page
        self._model.draft_select_mode_changed.connect(
            self.on_select_mode_change)
        self._model.draft_sidebar_out_changed.connect(
            self._ui.sidebar_draft.toggle)

        # graph page
        self._model.graph_zoom_mode_changed.connect(
            self.on_zoom_mode_change)
        self._model.current_commodity_changed.connect(
            self.on_commodity_change)

        """initialise view"""
        self._ui.logo.updateGeometry()
        self._ui.stacked_pages.setCurrentIndex(OverviewSelection.OVERVIEW.value)
        self._ui.scenario_select.set_model(self._model.scenarios)
        self._ui.sidebar_overview.load_data(self._model.overview_properties)
        self._section_scenes = List([
            SectionScene(OverviewSelection.ENERGY, self._model.project_elements,
                         self._model.commodities, self._model.process_cores),
            SectionScene(OverviewSelection.WATER, self._model.project_elements,
                         self._model.commodities, self._model.process_cores),
            SectionScene(OverviewSelection.FOOD, self._model.project_elements,
                         self._model.commodities, self._model.process_cores),
            SectionScene(OverviewSelection.BUSINESS, self._model.project_elements,
                         self._model.commodities, self._model.process_cores),
        ])
        self._ui.section_view.setScene(self._section_scenes[OverviewSelection.ENERGY.value])
        self._ui.draft_view.setScene(self._section_scenes[OverviewSelection.ENERGY.value])
        self._ui.draft_view.draft_mode = True

    def on_selection_change(self, selection):
        self._ui.logo.change_icon(OverviewSelection(selection))
        self._ui.title_overview.setText(str(OverviewSelection(selection)))

    def on_section_change(self, section):
        section = OverviewSelection(section)
        # prepare section page
        self._ui.title_sections.setText(section.name.title())
        self._ui.section_view.setScene(self._section_scenes[section.value - 1])
        # prepare draft page
        self._ui.title_draft.setText(section.name.title() + " - Draft")
        self._ui.draft_view.setScene(self._section_scenes[section.value - 1])

    def on_select_mode_change(self, select_type):
        # change view of toolbar buttons
        self._ui.tool_cursor.setChecked(False)
        self._ui.tool_connect.setChecked(False)
        if SelectConnect(select_type) is SelectConnect.SELECT:
            self._ui.tool_cursor.setChecked()
        else:
            self._ui.tool_connect.setChecked()

        # set mode in section scene
        self._ui.draft_view.scene().edit_mode = SelectConnect(select_type)
        if select_type == SelectConnect.SELECT.value:
            self._ui.draftbar.toggle(True)
        else:
            self._ui.draftbar.toggle(False)

    def on_zoom_mode_change(self, zoom_value):
        self._ui.tool_cursor_graph.setChecked(False)
        self._ui.tool_zoom_in.setChecked(False)
        self._ui.tool_zoom_out.setChecked(False)
        self._ui.tool_zoom_range.setChecked(False)

        zoom_type = ZoomType(zoom_value)
        if zoom_type is ZoomType.SELECT:
            self._ui.tool_cursor_graph.setChecked()
        elif zoom_type is ZoomType.ZOOM_IN:
            self._ui.tool_zoom_in.setChecked()
        elif zoom_type is ZoomType.ZOOM_OUT:
            self._ui.tool_zoom_out.setChecked()
        else:
            self._ui.tool_zoom_range.setChecked()

        self._ui.commodity_flow_view.set_zoom_mode(zoom_type)

    def on_draft_mode(self):
        """draft tool button clicked"""
        section_cores = list(filter(lambda core: core.section == self._model.current_section,
                                    self._model.process_cores))
        cores = List([list(filter(lambda core: core.category == ProcessCategory.SUPPLY, section_cores)),
                      list(filter(lambda core: core.category == ProcessCategory.PROCESS, section_cores)),
                      list(filter(lambda core: core.category == ProcessCategory.STORAGE, section_cores)),
                      list(filter(lambda core: core.category == ProcessCategory.DEMAND, section_cores))])
        self._ui.draftbar.load_data(cores, PageType.DRAFT)
        self._project_ctrl.change_page(PageType.DRAFT)

    def on_commodity_change(self, commodity_type):
        """commodity line in scene selected"""
        if commodity_type is not None:
            self._ui.title_graph.setText(str(commodity_type))
            commodities = list(filter(lambda commodity: commodity.commodity_type is commodity_type,
                                      self._model.project_elements.commodity_list))
            commodity_model = PropertyPopupMenu("Commodities", List(commodities))
            commodity_model.value_changed.connect(lambda: self.on_commodity_choose(commodity_model.value))
            self._ui.commodity_select.set_model(commodity_model)
            self.on_commodity_choose(commodity_model.value)

            self._project_ctrl.change_page(PageType.GRAPH)

    def on_commodity_choose(self, commodity):
        """commodity in dropdown menu of commodity page selected"""
        self._ui.commodity_flow_view.set_data(commodity.optimization_output)

    def show_section_sidebar(self, process):
        if process:
            self._project_ctrl.toggle_sidebar(PageType.SECTIONS, True)

            properties = []
            properties.extend(process.properties.list)
            # extend shown property list with optimization variables that have single values
            if process.optimization_output:
                single_variables = list(filter(lambda var: (var.resolution is DatasetResolution.YEARLY) &
                                                           (var.display is DisplayType.YES),
                                               process.core.variables))
                for variable in single_variables:
                    # display 3 significant figures
                    display_value = str(float('%.3g' % process.optimization_output[variable.name][0]))
                    optimization_variable = PropertyLineEdit(variable.name, display_value, variable.unit)
                    optimization_variable.read_only = True
                    properties.append(optimization_variable)

            self._ui.sidebar_sections.load_data(properties, PageType.SECTIONS)
        else:
            self._project_ctrl.toggle_sidebar(PageType.SECTIONS, False)

    def closeEvent(self, event):
        self._model.save()
