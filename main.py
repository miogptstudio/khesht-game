"""
بازی خشت — نسخه کامل
اجرا: python main.py
نیازمندی: pip install kivy
"""

import os

from kivy.config import Config

Config.set("graphics", "width", "480")
Config.set("graphics", "height", "720")
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window

from config import WINDOW_WIDTH, WINDOW_HEIGHT
from splash_screen import SplashScreen
from menu_screen import MenuScreen
from game_screen import GameScreen

ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "icon.png")


class KheshtApp(App):
    title = "خشت"
    icon = ICON_PATH

    def build(self):
        Window.clearcolor = (0.02, 0.03, 0.08, 1)
        try:
            Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
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
