"""صفحه گیم‌پلی یک مرحله — responsive و مناسب موبایل."""

import random

from kivy.metrics import dp, sp
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from config import (
    STAGES, PLAYER_SIZE, PLAYER_X, GRAVITY, JUMP_VELOCITY,
    GAME_FPS, LOW_RAM, LOW_RAM_MAX_OBSTACLES,
)
from entities import Character, Obstacle, VerticalObstacle, DeadlyObstacle
from ui import label_kwargs, button_kwargs, PersianLabel, PersianButton


class GameWorld(Widget):
    """دنیای بازی: بازیکن، موانع، برخورد، امتیاز."""

    score = NumericProperty(0)
    game_over = BooleanProperty(False)
    stage_id = NumericProperty(1)

    def __init__(self, stage_id=1, on_game_over=None, **kwargs):
        super().__init__(**kwargs)
        self.stage_id = stage_id
        self.cfg = STAGES[stage_id]
        self.on_game_over = on_game_over
        self.obstacles = []
        self._clock = None
        self._passed = set()
        self._scale = 1.0

        with self.canvas.before:
            Color(0.08, 0.1, 0.16, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._on_size)

        self.character = Character(
            size_x=PLAYER_SIZE,
            size_y=PLAYER_SIZE,
            gravity=GRAVITY,
            jump_velocity=JUMP_VELOCITY,
        )
        self.add_widget(self.character)

        self.score_label = PersianLabel(
            text="امتیاز: 0",
            font_size=sp(18),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(0.42, None),
            height=dp(38),
            halign="left",
            valign="middle",
            **label_kwargs(True),
        )
        self.add_widget(self.score_label)

        self.stage_label = PersianLabel(
            text=self.cfg["name"],
            font_size=sp(13),
            color=(0.85, 0.85, 0.95, 1),
            size_hint=(0.60, None),
            height=dp(32),
            halign="left",
            valign="middle",
            **label_kwargs(),
        )
        self.add_widget(self.stage_label)

        self.hint_label = PersianLabel(
            text="لمس / کلیک = پرش",
            font_size=sp(12),
            color=(1, 1, 1, 0.45),
            size_hint=(0.5, None),
            height=dp(28),
            halign="center",
            valign="middle",
            **label_kwargs(),
        )
        self.add_widget(self.hint_label)

    def _on_size(self, *args):
        self._update_bg()
        self._layout_hud()

    def _layout_hud(self):
        margin = dp(10)
        self.score_label.pos = (self.x + margin, self.top - dp(44))
        self.stage_label.pos = (self.x + margin, self.top - dp(76))
        self.hint_label.pos = (self.center_x - self.hint_label.width / 2, self.y + dp(8))

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self._layout_hud()

    def _world_scale(self):
        # مقیاس پایه 480×720؛ روی موبایل‌های بزرگ عناصر بازی هم متناسب رشد می‌کنند.
        return max(0.72, min(1.65, min(self.width / 480.0, self.height / 720.0)))

    def start(self):
        self.reset()
        if self._clock:
            self._clock.cancel()
        self._clock = Clock.schedule_interval(self.update, 1 / GAME_FPS)

    def stop(self):
        if self._clock:
            self._clock.cancel()
            self._clock = None

    def reset(self):
        self.game_over = False
        self.score = 0
        self._passed = set()
        self.score_label.text = "امتیاز: 0"
        self._scale = self._world_scale()

        for ob in list(self.obstacles):
            self.remove_widget(ob)
        self.obstacles = []

        psize = max(dp(20), PLAYER_SIZE * self._scale)
        self.character.size = (psize, psize)
        self.character.size_x = psize
        self.character.size_y = psize
        self.character.gravity = GRAVITY * self._scale
        self.character.jump_velocity = JUMP_VELOCITY * self._scale
        self.character.x = self.x + max(dp(18), PLAYER_X * self._scale)
        self.character.y = self.y + self.height / 2 - psize / 2
        self.character.velocity_y = 0

        self._spawn_obstacles()

    def _spawn_obstacles(self):
        cfg = self.cfg
        scale = self._scale
        start_x = self.width + dp(60)
        obstacle_count = min(cfg["num_obstacles"], LOW_RAM_MAX_OBSTACLES) if LOW_RAM else cfg["num_obstacles"]
        spacing = cfg["spacing"] * scale

        for i in range(obstacle_count):
            x = self.x + start_x + i * spacing
            w = max(dp(22), random.randint(*cfg["w_range"]) * scale)
            h = max(dp(42), random.randint(*cfg["h_range"]) * scale)
            max_y = max(self.y, self.top - h)
            y = random.uniform(self.y, max_y)
            roll = random.random()

            common = dict(
                x=x,
                y=y,
                size_x=w,
                size_y=h,
                velocity_x=cfg["speed"] * scale,
                acceleration_x=cfg["accel"] * scale,
            )

            if roll < cfg["deadly_chance"]:
                ob = DeadlyObstacle(**common)
            elif roll < cfg["deadly_chance"] + cfg["vertical_chance"]:
                ob = VerticalObstacle(
                    velocity_y=cfg["v_speed"] * scale * random.choice([-1, 1]),
                    **common,
                )
            else:
                ob = Obstacle(**common)

            self.obstacles.append(ob)
            self.add_widget(ob)

    def on_touch_down(self, touch):
        if self.game_over:
            return False
        if self.collide_point(*touch.pos):
            self.character.jump()
            return True
        return super().on_touch_down(touch)

    def update(self, dt):
        if self.game_over:
            return

        self.character.update()

        for ob in self.obstacles:
            ob.update()
            if id(ob) not in self._passed and ob.x + ob.size_x < self.character.x:
                self._passed.add(id(ob))
                self.score += 1
                self.score_label.text = f"امتیاز: {self.score}"

            if ob.x + ob.size_x < self.x:
                max_x = max((o.x for o in self.obstacles), default=self.right)
                ob.recycle(self.cfg, start_x=max_x + self.cfg["spacing"] * self._scale, world=self)
                self._passed.discard(id(ob))

        self._check_collision()
        self._check_bounds()

    def _check_collision(self):
        cx, cy = self.character.x, self.character.y
        cw, ch = self.character.size_x, self.character.size_y
        pad = max(1, self._scale)
        for ob in self.obstacles:
            if (
                cx + pad < ob.x + ob.size_x
                and cx + cw - pad > ob.x
                and cy + pad < ob.y + ob.size_y
                and cy + ch - pad > ob.y
            ):
                self._trigger_game_over()
                return

    def _check_bounds(self):
        if self.character.y + self.character.size_y > self.top:
            self.character.y = self.top - self.character.size_y
            self._trigger_game_over()
        elif self.character.y < self.y:
            self.character.y = self.y
            self._trigger_game_over()

    def _trigger_game_over(self):
        if self.game_over:
            return
        self.game_over = True
        if self.on_game_over:
            self.on_game_over(self.score)


class GameScreen(Screen):
    """صفحه کامل یک مرحله با دکمه بازگشت و پنل Game Over."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stage_id = 1
        self.world = None
        self.overlay = None
        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

    def on_pre_enter(self, *args):
        self.root_layout.clear_widgets()
        self.world = GameWorld(stage_id=self.stage_id, on_game_over=self._show_game_over)
        self.root_layout.add_widget(self.world)
        self.world.size = self.size
        self.world.pos = self.pos
        self.bind(size=self._sync_world, pos=self._sync_world)

        back_btn = PersianButton(
            text="منو",
            size_hint=(None, None),
            size=(dp(76), dp(42)),
            pos_hint={"right": 0.98, "top": 0.98},
            background_color=(0.25, 0.28, 0.4, 0.9),
            font_size=sp(13),
            halign="center",
            valign="middle",
            **button_kwargs(),
        )
        back_btn.bind(size=lambda inst, s: setattr(inst, "text_size", s))
        back_btn.bind(on_release=self._go_menu)
        self.root_layout.add_widget(back_btn)
        self.back_btn = back_btn

    def on_enter(self, *args):
        Clock.schedule_once(lambda dt: self._start_world(), 0.05)

    def on_leave(self, *args):
        if self.world:
            self.world.stop()

    def _sync_world(self, *args):
        if self.world:
            self.world.size = self.size
            self.world.pos = self.pos

    def _start_world(self):
        if self.world:
            self.world.size = self.size
            self.world.pos = self.pos
            self.world.start()

    def _go_menu(self, *args):
        if self.world:
            self.world.stop()
        self.manager.current = "menu"

    def _show_game_over(self, score):
        if self.overlay:
            self.root_layout.remove_widget(self.overlay)

        panel = BoxLayout(
            orientation="vertical",
            size_hint=(0.84, 0.44),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            spacing=dp(10),
            padding=dp(16),
        )
        with panel.canvas.before:
            Color(0.05, 0.06, 0.1, 0.92)
            panel._bg = Rectangle(pos=panel.pos, size=panel.size)

        def _upd(instance, value):
            panel._bg.pos = instance.pos
            panel._bg.size = instance.size

        panel.bind(pos=_upd, size=_upd)

        title = PersianLabel(
            text="تمام!",
            font_size=sp(28),
            bold=True,
            color=(1, 0.35, 0.35, 1),
            size_hint_y=None,
            height=dp(44),
            halign="center",
            valign="middle",
            **label_kwargs(True),
        )
        score_lbl = PersianLabel(
            text=f"امتیاز شما: {score}",
            font_size=sp(19),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(34),
            halign="center",
            valign="middle",
            **label_kwargs(),
        )
        stage_lbl = PersianLabel(
            text=STAGES[self.stage_id]["name"],
            font_size=sp(13),
            color=(0.7, 0.75, 0.9, 1),
            size_hint_y=None,
            height=dp(30),
            halign="center",
            valign="middle",
            **label_kwargs(),
        )

        for lbl in (title, score_lbl, stage_lbl):
            lbl.bind(size=lambda inst, s: setattr(inst, "text_size", s))

        btns = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        retry = PersianButton(
            text="دوباره",
            background_color=(0.2, 0.65, 0.35, 1),
            font_size=sp(14),
            **button_kwargs(),
        )
        menu = PersianButton(
            text="منوی مراحل",
            background_color=(0.3, 0.35, 0.55, 1),
            font_size=sp(14),
            **button_kwargs(),
        )
        for btn in (retry, menu):
            btn.bind(size=lambda inst, s: setattr(inst, "text_size", s))
        retry.bind(on_release=self._retry)
        menu.bind(on_release=self._go_menu)
        btns.add_widget(retry)
        btns.add_widget(menu)

        panel.add_widget(title)
        panel.add_widget(score_lbl)
        panel.add_widget(stage_lbl)
        panel.add_widget(btns)
        self.root_layout.add_widget(panel)
        self.overlay = panel

    def _retry(self, *args):
        if self.overlay:
            self.root_layout.remove_widget(self.overlay)
            self.overlay = None
        if self.world:
            self.world.start()
