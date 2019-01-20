class LoadHandler(object):
    def __init__(self, app, container):
        self.app = app
        self.initial_app_loading = True
        self.container = container

    def OnLoadingStateChange(self, **_):
        self.container.navigation_bar.updateState()

    def OnLoadStart(self, browser, **_):
        self.container.navigation_bar.url.setText(browser.GetUrl())
        if self.initial_app_loading:
            self.container.navigation_bar.cef_widget.setFocus()
            # Temporary fix no. 2 for focus issue on Linux (Issue #284)
            if self.app.platform == 'LINUX':
                print('[qt.py] LoadHandler.OnLoadStart: keyboard focus fix no. 2 (Issue #284)')
                browser.SetFocus(True)
            self.initial_app_loading = False
