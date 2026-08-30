# ساخت رایگان APK با GitHub (گام‌به‌گام)

## ۱) ساخت حساب
به [github.com](https://github.com) برو و ثبت‌نام کن (رایگان است).

## ۲) ساخت مخزن (Repository)
1. دکمه **New repository**
2. نام مثلاً: `khesht-game`
3. Public بگذار
4. **Create repository**

## ۳) آپلود پروژه
روش آسان با سایت:

1. داخل مخزن جدید، **uploading an existing file** را بزن
2. همه فایل‌های داخل پوشه `khesht` را بکش و رها کن  
   (حتماً پوشه `.github` هم باشد)
3. **Commit changes**

روش با Git (اگر بلدی):

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/USERNAME/khesht-game.git
git push -u origin main
```

`USERNAME` را با نام کاربری خودت عوض کن.

## ۴) اجرای بیلد
1. برو به تب **Actions**
2. workflow به اسم **Build APK** را انتخاب کن
3. **Run workflow** بزن (یا صبر کن تا با push خودش شروع شود)

اولین بیلد ممکن است **۴۵ تا ۹۰ دقیقه** طول بکشد (دانلود SDK/NDK).

## ۵) دانلود APK
1. وقتی بیلد سبز (موفق) شد، روی همان run کلیک کن
2. پایین صفحه بخش **Artifacts**
3. فایل **khesht-apk** را دانلود کن
4. از حالت zip خارج کن → فایل `.apk` را بگیر

## ۶) نصب روی گوشی
1. APK را به گوشی بفرست (تلگرام / کابل / درایو)
2. اجازه نصب از منابع ناشناس را بده
3. نصب کن

---

### نکات مهم
- گوشی‌های خیلی قدیمی (۳۲بیتی) ممکن است این APK را باز نکنند؛ این بیلد برای **arm64** است (تقریباً همه گوشی‌های چند سال اخیر)
- اگر بیلد قرمز شد، لاگ را باز کن و متن خطا را بفرست تا درستش کنیم
- Artifact حدود ۱۴ روز روی گیت‌هاب می‌ماند؛ دوباره بیلد بزن اگر پاک شد
