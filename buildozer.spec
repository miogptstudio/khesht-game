[app]

title = Khesht
package.name = khesht
package.domain = studio.miogpt

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf
source.include_patterns = assets/*

version = 1.0.1

requirements = python3==3.11.5,hostpython3==3.11.5,kivy==2.3.0

orientation = portrait

icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/splash_logo.jpg

fullscreen = 0

android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a,x86,x86_64

# Pin python-for-android to the release whose recipes default to Python 3.11.5
p4a.branch = v2024.01.21


[buildozer]
log_level = 2
warn_on_root = 0
