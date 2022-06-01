from enum import Enum


class ProcessCategory(Enum):
    """"process categories:
    - Supply
    - Process
    - Storage
    - Demand"""
    SUPPLY = 0
    PROCESS = 1
    STORAGE = 2
    DEMAND = 3

    def __str__(self):
        """return name as lowercase with first letter uppercase"""
        return self.name.title()


class OverviewSelection(Enum):
    """enumeration of the overview selector
    OVERVIEW
    ENERGY
    WATER
    FOOD
    BUSINESS"""
    OVERVIEW = 0
    ENERGY = 1
    WATER = 2
    FOOD = 3
    BUSINESS = 4

    def __str__(self):
        """return name as lowercase with first letter uppercase"""
        return self.name.title()


class PageType(Enum):
    """enumeration of the stacked page type
    OVERVIEW
    SECTIONS
    DRAFT
    GRAPH"""
    OVERVIEW = 0
    SECTIONS = 1
    DRAFT = 2
    GRAPH = 3


class SelectConnect(Enum):
    """enumeration of the select or connect in draft mode
    SELECT
    CONNECT"""
    SELECT = 0
    CONNECT = 1


class ZoomType(Enum):
    """enumeration zoom types in graph mode
    SELECT
    ZOOM_IN
    ZOOM_OUT
    ZOOM_RANGE"""
    SELECT = 0
    ZOOM_IN = 1
    ZOOM_OUT = 2
    ZOOM_RANGE = 3


class PropType(Enum):
    """define property types
    LINE_EDIT
    DIALOG
    CONTEXT_MENU"""
    LINE_EDIT = 0
    DIALOG = 1
    POPUP_MENU = 2


class MimeType(Enum):
    """define MimeTypes
    PROCESS_CORE"""
    PROCESS_CORE = "application/x-process_core"


class DatasetResolution(Enum):
    """define different resolutions for datasets
    numbers represent the respective amount within a year
    HOURLY
    DAILY
    WEEKLY
    MONTHLY"""
    HOURLY = 8760
    DAILY = 365
    WEEKLY = 52
    MONTHLY = 12
    YEARLY = 1

    def __str__(self):
        """return name as lowercase with first letter uppercase"""
        return self.name.title()

class PyomoVarType(Enum):
    """define different type of pyomo variables
    all in pyomo book at page 51
    REALS
    POSITIVE_REALS
    NON_NEGATIVE_REALS
    INTEGERS
    POSITIVE_INTEGERS
    NON_NEGATIVE_INTEGERS
    BOOLEAN"""
    NON_NEGATIVE_REALS = "NonNegativeReals"
    NON_NEGATIVE_INTEGERS = "NonNegativeIntegers"
    BOOLEAN = "Boolean"
    NON_PYOMO = "NonPyomo"
    REALS = "Reals"
    POSITIVE_REALS = "PositiveReals"
    INTEGERS = "Integers"
    POSITIVE_INTEGERS = "PositiveIntegers"
    HOURLY = "Index Hourly"
    DAILY = "Index Daily"
    WEEKLY = "Index Weekly"
    MONTHLY = "Index Monthly"

    def __str__(self):
        return self.value


class DisplayType(Enum):
    """define displaying of output"""
    YES = 0
    NO = 1

    def __str__(self):
        """return name as lowercase with first letter uppercase"""
        return self.name.title()
