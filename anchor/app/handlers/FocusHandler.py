class FocusHandler(object):
    def __init__(self, app, cef_widget):
        self.app = app
        self.cef_widget = cef_widget

    def OnSetFocus(self, **_):
        pass

    def OnGotFocus(self, browser, **_):
        # Temporary fix no. 1 for focus issues on Linux (Issue #284)
        if self.app.platform == 'LINUX':
            print('[qt.py] FocusHandler.OnGotFocus: keyboard focus fix no. 1 (Issue #284)')
            browser.SetFocus(True)
