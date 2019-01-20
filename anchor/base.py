import logging
import os
import platform
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from cefpython3 import cefpython as cef

from anchor.app import MainWindow

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel('INFO')


class CefApplication(QApplication):
    def __init__(self, args):
        super(CefApplication, self).__init__(args)
        if not cef.GetAppSetting('external_message_pump'):
            self.timer = self.createTimer()
        self.setupIcon()

    def createTimer(self):
        timer = QTimer()
        # noinspection PyUnresolvedReferences
        timer.timeout.connect(self.onTimer)
        timer.start(10)
        return timer

    def onTimer(self):
        cef.MessageLoopWork()

    def stopTimer(self):
        # Stop the timer after Qt's message loop has ended
        self.timer.stop()

    def setupIcon(self):
        icon_path = ''
        icon_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'resources", "{0}.png'.format(icon_path))
        if os.path.exists(icon_file):
            self.setWindowIcon(QIcon(icon_file))


class Anchor:
    def __init__(self, settings, switches, configs):
        self.settings = settings
        self.switches = switches
        self.configs = configs
        self.window_utils_ = None
        self._cef_ = None

    def __enter__(self):
        sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        if self.platform == 'MAC':
            self.settings["external_message_pump"] = True  # Issue #442
        cef.Initialize(settings=self.settings, switches=self.switches)
        self.window_utils_ = cef.WindowUtils()
        self._cef_ = CefApplication([])
        return self

    def run(self):
        self.check_versions()
        if not self._cef_:
            raise NameError('Application context not initialized.')
        main_window = MainWindow(self)
        main_window.show()
        main_window.activateWindow()
        main_window.raise_()
        self._cef_.exec_()

    def __exit__(self, *args, **kwargs):
        if not cef.GetAppSetting("external_message_pump"):
            self._cef_.stopTimer()
        del self._cef_
        cef.Shutdown()

    @property
    def platform(self):
        if platform.system() == "Windows":
            return 'WINDOWS'
        elif platform.system() == "Linux":
            return 'LINUX'
        elif platform.system() == "Darwin":
            return 'MAC'
        raise OSError('Un-supported OS found. Only (Linux, Windows and Mac) is supported!')

    @staticmethod
    def check_versions():
        ver = cef.GetVersion()
        logger.info('CEF Python {ver}'.format(ver=ver['version']))
        logger.info('Chromium {ver}'.format(ver=ver['chrome_version']))
        logger.info('CEF {ver}'.format(ver=ver['cef_version']))
        logger.info('Python {ver} {arch}'.format(
            ver=platform.python_version(),
            arch=platform.architecture()[0])
        )
        assert cef.__version__ >= '57.0', 'CEF Python v57.0+ required to run this'
