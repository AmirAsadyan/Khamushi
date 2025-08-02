import os
import datetime
import time
import tkinter as tk
import tkinter.messagebox as msgbox
import sys
import logging
from tkinter import simpledialog

# پیکربندی لاگ برای حالت noconsole
logging.basicConfig(
    filename="power_alert.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

try:
    from winotify import Notification
except ImportError:
    logging.error("کتابخانه winotify نصب نشده است.")
    raise ImportError(
        "کتابخانه winotify نصب نشده است. با دستور 'pip install winotify' نصب کنید."
    )

# --- توابع اصلی برنامه ---


def shutdown_computer():
    """کامپیوتر را با تاخیر ۱ دقیقه‌ای خاموش می‌کند"""
    notification = Notification(
        app_id="Khamushi",
        title="درحال خاموش کردن ...",
        msg="سیستم تا 1 دقیقه دیگر خاموش میشه",
        duration="short",
    )
    notification.show()
    os.system("shutdown /s /t 60")


def postpone_shutdown():
    """خاموشی را ۳۰ دقیقه به تاخیر می‌اندازد و دوباره سوال می‌پرسد"""
    notification = Notification(
        app_id="Khamushi",
        title="به تاخیر افتاد!",
        msg="خیالت راحت، ۳۰ دقیقه دیگه دوباره ازت می‌پرسم.",
        duration="short",
    )
    notification.show()
    time.sleep(1800)
    send_shutdown_notification()


def send_shutdown_notification():
    """پرسیدن سوال خاموشی از طریق پنجره گرافیکی"""
    root = tk.Tk()
    root.withdraw()
    answer = msgbox.askyesno(
        "!!! هشدار قطعی برق !!!",
        "قراره برق‌ها بره، فایل‌هات رو ذخیره کن!\n\nمی‌خوای سیستم رو خاموش کنم؟",
    )
    root.destroy()

    if answer:
        shutdown_computer()
    else:
        postpone_shutdown()


def get_outage_time_from_user():
    """یک پنجره برای پرسیدن زمان قطعی برق باز می‌کند"""
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askstring(
        "زمان قطعی برق",
        "سلام ایرانی امروز برق ها کی میره 🤣 به این صورت وارد کن مثلا (14:20)",
    )
    root.destroy()

    if user_input:
        try:
            return datetime.datetime.strptime(user_input, "%H:%M").time()
        except ValueError:
            error_notification = Notification(
                app_id="Khamushi",
                title="خطا در فرمت",
                msg="فرمت ساعت اشتباه بود، برنامه بسته می‌شود.",
                duration="short",
            )
            error_notification.show()
            return None
    return None


# تابع اصلی
def main():
    target_time = get_outage_time_from_user()
    if not target_time:
        sys.exit()

    target_dt = datetime.datetime.combine(datetime.date.today(), target_time)
    notification_dt = target_dt - datetime.timedelta(minutes=10)

    success_notification = Notification(
        app_id="Khamushi",
        title="زمان با موفقیت تنظیم شد",
        msg=f"زمان قطعی برق: {target_time.strftime('%H:%M')}\nهشدار در ساعت {notification_dt.strftime('%H:%M')} ارسال می‌شود.",
        duration="short",
    )
    success_notification.show()

    while True:
        now = datetime.datetime.now()
        if now >= notification_dt:
            send_shutdown_notification()
            break
        time.sleep(30)


# اجرای برنامه
if __name__ == "__main__":
    main()
