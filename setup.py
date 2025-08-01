import sys
from cx_Freeze import setup, Executable

# اطلاعات پایه برنامه
name = "Khamushi"
version = "1.0"
description = "یک دستیار هوشمند برای هشدار قطعی برق و خاموشی سیستم"
author = "Amir Asadyan"

# --- تنظیمات اصلی برای cx_Freeze ---

# تعیین اینکه برنامه گرافیکی است و نیازی به کنسول (صفحه سیاه) ندارد
# برای ویندوز از 'Win32GUI' استفاده می‌کنیم
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# تعریف فایل اجرایی اصلی برنامه
executables = [
    Executable(
        "main.py",
        base=base,
        target_name=f"{name}.exe",
        icon="icon.ico",  # <-- نکته: اینجا می‌تونی آیکون برنامه رو مشخص کنی
    )
]

# تعریف پکیج‌ها و فایل‌هایی که باید در فایل نهایی گنجانده شوند
build_exe_options = {
    "packages": ["os", "tkinter", "win10toast_click"],
    "include_files": ["icon.ico"],  # اگر فایل اضافی مثل عکس یا دیتابیس داشتی اینجا اضافه کن
    "excludes": [],
}


# --- اجرای تابع setup ---

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    options={"build_exe": build_exe_options},
    executables=executables,
)
