"""تنظیمات رابط کاربری فارسی و واکنش‌گرا برای بازی خشت."""
import os

from kivy.metrics import dp, sp
from kivy.uix.label import Label
from kivy.uix.button import Button

BASE_DIR = os.path.dirname(__file__)
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")
FONT_REGULAR = os.path.join(FONT_DIR, "NotoSansArabic-Regular.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "NotoSansArabic-Bold.ttf")


def _font_path(bold=False):
    path = FONT_BOLD if bold else FONT_REGULAR
    return path if os.path.exists(path) else None


def label_kwargs(bold=False):
    path = _font_path(bold)
    return {"font_name": path} if path else {}


def button_kwargs(bold=False):
    path = _font_path(bold)
    return {"font_name": path} if path else {}


def prepare_text(widget, rtl=True):
    """تنظیم متن برای خوانایی فارسی؛ بدون دست‌کاری محتوای آن."""
    if rtl:
        widget.halign = "right"
        widget.valign = "middle"
    return widget


def responsive_height(parent_height, fraction, minimum, maximum):
    return max(dp(minimum), min(dp(maximum), parent_height * fraction))
