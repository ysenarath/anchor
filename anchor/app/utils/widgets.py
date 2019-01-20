import os

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QPushButton

from anchor.app.utils.styles import BUTTON_STYLE
from anchor.const import RESOURCE_PATH


def create_button(icon=None, size=32):
    button = QPushButton()
    button.setStyleSheet(BUTTON_STYLE)
    button.setMaximumWidth(size)
    button.setMaximumHeight(size)
    button.setMinimumHeight(size)
    button.setMinimumWidth(size)
    if icon:
        pixmap = QPixmap(os.path.join(RESOURCE_PATH, 'icons', '{0}.png'.format(icon)))
        icon = QIcon(pixmap)
        button.setIcon(icon)
        button.setIconSize(button.size())
    return button
