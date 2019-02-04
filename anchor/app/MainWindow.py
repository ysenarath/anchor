from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from anchor.app.handlers import LoadHandler
from anchor.app.utils.styles import MAIN_WINDOW_STYLE
from anchor.app.widgets import CefBrowserView, NavigationBar
from anchor.app.widgets.SideBar import SideBar


class MainWindow(QMainWindow):
    def __init__(self, app):
        # noinspection PyArgumentList
        super(MainWindow, self).__init__(None)
        self.app = app
        self.browser_view = None
        self.sidebar_view = None
        self.navigation_bar = None
        self.side_bar = None
        self.setWindowTitle(self.app.configs['title'])
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        self.setupLayout()

    def setupLayout(self):
        self.resize(self.app.configs['width'], self.app.configs['height'])
        load_handler = LoadHandler(self.app, self)
        self.browser_view = CefBrowserView(self.app, parent=self, load_handler=load_handler)
        self.sidebar_view = CefBrowserView(self.app, parent=self)
        self.navigation_bar = NavigationBar(self.app, self.browser_view)
        self.side_bar = SideBar(self.app, self.sidebar_view)
        row_0_cols = QHBoxLayout()
        row_0_cols.addWidget(self.side_bar, 0)
        row_0_cols.addWidget(self.sidebar_view, 1)
        row_0_cols.addWidget(self.browser_view, 2)
        row_0_cols.setSpacing(0)
        rows = QVBoxLayout()
        rows.addWidget(self.navigation_bar, 0)
        rows.addLayout(row_0_cols, 1)
        rows.setContentsMargins(0, 0, 0, 0)
        rows.setSpacing(0)
        frame = QFrame()
        frame.setLayout(rows)
        self.setCentralWidget(frame)

        if self.app.platform == 'WINDOWS':
            self.show()

        # Browser can be embedded only after layout was set up
        self.browser_view.embedBrowser()
        self.sidebar_view.embedBrowser()

        if self.app.platform == 'LINUX':
            main_container = QWidget.createWindowContainer(self.browser_view.hidden_window, parent=self)
            row_0_cols.addWidget(main_container, 2)
            sidebar_container = QWidget.createWindowContainer(self.sidebar_view.hidden_window, parent=self)
            row_0_cols.addWidget(sidebar_container, 2)
        self.sidebar_view.setFixedWidth(0)

    def closeEvent(self, event):
        if self.browser_view.browser:
            self.browser_view.browser.CloseBrowser(True)
            self.browser_view.browser = None
        if self.sidebar_view.browser:
            self.sidebar_view.browser.CloseBrowser(True)
            self.sidebar_view.browser = None
