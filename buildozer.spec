[app]

# (str) Title of your application
title = Khesht

# (str) Package name
package.name = khesht

# (str) Package domain (needed for android/ios packaging)
package.domain = studio.miogpt

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (process only files with these extensions)
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# تعیین نسخه 3.11.9 برای جلوگیری از تداخل C-API با پایتون 3.14
requirements = python3==3.11.9,kivy==2.3.0

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/icon.png

# (str) Presplash image of the application
presplash.filename = %(source.dir)s/assets/splash_logo.jpg

# (bool) Hide status bar or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 24

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept NDK license automatically
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Skip warning when buildozer is executed as root
warn_on_root = 0
