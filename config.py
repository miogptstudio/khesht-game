"""تنظیمات مراحل بازی خشت — نسخه خیلی سخت"""

# اندازه پنجره
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 720

# فیزیک بازیکن — کنترل تنگ‌تر
PLAYER_SIZE = 24
PLAYER_X = 70
GRAVITY = -0.72
JUMP_VELOCITY = 10.5


# بهینه‌سازی خودکار برای دستگاه‌های کم‌حافظه.
# getMemoryClass سقف حافظه اپ است، نه RAM واقعی دستگاه؛ بنابراین علاوه بر آن
# از isLowRamDevice استفاده می‌کنیم تا گوشی‌های ضعیف‌تر هم درست شناسایی شوند.
LOW_RAM = False
DEVICE_MEMORY_MB = 0
try:
    from jnius import autoclass
    ActivityThread = autoclass("android.app.ActivityThread")
    activity = ActivityThread.currentActivity()
    if activity is not None:
        ActivityManager = autoclass("android.app.ActivityManager")
        am = activity.getSystemService(activity.ACTIVITY_SERVICE)
        DEVICE_MEMORY_MB = int(am.getMemoryClass())
        LOW_RAM = bool(am.isLowRamDevice()) or DEVICE_MEMORY_MB <= 192
except Exception:
    pass

GAME_FPS = 30 if LOW_RAM else 60
LOW_RAM_MAX_OBSTACLES = 8

# نام و تنظیمات هر مرحله
# spacing: فاصله افقی بین موانع
# speed: سرعت پایه موانع (منفی = به چپ)
# accel: شتاب اضافی در هر فریم
# vertical_chance: احتمال مانع عمودی (۰ تا ۱)
# deadly_chance: احتمال مانع مرگبار
STAGES = {
    1: {
        "name": "مرحله ۱ — آسان؟",
        "desc": "دیگه آسان نیست. از همین اول فشار است.",
        "color": (0.2, 0.7, 0.3, 1),
        "num_obstacles": 14,
        "spacing": 145,
        "speed": -5.5,
        "accel": -0.001,
        "vertical_chance": 0.2,
        "deadly_chance": 0.05,
        "w_range": (32, 48),
        "h_range": (70, 140),
        "v_speed": 3.5,
    },
    2: {
        "name": "مرحله ۲ — متوسط؟",
        "desc": "سریع‌تر، فشرده‌تر، بی‌رحم‌تر.",
        "color": (0.3, 0.6, 0.9, 1),
        "num_obstacles": 16,
        "spacing": 130,
        "speed": -6.5,
        "accel": -0.0015,
        "vertical_chance": 0.3,
        "deadly_chance": 0.1,
        "w_range": (34, 52),
        "h_range": (80, 160),
        "v_speed": 4.5,
    },
    3: {
        "name": "مرحله ۳ — سخت",
        "desc": "موانع سبز دیوانه‌وار بالا پایین می‌روند.",
        "color": (0.9, 0.7, 0.2, 1),
        "num_obstacles": 18,
        "spacing": 120,
        "speed": -7.5,
        "accel": -0.002,
        "vertical_chance": 0.45,
        "deadly_chance": 0.15,
        "w_range": (36, 55),
        "h_range": (90, 180),
        "v_speed": 5.5,
    },
    4: {
        "name": "مرحله ۴ — خیلی سخت",
        "desc": "شتاب شدید. لحظه‌ای غافل نشو.",
        "color": (0.95, 0.5, 0.15, 1),
        "num_obstacles": 20,
        "spacing": 110,
        "speed": -8.5,
        "accel": -0.003,
        "vertical_chance": 0.5,
        "deadly_chance": 0.2,
        "w_range": (38, 58),
        "h_range": (100, 200),
        "v_speed": 6.5,
    },
    5: {
        "name": "مرحله ۵ — روانی",
        "desc": "فاصله کم، سرعت بالا، موانع بلند.",
        "color": (0.6, 0.3, 0.8, 1),
        "num_obstacles": 22,
        "spacing": 100,
        "speed": -9.5,
        "accel": -0.004,
        "vertical_chance": 0.55,
        "deadly_chance": 0.25,
        "w_range": (40, 60),
        "h_range": (110, 220),
        "v_speed": 7.5,
    },
    6: {
        "name": "مرحله ۶ — فوق‌روانی",
        "desc": "تقریباً غیرممکن. تقریباً.",
        "color": (0.8, 0.25, 0.55, 1),
        "num_obstacles": 24,
        "spacing": 95,
        "speed": -11.0,
        "accel": -0.005,
        "vertical_chance": 0.6,
        "deadly_chance": 0.3,
        "w_range": (42, 65),
        "h_range": (120, 250),
        "v_speed": 8.5,
    },
    7: {
        "name": "مرحله ۷ — دیدار با قبر",
        "desc": "قبر از همین‌جا شروع می‌شود.",
        "color": (0.75, 0.15, 0.15, 1),
        "num_obstacles": 26,
        "spacing": 90,
        "speed": -12.5,
        "accel": -0.006,
        "vertical_chance": 0.55,
        "deadly_chance": 0.4,
        "w_range": (44, 70),
        "h_range": (130, 280),
        "v_speed": 9.5,
    },
    8: {
        "name": "مرحله ۸ — جهنم",
        "desc": "دیگر بهشت نیست. زنده ماندن یعنی معجزه.",
        "color": (0.95, 0.2, 0.1, 1),
        "num_obstacles": 30,
        "spacing": 85,
        "speed": -14.0,
        "accel": -0.008,
        "vertical_chance": 0.65,
        "deadly_chance": 0.5,
        "w_range": (48, 75),
        "h_range": (150, 320),
        "v_speed": 11.0,
    },
}
