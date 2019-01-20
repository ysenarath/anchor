from PyQt5.QtWidgets import *

from anchor.app.utils import widgets


class NavigationBar(QFrame):
    def __init__(self, app, cef_widget):
        # noinspection PyArgumentList
        super(NavigationBar, self).__init__()
        self.app = app
        self.cef_widget = cef_widget
        # Init layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # Anchor button
        self.anchor = widgets.create_button("anchor")
        layout.addWidget(self.anchor, 0)
        # Reload button
        self.reload = widgets.create_button('reload')
        # noinspection PyUnresolvedReferences
        self.reload.clicked.connect(self.onReload)
        # noinspection PyArgumentList
        layout.addWidget(self.reload, 1)
        # Back button
        self.backward = widgets.create_button("backward")
        # noinspection PyUnresolvedReferences
        self.backward.clicked.connect(self.onBack)
        # noinspection PyArgumentList
        layout.addWidget(self.backward, 2)
        # Forward button
        self.forward = widgets.create_button('forward')
        # noinspection PyUnresolvedReferences
        self.forward.clicked.connect(self.onForward)
        # noinspection PyArgumentList
        layout.addWidget(self.forward, 3)
        # Url input
        self.url = QLineEdit('')
        self.url.setMinimumHeight(25)
        # noinspection PyUnresolvedReferences
        self.url.returnPressed.connect(self.onGoUrl)
        # noinspection PyArgumentList
        layout.addWidget(self.url, 4)
        # Layout
        self.setLayout(layout)
        self.updateState()

    def onBack(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.GoBack()

    def onForward(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.GoForward()

    def onReload(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.Reload()

    def onGoUrl(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.LoadUrl(self.url.text())

    def updateState(self):
        browser = self.cef_widget.browser
        if not browser:
            self.backward.setEnabled(False)
            self.forward.setEnabled(False)
            self.reload.setEnabled(False)
            self.url.setEnabled(False)
            return
        self.backward.setEnabled(browser.CanGoBack())
        self.forward.setEnabled(browser.CanGoForward())
        self.reload.setEnabled(True)
        self.url.setEnabled(True)
        self.url.setText(browser.GetUrl())
