# ساخت APK بازی خشت با GitHub Actions

## ساختار مهم

این ZIP را طوری آماده کرده‌ایم که **خودِ محتویات ZIP ریشه Repository باشند**؛ یعنی `.github`، `main.py` و `buildozer.spec` مستقیماً در ریشه قرار بگیرند.

```text
.github/workflows/build-apk.yml
main.py
buildozer.spec
config.py
entities.py
menu_screen.py
game_screen.py
splash_screen.py
assets/
```

پوشه‌های `__pycache__` و فایل‌های `.pyc` عمداً حذف شده‌اند و لازم نیستند. `.gitignore` هم جلوی ساخته‌شدن دوبارهٔ آن‌ها را می‌گیرد.

## روش Build

1. یک Repository بساز.
2. **محتویات این ZIP را** در ریشه Repository آپلود کن؛ خود پوشهٔ والد را داخل Repository نگذار.
3. Commit کن.
4. وارد **Actions** شو.
5. Workflow با نام **Build APK** را انتخاب کن.
6. روی **Run workflow** بزن.
7. بعد از موفقیت، از بخش **Artifacts** فایل `khesht-apk` را دریافت کن.

Workflow با `ArtemSBulgakov/buildozer-action@v1` اجرا می‌شود و خروجی APK را از خروجی `filename` همان Action به‌عنوان Artifact ذخیره می‌کند.

## Build محلی

```bash
buildozer -v android debug
```

خروجی در پوشهٔ `bin/` ساخته می‌شود.
