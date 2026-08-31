"""صفحه گیم‌پلی یک مرحله"""

import random

from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line

from config import (
    STAGES, PLAYER_SIZE, PLAYER_X, GRAVITY, JUMP_VELOCITY,
    GAME_FPS, LOW_RAM, LOW_RAM_MAX_OBSTACLES,
)
from entities import Character, Obstacle, VerticalObstacle, DeadlyObstacle


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

        with self.canvas.before:
            Color(0.08, 0.1, 0.16, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
            # خطوط تزئینی پس‌زمینه
            Color(0.12, 0.16, 0.25, 1)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.character = Character(
            size_x=PLAYER_SIZE,
            size_y=PLAYER_SIZE,
            gravity=GRAVITY,
            jump_velocity=JUMP_VELOCITY,
        )
        self.add_widget(self.character)

        self.score_label = Label(
            text="امتیاز: 0",
            font_size="22sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 40),
            halign="left",
        )
        self.add_widget(self.score_label)

        self.stage_label = Label(
            text=self.cfg["name"],
            font_size="16sp",
            color=(0.85, 0.85, 0.95, 1),
            size_hint=(None, None),
            size=(280, 30),
        )
        self.add_widget(self.stage_label)

        self.hint_label = Label(
            text="لمس / کلیک = پرش",
            font_size="14sp",
            color=(1, 1, 1, 0.45),
            size_hint=(None, None),
            size=(200, 28),
        )
        self.add_widget(self.hint_label)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.score_label.pos = (self.x + 12, self.top - 48)
        self.stage_label.pos = (self.x + 12, self.top - 78)
        self.hint_label.pos = (self.center_x - 100, self.y + 12)

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

        # پاک کردن موانع قبلی
        for ob in list(self.obstacles):
            self.remove_widget(ob)
        self.obstacles = []

        # قرار دادن بازیکن
        self.character.size = (PLAYER_SIZE, PLAYER_SIZE)
        self.character.size_x = PLAYER_SIZE
        self.character.size_y = PLAYER_SIZE
        self.character.x = PLAYER_X
        self.character.y = self.height / 2 - PLAYER_SIZE / 2
        self.character.velocity_y = 0

        self._spawn_obstacles()

    def _spawn_obstacles(self):
        cfg = self.cfg
        start_x = self.width + 60
        obstacle_count = min(cfg["num_obstacles"], LOW_RAM_MAX_OBSTACLES) if LOW_RAM else cfg["num_obstacles"]
        for i in range(obstacle_count):
            x = start_x + i * cfg["spacing"]
            roll = random.random()
            w = random.randint(*cfg["w_range"])
            h = random.randint(*cfg["h_range"])
            max_y = max(0, int(self.height - h))
            y = random.randint(0, max_y)

            common = dict(
                x=x,
                y=y,
                size_x=w,
                size_y=h,
                velocity_x=cfg["speed"],
                acceleration_x=cfg["accel"],
            )

            if roll < cfg["deadly_chance"]:
                ob = DeadlyObstacle(**common)
            elif roll < cfg["deadly_chance"] + cfg["vertical_chance"]:
                ob = VerticalObstacle(
                    velocity_y=cfg["v_speed"] * random.choice([-1, 1]),
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
            # امتیاز وقتی از مانع رد شدی
            if id(ob) not in self._passed and ob.x + ob.size_x < self.character.x:
                self._passed.add(id(ob))
                self.score += 1
                self.score_label.text = f"امتیاز: {self.score}"

            # بازیافت مانع خارج‌شده
            if ob.x + ob.size_x < 0:
                # دورترین مانع را پیدا کن و بعد از آن بگذار
                max_x = max((o.x for o in self.obstacles), default=self.width)
                ob.recycle(self.cfg, start_x=max_x + self.cfg["spacing"])
                self._passed.discard(id(ob))

        self._check_collision()
        self._check_bounds()

    def _check_collision(self):
        cx, cy = self.character.x, self.character.y
        cw, ch = self.character.size_x, self.character.size_y
        # hitbox تقریباً کامل — نسخه سخت
        pad = 1
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
        if self.character.y + self.character.size_y > self.height:
            self.character.y = self.height - self.character.size_y
            self._trigger_game_over()
        elif self.character.y < 0:
            self.character.y = 0
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
        self.world = GameWorld(
            stage_id=self.stage_id,
            on_game_over=self._show_game_over,
        )
        self.root_layout.add_widget(self.world)
        # اتصال اندازه به کل صفحه
        self.world.size = self.size
        self.world.pos = self.pos
        self.bind(size=self._sync_world, pos=self._sync_world)

        # دکمه بازگشت به منو (بالا چپ در RTL حس، اینجا راست)
        back_btn = Button(
            text="منو",
            size_hint=(None, None),
            size=(70, 40),
            pos_hint={"right": 0.98, "top": 0.98},
            background_color=(0.25, 0.28, 0.4, 0.9),
            font_size="15sp",
        )
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
            size_hint=(0.75, 0.42),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            spacing=12,
            padding=20,
        )
        with panel.canvas.before:
            Color(0.05, 0.06, 0.1, 0.92)
            panel._bg = Rectangle(pos=panel.pos, size=panel.size)

            def _upd(instance, value):
                panel._bg.pos = instance.pos
                panel._bg.size = instance.size

            panel.bind(pos=_upd, size=_upd)

        title = Label(
            text="تمام!",
            font_size="32sp",
            bold=True,
            color=(1, 0.35, 0.35, 1),
            size_hint_y=None,
            height=48,
        )
        score_lbl = Label(
            text=f"امتیاز شما: {score}",
            font_size="22sp",
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=36,
        )
        stage_lbl = Label(
            text=STAGES[self.stage_id]["name"],
            font_size="15sp",
            color=(0.7, 0.75, 0.9, 1),
            size_hint_y=None,
            height=28,
        )

        btns = BoxLayout(size_hint_y=None, height=48, spacing=10)
        retry = Button(
            text="دوباره",
            background_color=(0.2, 0.65, 0.35, 1),
            font_size="16sp",
        )
        menu = Button(
            text="منوی مراحل",
            background_color=(0.3, 0.35, 0.55, 1),
            font_size="16sp",
        )
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
