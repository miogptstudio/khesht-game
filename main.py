"""
بازی خشت — نسخه کامل
اجرا: python main.py
نیازمندی: pip install kivy
"""

import os

__version__ = "1.0.2"

from kivy.config import Config
from kivy.utils import platform

# فقط برای اجرای دسکتاپ اندازه پیش‌فرض تعیین می‌شود.
# روی Android نباید Window.size ثابت شود؛ وگرنه برنامه روی بخشی از صفحه می‌افتد.
if platform != "android":
    Config.set("graphics", "width", "480")
    Config.set("graphics", "height", "720")
    Config.set("graphics", "resizable", "1")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window

from splash_screen import SplashScreen
from menu_screen import MenuScreen
from game_screen import GameScreen

ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "icon.png")


class KheshtApp(App):
    title = "خشت"
    icon = ICON_PATH

    def build(self):
        Window.clearcolor = (0.02, 0.03, 0.08, 1)

        # روی Android اندازه واقعی صفحه توسط سیستم تعیین می‌شود.
        if platform != "android":
            try:
                Window.size = (480, 720)
            except Exception:
                pass

        sm = ScreenManager(transition=FadeTransition(duration=0.35))
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.current = "splash"
        return sm


if __name__ == "__main__":
    KheshtApp().run()
