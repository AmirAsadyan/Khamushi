import os
import datetime
import time
import tkinter as tk
import sys
import logging
from tkinter import simpledialog

# پیکربندی لاگ برای حالت noconsole
logging.basicConfig(
    filename="power_alert.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# تلاش برای بارگذاری ToastNotifier
try:
    from win10toast_click import ToastNotifier
except ImportError:
    logging.error("کتابخانه win10toast_click نصب نشده است.")
    raise ImportError(
        "کتابخانه win10toast_click نصب نشده است. با دستور 'pip install win10toast_click' نصب کنید."
    )

# ایجاد شیء toaster
toaster = ToastNotifier()


# تابع کمکی برای نمایش نوتیفیکیشن
def show_notification(title, msg, duration=10, buttons=None, callback_on_click=None):
    try:
        toaster.show_toast(
            title=title,
            msg=msg,
            duration=duration,
            threaded=True,
            buttons=buttons,
            callback_on_click=callback_on_click,
        )
    except Exception as e:
        logging.error(f"خطا در نمایش نوتیفیکیشن '{title}': {e}")


# خاموش کردن سیستم
def shutdown_computer():
    show_notification("درحال خاموش کردن ...", "سیستم تا 1 دقیقه دیگر خاموش میشه", 10)
    os.system("shutdown /s /t 60")


# به تأخیر انداختن خاموشی
def postpone_shutdown():
    show_notification(
        "به تاخیر افتاد!", "خیالت راحت، ۳۰ دقیقه دیگه دوباره ازت می‌پرسم.", 10
    )
    time.sleep(1800)
    send_shutdown_notification()


# ارسال نوتیفیکیشن هشدار
def send_shutdown_notification():
    buttons = [
        {"activation_type": "callback", "arguments": "yes", "content": "آره، خاموش کن"},
        {
            "activation_type": "callback",
            "arguments": "no",
            "content": "نه، ۳۰ دقیقه بعد بپرس",
        },
    ]
    callbacks = {"yes": shutdown_computer, "no": postpone_shutdown}
    show_notification(
        "!!! هشدار قطعی برق !!!",
        "قراره برق‌ها بره، فایل‌هات رو ذخیره کن! می‌خوای سیستم رو خاموش کنم؟",
        duration=30,
        buttons=buttons,
        callback_on_click=callbacks,
    )


# دریافت زمان قطعی برق از کاربر
def get_outage_time_from_user():
    root = tk.Tk()
    root.withdraw()
    while True:
        user_input = simpledialog.askstring(
            "زمان قطعی برق",
            "سلام ایرانی امروز برق ها کی میره 🤣 به این صورت وارد کن مثلا (14:20)",
        )
        if user_input is None:
            root.destroy()
            return None
        try:
            t = datetime.datetime.strptime(user_input, "%H:%M").time()
            root.destroy()
            return t
        except ValueError:
            show_notification(
                "خطا در فرمت", "فرمت ساعت اشتباه بود، لطفا دوباره تلاش کن.", 5
            )


# تابع اصلی
def main():
    target_time = get_outage_time_from_user()
    if not target_time:
        show_notification("خطا", "زمانی وارد نشد. برنامه بسته می‌شود.", 5)
        time.sleep(5)
        sys.exit()

    target_dt = datetime.datetime.combine(datetime.date.today(), target_time)
    notification_dt = target_dt - datetime.timedelta(minutes=10)

    show_notification(
        "زمان با موفقیت تنظیم شد",
        f"زمان قطعی برق: {target_time.strftime('%H:%M')}\nهشدار در ساعت {notification_dt.strftime('%H:%M')} ارسال می‌شود.",
        10,
    )

    while True:
        now = datetime.datetime.now()
        if now >= notification_dt:
            send_shutdown_notification()
            break
        time.sleep(30)


# اجرای برنامه
if __name__ == "__main__":
    main()
