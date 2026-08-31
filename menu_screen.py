"""منوی انتخاب مرحله — واکنش‌گرا و مناسب نمایشگرهای مختلف."""

import os

from kivy.metrics import dp, sp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.app import App

from config import STAGES
from ui import label_kwargs, button_kwargs, PersianLabel, PersianButton

ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "icon.png")


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(
            orientation="vertical",
            padding=(dp(12), dp(10)),
            spacing=dp(7),
        )
        with root.canvas.before:
            Color(0.07, 0.09, 0.14, 1)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda i, v: setattr(self._bg, "pos", v),
            size=lambda i, v: setattr(self._bg, "size", v),
        )

        # تصویر همیشه وسط صفحه و با اندازه متناسب با ارتفاع صفحه.
        if os.path.exists(ICON_PATH):
            icon_box = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(105),
                padding=(dp(4), dp(2)),
            )
            icon = Image(
                source=ICON_PATH,
                size_hint=(1, 1),
                allow_stretch=False,
                keep_ratio=True,
            )
            icon_box.add_widget(icon)
            root.add_widget(icon_box)

        title = PersianLabel(
            text="خشت",
            font_size=sp(30),
            bold=True,
            color=(1, 0.85, 0.3, 1),
            size_hint_y=None,
            height=dp(42),
            halign="center",
            valign="middle",
            **label_kwargs(True),
        )
        title.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        subtitle = PersianLabel(
            text="با لمس بپر · از موانع رد شو · زنده بمان",
            font_size=sp(12),
            color=(0.7, 0.75, 0.85, 1),
            size_hint_y=None,
            height=dp(27),
            halign="center",
            valign="middle",
            **label_kwargs(),
        )
        subtitle.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        root.add_widget(title)
        root.add_widget(subtitle)

        legend = PersianLabel(
            text="آبی = عادی   |   سبز = متحرک   |   قرمز = مرگبار",
            font_size=sp(10.5),
            color=(0.55, 0.6, 0.7, 1),
            size_hint_y=None,
            height=dp(24),
            halign="center",
            valign="middle",
            **label_kwargs(),
        )
        legend.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        root.add_widget(legend)

        # فهرست مراحل فضای باقی‌مانده را می‌گیرد و روی صفحه‌های کوتاه اسکرول می‌شود.
        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(4),
            scroll_type=["bars", "content"],
        )
        grid = GridLayout(
            cols=1,
            spacing=dp(7),
            padding=(dp(2), dp(3)),
            size_hint_y=None,
        )
        grid.bind(minimum_height=grid.setter("height"))

        for sid in sorted(STAGES.keys()):
            cfg = STAGES[sid]
            btn = PersianButton(
                text=f"{cfg['name']}\n{cfg['desc']}",
                size_hint_y=None,
                height=dp(64),
                halign="center",
                valign="middle",
                background_color=cfg["color"],
                font_size=sp(13),
                padding=(dp(10), dp(4)),
                **button_kwargs(),
            )
            btn.bind(
                size=lambda inst, s: setattr(
                    inst, "text_size", (max(0, s[0] - dp(20)), max(0, s[1] - dp(6)))
                )
            )
            btn.stage_id = sid
            btn.bind(on_release=self._open_stage)
            grid.add_widget(btn)

        scroll.add_widget(grid)
        root.add_widget(scroll)

        exit_btn = PersianButton(
            text="خروج",
            size_hint_y=None,
            height=dp(44),
            background_color=(0.55, 0.18, 0.18, 1),
            font_size=sp(14),
            halign="center",
            valign="middle",
            **button_kwargs(),
        )
        exit_btn.bind(size=lambda inst, s: setattr(inst, "text_size", s))
        exit_btn.bind(on_release=lambda *_: App.get_running_app().stop())
        root.add_widget(exit_btn)

        self.add_widget(root)

    def _open_stage(self, instance):
        game = self.manager.get_screen("game")
        game.stage_id = instance.stage_id
        self.manager.current = "game"
