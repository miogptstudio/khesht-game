"""رابط کاربری فارسی و واکنش‌گرا برای بازی خشت.

این ماژول متن فارسی را قبل از ارسال به Kivy شکل‌دهی و راست‌به‌چپ می‌کند.
برای جلوگیری از مربع شدن حروف، فونت Noto Sans Arabic که فرم‌های ارائه‌شده
حروف را دارد برای متن‌های فارسی استفاده می‌شود. Suls.ttf نیز داخل پروژه
نگه داشته شده و برای استفاده‌های تزئینی در دسترس است.
"""
import os
import re

from kivy.metrics import dp, sp
from kivy.resources import resource_find
from kivy.uix.label import Label
from kivy.uix.button import Button

from arabic_reshaper import reshape
from bidi.algorithm import get_display

BASE_DIR = os.path.dirname(__file__)
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")
FONT_REGULAR = os.path.join(FONT_DIR, "NotoSansArabic-Regular.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "NotoSansArabic-Bold.ttf")
SULS_FONT = os.path.join(FONT_DIR, "Suls.ttf")

_ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")


def _resolve(path):
    if os.path.exists(path):
        return path
    found = resource_find(path)
    return found if found else path


def _font_path(bold=False):
    path = FONT_BOLD if bold else FONT_REGULAR
    return _resolve(path)


def label_kwargs(bold=False):
    return {"font_name": _font_path(bold)}


def button_kwargs(bold=False):
    return {"font_name": _font_path(bold)}


def shape_farsi(text):
    """شکل‌دهی حروف عربی/فارسی و اعمال BiDi بدون تغییر محتوای متن."""
    if not isinstance(text, str) or not text or not _ARABIC_RE.search(text):
        return text

    # هر خط جداگانه پردازش می‌شود تا newline و متن‌های ترکیبی درست بمانند.
    out = []
    for line in text.split("\n"):
        if _ARABIC_RE.search(line):
            try:
                line = get_display(reshape(line), base_dir="R")
            except TypeError:
                line = get_display(reshape(line))
        out.append(line)
    return "\n".join(out)


class PersianLabel(Label):
    """Label با فونت فارسی و shaping خودکار."""
    def __init__(self, **kwargs):
        original = kwargs.get("text", "")
        kwargs.setdefault("font_name", _font_path(False))
        super().__init__(**kwargs)
        self._raw_text = original
        self._shaping_guard = False

    def on_text(self, instance, value):
        if self._shaping_guard:
            return
        shaped = shape_farsi(value)
        if shaped != value:
            self._shaping_guard = True
            try:
                self.text = shaped
            finally:
                self._shaping_guard = False


class PersianButton(Button):
    """Button با فونت فارسی و shaping خودکار."""
    def __init__(self, **kwargs):
        original = kwargs.get("text", "")
        kwargs.setdefault("font_name", _font_path(False))
        super().__init__(**kwargs)
        self._raw_text = original
        self._shaping_guard = False

    def on_text(self, instance, value):
        if self._shaping_guard:
            return
        shaped = shape_farsi(value)
        if shaped != value:
            self._shaping_guard = True
            try:
                self.text = shaped
            finally:
                self._shaping_guard = False


def prepare_text(widget, rtl=True):
    if rtl:
        widget.halign = "right"
        widget.valign = "middle"
    return widget


def responsive_height(parent_height, fraction, minimum, maximum):
    return max(dp(minimum), min(dp(maximum), parent_height * fraction))
