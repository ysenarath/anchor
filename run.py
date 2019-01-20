# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+.

from anchor import Anchor

SETTINGS = {
    # "debug": True,
    # "log_severity": cef.LOGSEVERITY_INFO,
    # "log_file": "debug.log",
    # "product_version": "MyProduct/10.00",
    # "user_agent": "MyAgent/20.00 MyProduct/10.00",
    # "windowless_rendering_enabled": True,
    'cache_path': 'cache/'
}

SWITCHES = {
    # "enable-media-stream": "",
    # "proxy-server": "socks5://127.0.0.1:8888",
    # "disable-gpu": "",
}

CONFIGS = {
    'title': 'Anchor',
    'height': 400,
    'width': 300,
    'home-page': 'https://www.google.com/',
    'sidebar': [
        {
            'name': 'facebook-messenger',
            'url': 'https://www.messenger.com/',
        },
        {
            'name': 'gmail',
            'url': 'https://mail.google.com/',
        }
    ]
}


def main():
    kwargs = {
        'settings': SETTINGS,
        'switches': SWITCHES,
        'configs': CONFIGS
    }
    with Anchor(**kwargs) as app:
        app.run()


if __name__ == '__main__':
    main()
