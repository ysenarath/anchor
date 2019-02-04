import ctypes
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cefpython3 import cefpython as cef

from anchor.app.handlers import FocusHandler


class CefBrowserView(QWidget):
    def __init__(self, app, url=None, parent=None, load_handler=None):
        # noinspection PyArgumentList
        super(CefBrowserView, self).__init__(parent)
        self.app = app
        self.parent = parent
        self.browser = None
        self.hidden_window = None
        self.load_handler = load_handler
        self.url = url if url else self.app.configs['home-page'] if self.load_handler else \
            self.app.configs['sidebar'][0]['url']
        self.focus_handler = FocusHandler(self.app, self)
        self.show()

    def focusInEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        if self.browser:
            if self.app.platform == 'WINDOWS':
                self.app.window_utils_.OnSetFocus(self.getHandle(), 0, 0, 0)
            self.browser.SetFocus(True)

    def focusOutEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        if self.browser:
            self.browser.SetFocus(False)

    def embedBrowser(self):
        if self.app.platform == 'LINUX':
            # noinspection PyUnresolvedReferences
            self.hidden_window = QWindow()
        window_info = cef.WindowInfo()
        rect = [0, 0, self.width(), self.height()]
        window_info.SetAsChild(self.getHandle(), rect)
        self.browser = cef.CreateBrowserSync(window_info, url=self.url)
        self.browser.SetClientHandler(self.load_handler)
        self.browser.SetClientHandler(self.focus_handler)

    # noinspection SpellCheckingInspection,PyBroadException,PyPep8
    def getHandle(self):
        if self.hidden_window:
            # PyQt5 on Linux
            return int(self.hidden_window.winId())
        try:
            # PyQt5
            return int(self.winId())
        except:
            # PySide:
            # | QWidget.winId() returns <PyCObject object at 0x02FD8788>
            # | Converting it to int using ctypes.
            if sys.version_info[0] == 2:
                # Python 2
                ctypes.pythonapi.PyCObject_AsVoidPtr.restype = (
                    ctypes.c_void_p
                )
                ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = ([ctypes.py_object])
                return ctypes.pythonapi.PyCObject_AsVoidPtr(self.winId())
            else:
                # Python 3
                ctypes.pythonapi.PyCapsule_GetPointer.restype = (
                    ctypes.c_void_p)
                ctypes.pythonapi.PyCapsule_GetPointer.argtypes = (
                    [ctypes.py_object])
                return ctypes.pythonapi.PyCapsule_GetPointer(self.winId(), None)

    # noinspection PyAttributeOutsideInit
    def moveEvent(self, _):
        self.x = 0
        self.y = 0
        if self.browser:
            if self.app.platform == 'WINDOWS':
                self.app.window_utils_.OnSize(self.getHandle(), 0, 0, 0)
            elif self.app.platform == 'LINUX':
                self.browser.SetBounds(self.x, self.y, self.width(), self.height())
            self.browser.NotifyMoveOrResizeStarted()

    def resizeEvent(self, event):
        size = event.size()
        if self.app.platform == 'WINDOWS':
            self.app.window_utils_.OnSize(self.getHandle(), 0, 0, 0)
        elif self.app.platform == 'LINUX':
            if self.browser:
                self.browser.SetBounds(self.x, self.y, size.width(), size.height())
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()
