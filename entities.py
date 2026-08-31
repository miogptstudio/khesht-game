"""موجودات بازی: بازیکن و انواع موانع"""

import random

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty
from kivy.graphics import Color, RoundedRectangle, Ellipse, Rectangle


class Character(Widget):
    velocity_y = NumericProperty(0)
    gravity = NumericProperty(-0.55)
    jump_velocity = NumericProperty(11)
    size_x = NumericProperty(28)
    size_y = NumericProperty(28)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (self.size_x, self.size_y)
        with self.canvas:
            # بدنه
            Color(0.95, 0.25, 0.25, 1)
            self.body = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[8]
            )
            # چشم
            Color(1, 1, 1, 1)
            self.eye = Ellipse(pos=(self.x + 14, self.y + 14), size=(10, 10))
            Color(0.1, 0.1, 0.1, 1)
            self.pupil = Ellipse(pos=(self.x + 17, self.y + 16), size=(5, 5))

        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *args):
        self.body.pos = self.pos
        self.body.size = self.size
        self.eye.pos = (self.x + self.width * 0.5, self.y + self.height * 0.45)
        self.eye.size = (self.width * 0.35, self.height * 0.35)
        self.pupil.pos = (self.x + self.width * 0.62, self.y + self.height * 0.52)
        self.pupil.size = (self.width * 0.18, self.height * 0.18)

    def update(self):
        self.velocity_y += self.gravity
        # سقف سرعت سقوط
        if self.velocity_y < -18:
            self.velocity_y = -18
        self.y += self.velocity_y
        self._sync()

    def jump(self):
        self.velocity_y = self.jump_velocity


class Obstacle(Widget):
    """مانع آبی معمولی — فقط افقی حرکت می‌کند."""

    size_x = NumericProperty(40)
    size_y = NumericProperty(80)
    velocity_x = NumericProperty(-4)
    acceleration_x = NumericProperty(0)
    kind = StringProperty("normal")

    def __init__(self, color=(0.2, 0.45, 0.95, 1), **kwargs):
        self.size_x = kwargs.pop("size_x", self.size_x)
        self.size_y = kwargs.pop("size_y", self.size_y)
        self.velocity_x = kwargs.pop("velocity_x", self.velocity_x)
        self.acceleration_x = kwargs.pop("acceleration_x", self.acceleration_x)
        super().__init__(**kwargs)
        self.size = (self.size_x, self.size_y)
        self._color = color
        with self.canvas:
            Color(*color)
            self.rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[6]
            )
            # نوار روشن برای ظاهر بهتر
            Color(1, 1, 1, 0.2)
            self.shine = Rectangle(
                pos=(self.x + 4, self.y + self.height * 0.15),
                size=(6, self.height * 0.7),
            )
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shine.pos = (self.x + 4, self.y + self.height * 0.15)
        self.shine.size = (6, max(4, self.height * 0.7))

    def update(self):
        self.velocity_x += self.acceleration_x
        # محدودیت سرعت نهایی — نسخه سخت
        if self.velocity_x < -22:
            self.velocity_x = -22
        self.x += self.velocity_x
        self._sync()

    def recycle(self, stage_cfg, start_x=None, world=None):
        """برگرداندن مانع به سمت راست صفحه با اندازه و نوع تصادفی."""
        scale = getattr(world, "_scale", 1.0) if world is not None else 1.0
        w = max(22, random.randint(*stage_cfg["w_range"]) * scale)
        h = max(42, random.randint(*stage_cfg["h_range"]) * scale)
        self.size_x = w
        self.size_y = h
        self.size = (w, h)
        right = world.right if world is not None else 480
        bottom = world.y if world is not None else 0
        top = world.top if world is not None else 720
        self.x = start_x if start_x is not None else right + random.randint(0, 40)
        max_y = max(bottom, int(top - h))
        self.y = random.uniform(bottom, max_y)
        self.velocity_x = stage_cfg["speed"]
        self._sync()


class VerticalObstacle(Obstacle):
    """مانع سبز که علاوه بر حرکت افقی، بالا و پایین می‌رود."""

    velocity_y = NumericProperty(3)

    def __init__(self, **kwargs):
        self.velocity_y = kwargs.pop("velocity_y", 3)
        kwargs.setdefault("color", (0.2, 0.75, 0.35, 1))
        super().__init__(**kwargs)
        self.kind = "vertical"

    def update(self):
        self.y += self.velocity_y
        # محدوده عمودی در GameWorld مدیریت می‌شود؛ این مقدار فقط fallback است.
        parent = self.parent
        bottom = parent.y if parent is not None else 0
        top = parent.top if parent is not None else 720
        if self.y + self.size_y > top:
            self.y = top - self.size_y
            self.velocity_y = -abs(self.velocity_y)
        elif self.y < bottom:
            self.y = bottom
            self.velocity_y = abs(self.velocity_y)
        super().update()

    def recycle(self, stage_cfg, start_x=None, world=None):
        super().recycle(stage_cfg, start_x, world=world)
        self.velocity_y = stage_cfg["v_speed"] * random.choice([-1, 1])


class DeadlyObstacle(Obstacle):
    """مانع قرمز مرگبار — کمی بزرگ‌تر و خطرناک‌تر."""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", (0.9, 0.15, 0.15, 1))
        super().__init__(**kwargs)
        self.kind = "deadly"

    def recycle(self, stage_cfg, start_x=None, world=None):
        super().recycle(stage_cfg, start_x, world=world)
        # کمی بزرگ‌تر از حالت عادی
        world_height = world.height if world is not None else 720
        bottom = world.y if world is not None else 0
        self.size_x = int(self.size_x * 1.15)
        self.size_y = min(int(self.size_y * 1.2), int(world_height * 0.45))
        self.size = (self.size_x, self.size_y)
        max_y = max(bottom, int((world.top if world is not None else 720) - self.size_y))
        self.y = random.uniform(bottom, max_y)
        self._sync()
