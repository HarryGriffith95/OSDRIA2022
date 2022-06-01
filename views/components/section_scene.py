from PySide2.QtCore import QSize, QPoint, QPointF, QLineF, QRect, QRectF, Qt, QMargins
from PySide2.QtGui import QPen, QBrush, QColor, QTransform, QCursor
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItemGroup, QGraphicsItem, QMenu, QAction, QMessageBox

from models.constants import MimeType, SelectConnect, OverviewSelection, ProcessCategory
from models.element import Process
from models.data_structure import List

GRID_WIDTH = 100
GRID_HEIGHT = 100
MIN_GRID_MARGIN = 10
COMMODITY_LINE_WIDTH = 22
DROP_INDICATOR_SIZE = 5
ARROW_SIZE = 10

PROCESS_SIZE = 80


class SectionScene(QGraphicsScene):
    def __init__(self, section, model, commodity_types, process_cores):
        super().__init__()
        self._grid_size = QSize(GRID_WIDTH, GRID_HEIGHT)
        self._drop_indicator = self.init_drop_indicator()
        self._process_items = QGraphicsItemGroup()
        self._commodity_items = List([])
        self._bounding_rect = BoundingRect(section, model.process_list, commodity_types)
        self._clicked_item = None
        self._item_mouse_offset = None
        self._connect_line = None
        self._items_border = QRect()
        self._grid_border = QRect()
        self._section = section
        self._model = model
        self._cores = process_cores

        self._edit_mode = SelectConnect.SELECT
        self._draft_mode = False

        self.init_scene()

    @property
    def edit_mode(self):
        return self._edit_mode

    @edit_mode.setter
    def edit_mode(self, value):
        if value in SelectConnect:
            self._edit_mode = value
            if value == SelectConnect.SELECT:
                self._process_items.setFlag(QGraphicsItem.ItemIsMovable)
            else:
                self._process_items.setFlag(QGraphicsItem.ItemIsMovable, False)
        else:
            raise TypeError

    @property
    def draft_mode(self):
        return self._draft_mode

    @draft_mode.setter
    def draft_mode(self, value):
        if value in [True, False]:
            self._draft_mode = value
            self._process_items.setFlag(QGraphicsItem.ItemIsMovable, value)
        else:
            raise TypeError

    def init_scene(self):
        """initialize content of scene based on list of elements"""
        for process in self._model.process_list:
            if process.core.section == self._section:
                process_item = self.draw_process(process)
                self.draw_connection(process_item)
                self.draw_connection(process_item, False)
        self.update_commodities()

    def draw_commodity(self, commodity):
        """create commodity item"""
        commodity_item = CommodityItem(commodity.locations[self._section], self._bounding_rect)
        commodity_item.setData(0, commodity)
        commodity_item.setData(1, 0)
        self.addItem(commodity_item)

        return commodity_item

    def draw_connection(self, process_item, input_com=True):
        commodity_types = []
        process = process_item.data(0)
        connections = process_item.data(1)

        # define necessary connections to commodity item
        commodities = process.inputs if input_com else process.outputs
        for commodity in commodities:
            if commodity.commodity_type not in commodity_types:
                commodity_types.append(commodity.commodity_type)

        commodity_difference = PROCESS_SIZE / (len(commodity_types) + 1)
        for commodity_type in commodity_types:
            commodity_position = commodity_type.locations[self._section]
            item_position = process.coordinate.x() + PROCESS_SIZE / 2
            # set item_position to left/right border of process depending on commodity_position
            if commodity_position < item_position:
                item_position -= PROCESS_SIZE

            start_position = commodity_position if input_com else item_position
            end_position = item_position if input_com else commodity_position

            commodity_item = [item for item in self._commodity_items if item.data(0) is commodity_type]
            connection_item = [connection for connection in connections if connection.data(1) is commodity_item]

            if commodity_item:
                commodity_item = commodity_item[0]
            else:
                # create new commodity item
                commodity_item = self.draw_commodity(commodity_type)
                self._commodity_items.add(commodity_item)

            if connection_item:
                connection_item = connection_item[0]
            else:
                # ignore second double arrow for storage processes if start_position is left of end_position
                if (process.core.category is ProcessCategory.STORAGE) & (end_position - start_position < 0):
                    return

                # create new connection item
                connection_item = ConnectionItem(end_position - start_position,
                                                 process.core.category is ProcessCategory.STORAGE)
                commodity_item.setData(1, commodity_item.data(1) + 1)
                connection_item.setData(1, commodity_item)
                connection_list = process_item.data(1)
                connection_list.append(connection_item)
                process_item.setData(1, connection_list)

            connection_item.setX(start_position)
            index = commodity_types.index(commodity_type) + 1
            connection_item.setY(process.coordinate.y() - PROCESS_SIZE / 2 + commodity_difference * index)
            self.addItem(connection_item)

    def draw_process(self, process):
        """create process item and add to scene & process items list"""
        process_item = ProcessItem(process.core.icon)
        process_item.setData(0, process)
        process_item.setData(1, [])
        process_item.setPos(process.coordinate)
        process_item.setFlag(QGraphicsItem.ItemIsMovable)

        self._process_items.prepareGeometryChange()
        self._process_items.addToGroup(process_item)
        self.addItem(process_item)

        return process_item

    def delete_process(self, item):
        process = item.data(0)
        self._model.process_list.remove(process)

        # remove all connection items and the commodity item if applicable
        for connection_item in item.data(1):
            commodity_item = connection_item.data(1)
            commodity_references = commodity_item.data(1) - 1
            commodity_item.setData(1, commodity_references)
            if commodity_references == 0:
                # remove commodity of section count and commodity item
                commodity_item.data(0).locations.remove(self._section)
                self._commodity_items.remove(commodity_item)
                self.removeItem(commodity_item)
            self.removeItem(connection_item)

        # reduce connection count of all commodities connected to process
        for input_com in process.inputs:
            input_com.connection_count[self._section] -= 1
            if input_com.connection_count[self._section] == 0:
                input_com.connection_count.remove(self._section)
                if not input_com.connection_count:
                    self._model.commodity_list.remove(input_com)

        for output in process.outputs:
            output.connection_count[self._section] -= 1
            if output.connection_count[self._section] == 0:
                output.connection_count.remove(self._section)
                if not output.connection_count:
                    self._model.commodity_list.remove(output)

        self._process_items.removeFromGroup(item)
        self.removeItem(item)

        self.update_commodities()

    def init_drop_indicator(self):
        rect = QRect(-DROP_INDICATOR_SIZE/2, -DROP_INDICATOR_SIZE/2, DROP_INDICATOR_SIZE, DROP_INDICATOR_SIZE)
        brush = QBrush(Qt.darkBlue)
        pen = QPen(Qt.darkBlue, 1)
        ellipse = self.addEllipse(rect, pen, brush)
        ellipse.setVisible(False)
        return ellipse

    def disable_drop_indicator(self):
        self._drop_indicator.setX(-DROP_INDICATOR_SIZE / 2)
        self._drop_indicator.setY(-DROP_INDICATOR_SIZE / 2)
        self._drop_indicator.setVisible(False)
        self.update()

    def align_drop_indicator(self, point):
        """align the drop indicator to grid while mouse movement"""
        # move drop indicator only within grid boundaries
        if not self.get_grid_border(-MIN_GRID_MARGIN).contains(point.toPoint()):
            self._drop_indicator.setVisible(False)
            return

        # calculate the nearby position of grid interceptions
        grid_x = (round(point.x() / self._grid_size.width() / 2 - 1/2) * 2 + 1) * self._grid_size.width()
        grid_y = round(point.y() / self._grid_size.height()) * self._grid_size.height()

        # move drop indicator to grid interception
        self._drop_indicator.setX(grid_x)
        self._drop_indicator.setY(grid_y)
        self._drop_indicator.setVisible(True)
        self.update()

    def get_grid_border(self, margin=0):
        def get_raster_length(length, raster):
            return (int((length + MIN_GRID_MARGIN + raster/2) / raster) - 1/2) * raster

        left = get_raster_length(self.sceneRect().left(), self._grid_size.width())
        right = get_raster_length(self.sceneRect().right(), self._grid_size.width())
        top = get_raster_length(self.sceneRect().top(), self._grid_size.height())
        bottom = get_raster_length(self.sceneRect().bottom(), self._grid_size.height())

        return QRect(left, top, right-left, bottom-top).marginsAdded(QMargins(margin, margin, margin, margin))

    def execute_connection(self, item, position):
        if not self._connect_line:
            if self.show_connection_menu(item, position):
                return
        else:
            selected_commodity = self._connect_line.data(1)
            if isinstance(item, ProcessItem):
                # create incoming connection
                if selected_commodity in item.data(0).core.inputs:
                    if self._connect_line.data(0) is None:
                        # establish connection from commodity
                        if selected_commodity not in item.data(0).inputs:
                            self.connect_process(item.data(0), selected_commodity, False)
                            self.draw_connection(item)
                    else:
                        # establish connection between processes
                        self.connect_processes(selected_commodity, self._connect_line.data(0), item)
            elif item is None:
                # create outgoing connection
                menu = QMenu()
                menu.addAction("> Commodity")

                if menu.exec_(QCursor.pos()):
                    self.connect_process(self._connect_line.data(0).data(0), selected_commodity)
                    self.draw_connection(self._connect_line.data(0), False)

        # end connection
        self.views()[1].setMouseTracking(False)
        self.removeItem(self._connect_line)
        self._connect_line = None

    def show_connection_menu(self, item, position):
        menu = QMenu()
        # add all output commodities of process to menu
        for commodity in item.data(0).core.outputs:
            action = menu.addAction(str(commodity))
            action.setData(commodity)

        # execute menu
        action = menu.exec_(QCursor.pos())
        if action:
            # start connection
            line_pen = QPen(Qt.lightGray, 1, Qt.DashLine)
            line = QLineF(position, position)
            self._connect_line = self.addLine(line, line_pen)
            self._connect_line.setData(0, item)
            self._connect_line.setData(1, action.data())
            self.views()[1].setMouseTracking(True)
            return True

        return False

    def connect_processes(self, selected_commodity, start_process_item, end_process_item):
        # establish connection
        connect_commodity = None
        commodity_in_input = False
        commodity_in_output = False
        start_process = start_process_item.data(0)
        end_process = end_process_item.data(0)

        # check if selected_commodity is in outputs or inputs of related processes
        outputs = start_process.outputs
        if selected_commodity in outputs:
            commodity_in_output = True
            connect_commodity = outputs[outputs.index(selected_commodity)]

        inputs = end_process.inputs
        if selected_commodity in inputs:
            commodity_in_input = True
            connect_commodity = inputs[inputs.index(selected_commodity)]

        # determine necessary connection steps
        if commodity_in_input & commodity_in_output:
            # selected_commodity already exists in input and output -> connection exists
            QMessageBox.warning(self.views()[1], "Connection exists", "Connection already established", QMessageBox.Ok)
            return
        elif commodity_in_input:
            # add commodity to output of start process
            self.connect_process(start_process, connect_commodity)
            self.draw_connection(start_process_item, False)
        elif commodity_in_output:
            # add commodity to input of end process
            self.connect_process(end_process, connect_commodity, False)
            self.draw_connection(end_process_item)
        else:
            # establish new commodity in both processes
            connect_commodity = selected_commodity.copy()

            self.connect_process(start_process, connect_commodity)
            self.connect_process(end_process, connect_commodity, False)
            self.draw_connection(start_process_item, False)
            self.draw_connection(end_process_item)

    def connect_process(self, process, commodity, output=True):
        if self._section not in commodity.connection_count.keys():
            commodity.connection_count[self._section] = 0
        if commodity not in self._model.commodity_list:
            self._model.commodity_list.add(commodity)
        commodity.connection_count[self._section] += 1

        commodity_list = process.outputs if output else process.inputs
        commodity_list.add(commodity)
        # add commodity in input and output list
        if process.core.category is ProcessCategory.STORAGE:
            commodity_list = process.outputs if not output else process.inputs
            commodity_list.add(commodity)

        self.set_commodity_position(commodity.commodity_type, process, output)

    def set_commodity_position(self, commodity_type, process, right=True):
        """changes the commodity position according to newly connected process"""
        if self._section not in commodity_type.locations.keys():
            # set initial position to right of process
            location = process.coordinate.x() + self._grid_size.width() * (1 if right else -1)
            commodity_type.locations[self._section] = location
        else:
            # todo change position based on newly connected process
            pass

    def update_commodities(self):
        """update length of commodity line based on bounding rect"""
        self._bounding_rect.update()
        top_border = self._bounding_rect.top()
        height_border = self._bounding_rect.height()
        for commodity_item in self._commodity_items:
            commodity_item.update_line(top_border, height_border)

    def drawBackground(self, painter, rect):
        if self.draft_mode:
            border_rect = self.get_grid_border()
            grid_rect = self.get_grid_border(-self._grid_size.width()/2)

            line_list = []
            # horizontal grid lines
            for line_coordinate in range(grid_rect.top(), border_rect.bottom(), self._grid_size.height()):
                line_list.append(QLineF(border_rect.left(), line_coordinate,
                                        border_rect.right(), line_coordinate))
            # vertical process lines
            left_border = int((grid_rect.left() + self._grid_size.width()) / (2 * self._grid_size.width())) * \
                self._grid_size.width() * 2 - self._grid_size.width()
            for line_coordinate in range(left_border, border_rect.right(), self._grid_size.width()*2):
                line_list.append(QLineF(line_coordinate, border_rect.top(),
                                        line_coordinate, border_rect.bottom()))

            # vertical commodity lines
            left_border = int(grid_rect.left() / (2 * self._grid_size.width())) * self._grid_size.width() * 2
            for line_coordinate in range(left_border, border_rect.right(), self._grid_size.width() * 2):
                line_list.append(QLineF(line_coordinate - 1, border_rect.top(),
                                        line_coordinate - 1, border_rect.bottom()))
                line_list.append(QLineF(line_coordinate + 1, border_rect.top(),
                                        line_coordinate + 1, border_rect.bottom()))

            painter.setPen(QPen(Qt.lightGray, 1))
            painter.drawLines(line_list)

        super().drawBackground(painter, rect)

    def mousePressEvent(self, event):
        # ignore right button click
        if event.button() == Qt.RightButton:
            return

        self._clicked_item = self.itemAt(event.scenePos(), QTransform())
        if self.draft_mode & (self.edit_mode == SelectConnect.SELECT):
            if isinstance(self._clicked_item, ProcessItem):
                self._clicked_item.setOpacity(0.5)
                self._drop_indicator.setPos(self._clicked_item.pos())
                self._drop_indicator.setVisible(True)
                # set offset between mouse and center of item for mouseMoveEvent
                self._item_mouse_offset = self._clicked_item.mapFromScene(event.scenePos())
            else:
                self._clicked_item = None

    def mouseMoveEvent(self, event):
        if self.draft_mode:
            if self.edit_mode == SelectConnect.SELECT:
                if self._clicked_item:
                    # move drop indicator along grid and process item according to mouse position
                    self.align_drop_indicator(event.scenePos() - self._item_mouse_offset)
                    self._clicked_item.setPos(event.scenePos() - self._item_mouse_offset)
            elif self._connect_line:
                # update connect line in CONNECT mode
                line = self._connect_line.line()
                # add offset to position to avoid itemAt function to return lineItem
                line.setP2(event.scenePos() - QPoint(2, 2))
                self._connect_line.setLine(line)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # normal mode
        if not self.draft_mode:
            if event.button() == Qt.LeftButton:
                # toggle sidebar with properties
                clicked_item = self.itemAt(event.scenePos(), QTransform())
                if self._clicked_item:
                    if isinstance(clicked_item, ProcessItem):
                        self.views()[0].sidebar_toggled.emit(clicked_item.data(0))
                        self.views()[0].commodity_clicked.emit(None)
                    elif isinstance(clicked_item, CommodityItem):
                        self.views()[0].sidebar_toggled.emit(None)
                        self.views()[0].commodity_clicked.emit(clicked_item.data(0))
                    else:
                        self.views()[0].sidebar_toggled.emit(None)
                        self.views()[0].commodity_clicked.emit(None)
                else:
                    self.views()[0].sidebar_toggled.emit(None)
                    self.views()[0].commodity_clicked.emit(None)
            return

        # draft mode in selection
        if self.edit_mode == SelectConnect.SELECT:
            # release process item
            if self._clicked_item:
                self._clicked_item.setOpacity(1.0)
                # remove clicked item from collision list with drop indicator
                collision_items = self.collidingItems(self._drop_indicator)
                if collision_items:
                    collision_items.remove(self._clicked_item)
                # avoid placement if colliding with other items
                if not collision_items:
                    self._clicked_item.setPos(self._drop_indicator.scenePos())
                    self._clicked_item.data(0).coordinate = self._drop_indicator.pos()
                    self._bounding_rect.update()
                self.disable_drop_indicator()
                self._clicked_item = None
        else:
            # connecting processes
            if event.button() == Qt.LeftButton:
                clicked_item = self.itemAt(event.scenePos(), QTransform())
                self.execute_connection(clicked_item, event.scenePos())

        super().mouseReleaseEvent(event)

    def dragEnterEvent(self, event):
        pass

    def dragLeaveEvent(self, event):
        self.disable_drop_indicator()

    def dragMoveEvent(self, event):
        if self.draft_mode & (self.edit_mode == SelectConnect.SELECT):
            self.align_drop_indicator(event.scenePos())

    def dropEvent(self, event):
        """add new process to list and process item to scene"""
        # prevent process placement if item exists there
        if len(self.collidingItems(self._drop_indicator)) > 0:
            return

        core_name = event.mimeData().data(MimeType.PROCESS_CORE.value).data().decode('UTF-8')
        process_core = list(filter(lambda element: element.name == core_name, self._cores))[0]

        # define name based on process core and existing names
        remainder_name = [process.name.split(process_core.name)[1].strip()
                          for process in self._model.process_list if process_core.name in process.name]
        if not remainder_name:
            process_name = process_core.name
        elif max(remainder_name).isdigit():
            process_name = process_core.name + " " + str(int(max(remainder_name)) + 1)
        else:
            process_name = process_core.name + " 1"

        # create new process based on process core and add to element list
        process = Process(process_name, self._drop_indicator.pos(), process_core)
        self._model.add_process(process)

        # create process item and connections
        self.draw_process(process)
        self.update_commodities()

        self.disable_drop_indicator()

    def contextMenuEvent(self, event):
        """context menu to interact with process items - delete item"""
        # prevent context menu of scene not in draft mode
        if not self.draft_mode:
            return

        if self._edit_mode == SelectConnect.SELECT:
            # open context menu only for process items
            self._clicked_item = self.itemAt(event.scenePos(), QTransform())
            if self._clicked_item:
                if isinstance(self._clicked_item, ProcessItem):
                    menu = QMenu()
                    delete_action = QAction("Delete", None)
                    delete_action.triggered.connect(
                        lambda: self.delete_process(self._clicked_item))
                    menu.addAction(delete_action)
                    menu.exec_(event.screenPos())
                    self._clicked_item = None
        else:
            # open context menu for commodities of other sections
            menu = QMenu()
            section_list = [item for item in OverviewSelection
                            if item is not self._section and item is not OverviewSelection.OVERVIEW]
            for section in section_list:
                submenu = QMenu(section.name)
                section_coms = [commodity for commodity in self._model.commodity_list
                                if section in commodity.connection_count.keys()]
                for commodity in section_coms:
                    action = submenu.addAction(str(commodity))
                    action.setData(commodity)

                # only add sub menu if commodities are available
                if section_coms:
                    menu.addMenu(submenu)

            # execute menu
            action = menu.exec_(QCursor.pos())
            if action:
                # start connection
                line_pen = QPen(Qt.lightGray, 1, Qt.DashLine)
                line = QLineF(event.scenePos(), event.scenePos())
                self._connect_line = self.addLine(line, line_pen)
                self._connect_line.setData(0, None)
                self._connect_line.setData(1, action.data())
                self.views()[1].setMouseTracking(True)

    def setSceneRect(self, rect):
        """set sceneRect to view boundaries if necessary space is less"""
        super().setSceneRect(self._bounding_rect.scene_rect(rect, 2*MIN_GRID_MARGIN))


class BoundingRect(QRect):
    """bounding rectangle including processes and commodities"""
    def __init__(self, section, process_list, commodity_list):
        super().__init__(0, 0, 0, 0)
        self._section = section
        self._processes = process_list
        self._commodities = commodity_list

    def update(self):
        # todo extend/reduce sceneRect with position of elements
        processes = [process for process in self._processes if process.core.section is self._section]
        # set rect to initial value if no items exist
        if not processes:
            self.setRect(0, 0, 0, 0)
            return

        process_x_coordinates = [process.coordinate.x() for process in processes]
        process_y_coordinates = [process.coordinate.y() for process in processes]
        commodity_x_coordinates = [commodity.locations[self._section] for commodity in self._commodities
                                   if self._section in commodity.locations.keys()]
        commodity_x_coordinates.extend([min(process_x_coordinates) - PROCESS_SIZE/2,
                                        max(process_x_coordinates) + PROCESS_SIZE/2])
        left_bound = min(commodity_x_coordinates)
        right_bound = max(commodity_x_coordinates)
        top_bound = min(process_y_coordinates) - PROCESS_SIZE/2
        bottom_bound = max(process_y_coordinates) + PROCESS_SIZE/2

        self.setRect(left_bound, top_bound, right_bound-left_bound, bottom_bound-top_bound)

    def scene_rect(self, other, margin):
        """define scene rectangle based on bounding rectangle with margin and other rectangle"""
        if not isinstance(other, QRect):
            raise TypeError

        scene_rect = self.marginsAdded(QMargins(margin, margin, margin, margin))
        # bounding rectangle of items within other rectangle
        if scene_rect.width() < other.width():
            # left border of items is within left border of other rectangle
            if other.left() < scene_rect.left():
                width_difference = other.width() - scene_rect.width()
                scene_rect.moveLeft(scene_rect.left() - width_difference/2)
            scene_rect.setWidth(other.width())
        if scene_rect.height() < other.height():
            if other.top() < scene_rect.top():
                height_difference = other.height() - scene_rect.height()
                scene_rect.moveTop(scene_rect.top() - height_difference/2)
            scene_rect.setHeight(other.height())

        return scene_rect


# todo create QGraphicsItem class for process
class ProcessItem(QGraphicsItem):
    """create rounded rectangle with icon"""

    def __init__(self, icon):
        super().__init__()
        self._icon = icon

    def boundingRect(self):
        return QRect(-PROCESS_SIZE/2, -PROCESS_SIZE/2, PROCESS_SIZE, PROCESS_SIZE)

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor(0, 90, 158)))
        painter.setPen(QPen(QColor(0, 90, 158)))
        painter.drawRoundedRect(self.boundingRect(), 10, 10)
        painter.setBrush(QBrush())
        icon_rect = QRect(option.rect.top()/2, option.rect.left()/2, option.rect.width()/2, option.rect.height()/2)
        painter.drawPixmap(icon_rect, self._icon.pixmap(option.rect.size()/2))


# todo create QGraphicsItem class for commodity
class CommodityItem(QGraphicsItem):
    """create vertical commodity line"""

    def __init__(self, x_position, rect):
        super().__init__()
        self.setAcceptHoverEvents(True)
        self._x = x_position
        self._top = rect.top()
        self._height = rect.height()
        self.setPos(self._x, self._top)

    def boundingRect(self):
        return QRectF(-COMMODITY_LINE_WIDTH/2, 0, COMMODITY_LINE_WIDTH, self._height)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(0, 0, 0, self._height)

    def update_line(self, top, height):
        old_bounding_rect = self.boundingRect()
        self._top = top
        self._height = height
        self.update(old_bounding_rect)
        self.setPos(self._x, self._top)

    def hoverEnterEvent(self, event):
        event.widget().setCursor(Qt.PointingHandCursor)

    def hoverLeaveEvent(self, event):
        event.widget().unsetCursor()


# todo create connection item
class ConnectionItem(QGraphicsItem):
    """create horizontal connection arrows"""

    def __init__(self, length, double_arrow=False):
        super().__init__()
        self._length = abs(length)

        if length < 0:
            self.setRotation(180)

        right_arrow = [QPointF(self._length - ARROW_SIZE, 0),
                       QPointF(self._length - ARROW_SIZE, -ARROW_SIZE / 2),
                       QPointF(self._length, 0),
                       QPointF(self._length - ARROW_SIZE, ARROW_SIZE / 2),
                       QPointF(self._length - ARROW_SIZE, 0)]

        left_arrow = [QPointF(ARROW_SIZE, 0),
                      QPointF(ARROW_SIZE, -ARROW_SIZE / 2),
                      QPointF(0, 0),
                      QPointF(ARROW_SIZE, ARROW_SIZE / 2),
                      QPointF(ARROW_SIZE, 0)]

        if double_arrow:
            self._points = left_arrow + right_arrow
        else:
            self._points = [QPointF(0, 0)] + right_arrow

    def boundingRect(self):
        return QRect(0, -ARROW_SIZE/2, self._length, ARROW_SIZE/2)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(Qt.black))
        painter.drawPolygon(self._points)
