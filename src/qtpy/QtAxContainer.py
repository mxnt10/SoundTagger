# -----------------------------------------------------------------------------
# Copyright © 2009- The Spyder Development Team
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------

"""Provides QtAxContainer classes and functions."""

from . import (
    PYQT5,
    PYQT6,
    PYSIDE2,
    PYSIDE6,
    QtBindingMissingModuleError,
)

if PYQT5:
    raise QtBindingMissingModuleError(name='QtAxContainer')
elif PYQT6:
    raise QtBindingMissingModuleError(name='QtAxContainer')
elif PYSIDE2:
    from PySide2.QtAxContainer import *
elif PYSIDE6:
    from PySide6.QtAxContainer import *
