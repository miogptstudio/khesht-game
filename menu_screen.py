"""منوی انتخاب مرحله"""

import os

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.app import App

from config import STAGES

ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "icon.png")


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical", padding=16, spacing=12)
        with root.canvas.before:
            Color(0.07, 0.09, 0.14, 1)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda i, v: setattr(self._bg, "pos", v),
            size=lambda i, v: setattr(self._bg, "size", v),
        )

        # آیکون بازی
        if os.path.exists(ICON_PATH):
            icon = Image(
                source=ICON_PATH,
                size_hint_y=None,
                height=120,
                allow_stretch=True,
                keep_ratio=True,
            )
            root.add_widget(icon)

        title = Label(
            text="خشت",
            font_size="42sp",
            bold=True,
            color=(1, 0.85, 0.3, 1),
            size_hint_y=None,
            height=56,
        )
        subtitle = Label(
            text="با لمس بپر · از موانع رد شو · زنده بمان",
            font_size="14sp",
            color=(0.7, 0.75, 0.85, 1),
            size_hint_y=None,
            height=28,
        )
        root.add_widget(title)
        root.add_widget(subtitle)

        # راهنمای رنگ‌ها
        legend = Label(
            text="آبی = عادی   |   سبز = متحرک   |   قرمز = مرگبار",
            font_size="12sp",
            color=(0.55, 0.6, 0.7, 1),
            size_hint_y=None,
            height=24,
        )
        root.add_widget(legend)

        scroll = ScrollView(do_scroll_x=False)
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=(4, 4))
        grid.bind(minimum_height=grid.setter("height"))

        for sid in sorted(STAGES.keys()):
            cfg = STAGES[sid]
            btn = Button(
                text=f"{cfg['name']}\n{cfg['desc']}",
                size_hint_y=None,
                height=72,
                halign="center",
                valign="middle",
                background_color=cfg["color"],
                font_size="15sp",
            )
            btn.bind(size=lambda inst, s: setattr(inst, "text_size", (s[0] - 20, None)))
            btn.stage_id = sid
            btn.bind(on_release=self._open_stage)
            grid.add_widget(btn)

        scroll.add_widget(grid)
        root.add_widget(scroll)

        exit_btn = Button(
            text="خروج",
            size_hint_y=None,
            height=48,
            background_color=(0.55, 0.18, 0.18, 1),
            font_size="16sp",
        )
        exit_btn.bind(on_release=lambda *_: App.get_running_app().stop())
        root.add_widget(exit_btn)

        self.add_widget(root)

    def _open_stage(self, instance):
        game = self.manager.get_screen("game")
        game.stage_id = instance.stage_id
        self.manager.current = "game"
