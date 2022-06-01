__version__ = "5.12.2"
__version_info__ = (5, 12, 2, "", "")

# PYSIDE-932: Python 2 cannot import 'zipfile' for embedding while being imported, itself.
# We simply pre-load all imports for the signature extension.
import sys, zipfile, base64, marshal, io

from .shiboken2 import *

# Trigger signature initialization.
type.__signature__
