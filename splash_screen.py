"""صفحه شروع بازی خشت."""
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.metrics import sp, dp
import os

from ui import label_kwargs, PersianLabel


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        with root.canvas.before:
            Color(0.02, 0.03, 0.08, 1)
            self.bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._sync_bg, size=self._sync_bg)

        logo_path = os.path.join(os.path.dirname(__file__), "assets", "splash.png")
        if os.path.exists(logo_path):
            root.add_widget(Image(
                source=logo_path,
                size_hint=(0.72, 0.45),
                pos_hint={"center_x": 0.5, "center_y": 0.56},
                allow_stretch=True,
                keep_ratio=True,
            ))

        title_label = PersianLabel(
            text="خشت",
            font_size=sp(32),
            bold=True,
            color=(1, 0.85, 0.3, 1),
            halign="center",
            valign="middle",
            **label_kwargs(True),
            size_hint=(1, None),
            height=dp(54),
            pos_hint={"center_x": 0.5, "center_y": 0.23},
        )
        title_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        root.add_widget(title_label)

        status_label = PersianLabel(
            text="در حال آماده‌سازی...",
            font_size=sp(12),
            color=(0.7, 0.75, 0.85, 1),
            halign="center",
            valign="middle",
            **label_kwargs(),
            size_hint=(1, None),
            height=dp(32),
            pos_hint={"center_x": 0.5, "center_y": 0.16},
        )
        status_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        root.add_widget(status_label)
        self.add_widget(root)

    def _sync_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def on_enter(self, *args):
        Clock.schedule_once(self._go_menu, 1.2)

    def _go_menu(self, dt):
        if self.manager:
            self.manager.current = "menu"
