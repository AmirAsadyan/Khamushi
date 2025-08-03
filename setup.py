import sys
from cx_Freeze import setup, Executable

# اطلاعات پایه برنامه
name = "Khamushi"
version = "1.0"
description = "یک دستیار هوشمند برای هشدار قطعی برق و خاموشی سیستم"
author = "Amir Asadyan"

# --- تنظیمات اصلی برای cx_Freeze ---

# تعیین اینکه برنامه گرافیکی است و نیازی به کنسول (صفحه سیاه) ندارد
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# تعریف فایل اجرایی اصلی برنامه
executables = [
    Executable(
        "main.py",
        base=base,
        target_name=f"{name}.exe",
        icon="icon.ico",
    )
]

# تعریف پکیج‌ها و فایل‌هایی که باید در فایل نهایی گنجانده شوند
build_exe_options = {
    "packages": ["os", "tkinter", "winotify"],
    "include_files": ["icon.ico"],
    "excludes": [],
}

# ===== این بخش برای درخواست دسترسی ادمین اضافه شده است =====
bdist_msi_options = {
    # با True کردن این گزینه، نصب برای تمام کاربران فعال می‌شود
    # و به طور خودکار درخواست دسترسی ادمین (UAC) می‌کند.
    "all_users": True,
}
# ==========================================================


# --- اجرای تابع setup ---
setup(
    name=name,
    version=version,
    description=description,
    author=author,
    # در اینجا آپشن جدید را به setup اضافه می‌کنیم
    options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
    executables=executables,
)