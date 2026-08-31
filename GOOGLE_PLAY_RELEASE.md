# Khesht — Google Play release

## وضعیت انتشار

این نسخه برای Google Play آماده‌سازی شده و تنظیمات انتشار آن شامل:

- Target API 36 (Android 16)
- Minimum API 24 (Android 7.0)
- NDK 28c
- python-for-android v2026.05.09
- Kivy 2.3.0
- arm64-v8a, armeabi-v7a, x86, x86_64
- خروجی اصلی: Android App Bundle (`.aab`)

Google Play از 31 August 2026 برای برنامه‌های جدید و به‌روزرسانی‌ها Target API 36 یا بالاتر را می‌خواهد.

## ساخت

در GitHub Actions workflow با نام **Build Khesht Release (Google Play)** را اجرا کن، یا یک tag مثل `v1.0.3` push کن.

خروجی را از قسمت **Artifacts** با نام `khesht-google-play-release` بردار.

## امضای برنامه

برای انتشار واقعی، کلید upload را گم نکن.

### روش پیشنهادی

در Repository Settings → Secrets and variables → Actions این چهار Secret را تنظیم کن:

- `KHESHT_KEYSTORE_B64`
- `KHESHT_KEYSTORE_PASSWORD`
- `KHESHT_KEY_ALIAS`
- `KHESHT_KEY_PASSWORD`

اگر Secretها تنظیم نشده باشند، workflow برای اولین build یک upload key موقت می‌سازد و آن را در artifact جداگانه قرار می‌دهد. آن فایل را دانلود و در جای امن نگهداری کن؛ برای نسخه‌های بعدی باید همان کلید را دوباره استفاده کنی.

## ساخت صفحه Google Play

اطلاعات لازم:

- نام: Khesht
- دسته: Game
- آیکون: `assets/icon.png`
- توضیح کوتاه: یک بازی مهارتی هشت‌مرحله‌ای با موانع متحرک و سختی افزایشی.
- توضیح کامل: در این بازی کنترل شخصیت را در اختیار بگیر، از موانع عبور کن و هر ۸ مرحله را پشت سر بگذار. هر مرحله سخت‌تر از قبلی است و به واکنش سریع و زمان‌بندی دقیق نیاز دارد.

قبل از ارسال، اسکرین‌شات‌های واقعی از نسخه نهایی بازی تهیه و در Play Console اضافه کن.

## اطلاعاتی که باید در Play Console تکمیل شوند

- App access
- Ads declaration
- Target audience and content
- Data safety
- Content rating
- Privacy policy، در صورت نیاز بر اساس رفتار واقعی برنامه
- Store listing
- App category

این موارد را باید مطابق رفتار واقعی Khesht پاسخ بده؛ چیزی را که بازی واقعاً جمع‌آوری یا استفاده نمی‌کند اعلام نکن.

## تست قبل از Production

اگر حساب توسعه‌دهنده شخصی جدید مشمول الزامات تست Google Play باشد، باید Closed testing را انجام دهی. طبق راهنمای فعلی Google، برای این حساب‌ها حداقل ۱۲ تستر باید ۱۴ روز پیوسته در تست بسته opt-in باشند، سپس می‌توان درخواست دسترسی Production داد.
