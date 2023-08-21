import pytest
from qtpy import PYSIDE2, PYSIDE6, PYQT5, PYQT6


def test_qtremoteobjects():
    """Test the qtpy.QtRemoteObjects namespace"""
    QtRemoteObjects = pytest.importorskip("qtpy.QtRemoteObjects")

    assert QtRemoteObjects.QRemoteObjectAbstractPersistedStore is not None
    assert QtRemoteObjects.QRemoteObjectDynamicReplica is not None
    assert QtRemoteObjects.QRemoteObjectHost is not None
    assert QtRemoteObjects.QRemoteObjectHostBase is not None
    assert QtRemoteObjects.QRemoteObjectNode is not None
