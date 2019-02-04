from PyQt5.QtWidgets import *

from anchor.app.utils import widgets


class SideBar(QFrame):
    def __init__(self, app, browser_view):
        super(SideBar, self).__init__()
        self.app = app
        self.browser_view = browser_view
        # Init layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.current = None
        self.buttons = []
        for idx, item in enumerate(app.configs['sidebar']):
            button = widgets.create_button(item['name'])
            # noinspection PyUnresolvedReferences
            button.clicked.connect(self.onItemClicked(idx))
            layout.addWidget(button, idx)
            item['button'] = button
            self.buttons.append(item)
        layout.addStretch(len(self.buttons))
        self.setLayout(layout)

    def onItemClicked(self, idx):
        def temp_func():
            if self.browser_view.width() != 0 and self.current == idx:
                self.browser_view.setFixedWidth(0)
            else:
                if self.browser_view.browser:
                    if self.current != idx:
                        self.browser_view.browser.LoadUrl(self.buttons[idx]['url'])
                        self.current = idx
                else:
                    pass
                self.browser_view.setFixedWidth(600)

        return temp_func
