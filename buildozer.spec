[app]

title = Cuidadora Bariatrica
package.name = cuidadorabariatrica
package.domain = org.johann

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

source.exclude_dirs = venv,__pycache__,bin,.buildozer

version = 0.1

requirements = python3,kivy==2.3.1,kivymd==1.2.0,plyer,pillow

orientation = portrait

fullscreen = 0

android.permissions = POST_NOTIFICATIONS,VIBRATE

android.api = 35
android.minapi = 23
android.ndk = 25b

android.archs = arm64-v8a


log_level = 2

warn_on_root = 1
