"""صفحه اسپلش — لوگوی استودیو هنگام ورود به بازی"""

import os

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.animation import Animation

LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "splash_logo.jpg")


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()
        with root.canvas.before:
            Color(0.02, 0.03, 0.08, 1)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda i, v: setattr(self._bg, "pos", v),
            size=lambda i, v: setattr(self._bg, "size", v),
        )

        self.logo = Image(
            source=LOGO_PATH if os.path.exists(LOGO_PATH) else "",
            size_hint=(0.85, 0.55),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            allow_stretch=True,
            keep_ratio=True,
            opacity=0,
        )
        root.add_widget(self.logo)

        self.caption = Label(
            text="در حال ورود...",
            font_size="16sp",
            color=(0.6, 0.75, 1, 0.85),
            size_hint=(1, None),
            height=36,
            pos_hint={"center_x": 0.5, "y": 0.12},
            opacity=0,
        )
        root.add_widget(self.caption)

        self.add_widget(root)

    def on_enter(self, *args):
        # ظاهر شدن نرم لوگو
        Animation(opacity=1, duration=0.6).start(self.logo)
        Animation(opacity=1, duration=0.8).start(self.caption)
        # بعد از حدود ۲.۵ ثانیه برو به منو
        Clock.schedule_once(self._go_menu, 2.5)

    def _go_menu(self, dt):
        if self.manager:
            self.manager.current = "menu"
