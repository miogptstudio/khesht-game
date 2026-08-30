# ساخت فایل APK بازی خشت

در محیط چت نمی‌شود APK نهایی تولید کرد؛ باید روی **کامپیوتر خودت** (ترجیحاً لینوکس یا WSL در ویندوز) بسازی.

## پیش‌نیاز

- لینوکس Ubuntu 22.04 یا WSL2
- اینترنت پایدار (اولین بیلد ممکن است ۳۰–۹۰ دقیقه طول بکشد)
- حداقل حدود ۱۰–۱۵ گیگ فضای خالی

## مراحل (Ubuntu / WSL)

```bash
# 1) وابستگی‌های سیستم
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv \
  autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
  libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 2) محیط مجازی
cd khesht
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install buildozer cython

# 3) ساخت APK دیباگ
buildozer -v android debug
```

بعد از اتمام موفق، فایل اینجاست:

```text
bin/خشت-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

(نام دقیق ممکن است کمی فرق کند؛ داخل پوشه `bin/` را ببین.)

## نصب روی گوشی

1. فایل APK را به گوشی منتقل کن  
2. در تنظیمات اندروید، نصب از منابع ناشناس را برای آن برنامه (Files / Chrome) فعال کن  
3. روی APK بزن و نصب کن  

## نسخه انتشار (Release)

```bash
buildozer -v android release
```

برای انتشار در گوگل‌پلی باید keystore بسازی و امضا کنی.

## اگر خطا دیدی

- اولین اجرا SDK و NDK را دانلود می‌کند؛ صبور باش  
- اگر حافظه کم است فقط یک معماری بگذار در `buildozer.spec`:

```text
android.archs = arm64-v8a
```

- لاگ کامل با `buildozer -v android debug` دیده می‌شود  

## نکته

بدون این بیلد، بازی را می‌توانی روی کامپیوتر با دستور زیر هم اجرا کنی:

```bash
pip install kivy
python main.py
```
