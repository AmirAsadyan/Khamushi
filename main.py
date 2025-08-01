import os
import datetime
import time
import tkinter as tk
from tkinter import simpledialog
from win10toast_click import ToastNotifier
import threading

# --- تنظیمات اولیه ---
toaster = ToastNotifier()

# --- توابع اصلی برنامه ---


def shutdown_computer():
    toaster.show_toast(
        title= "درحال خاموش کردن ...",
        msg="سیستم تا 1 دقیقه دیگر خاموش میشه ",
        duration=10,
        threaded=True,
    )
    os.system("shutdown /s /t 60")


def postpone_shutdown():
    toaster.show_toast(
        "به تاخیر افتاد!",
        "خیالت راحت، ۳۰ دقیقه دیگه دوباره ازت می‌پرسم.",
        duration=10,
        threaded=True,
    )

    # ۳۰ دقیقه صبر می‌کند (۱۸۰۰ ثانیه)
    time.sleep(1800)

    # بعد از ۳۰ دقیقه، دوباره همان نوتیفیکیشن را ارسال می‌کند
    send_shutdown_notification()


def send_shutdown_notification():
    # چون تابع postpone_shutdown در یک ترد جدا اجرا می‌شود،
    # باید برای هر نوتیفیکیشن یک ترد جدید ساخت.
    threading.Thread(
        target=toaster.show_toast,
        kwargs={
            "title": "!!! هشدار قطعی برق !!!",
            "msg": "قراره برق‌ها بره، فایل‌هات رو ذخیره کن! می‌خوای سیستم رو خاموش کنم؟",
            "duration": 30,  # نوتیفیکیشن ۳۰ ثانیه می‌ماند
            "threaded": False,  # این باید False باشد تا ترد اصلی منتظر بماند
            "buttons": [
                {
                    "activation_type": "callback",
                    "arguments": "yes",
                    "content": "آره، خاموش کن",
                },
                {
                    "activation_type": "callback",
                    "arguments": "no",
                    "content": "نه، ۳۰ دقیقه بعد بپرس",
                },
            ],
            "callback_on_click": {"yes": shutdown_computer, "no": postpone_shutdown},
        },
    ).start()


def get_outage_time_from_user():
    #یک پنجره برای پرسیدن زمان قطعی برق باز می‌کند
    root = tk.Tk()
    root.withdraw()  # پنجره اصلی را مخفی می‌کند

    while True:
        user_input = simpledialog.askstring(
            "زمان قطعی برق",
            "سلام ایرانی امروز برق ها کی میره 🤣 به این صورت وارد کن مثلا (14:20)",
        )

        if not user_input:  # اگر کاربر پنجره را بست
            return None

        try:
            # تبدیل ورودی به شیء زمان
            t = datetime.datetime.strptime(user_input, "%H:%M").time()
            return t
        except ValueError:
            # اگر فرمت اشتباه بود، دوباره می‌پرسد
            print("فرمت ورودی اشتباه است.")
            # اینجا می‌توان یک پیام خطا با tkinter هم نشان داد


# --- حلقه اصلی برنامه ---
if __name__ == "__main__":
    target_time = get_outage_time_from_user()

    if target_time:
        # محاسبه زمان ارسال نوتیفیکیشن (۱۰ دقیقه قبل از زمان اصلی)
        target_dt = datetime.datetime.combine(datetime.date.today(), target_time)
        notification_dt = target_dt - datetime.timedelta(minutes=10)

        print(f"زمان قطعی برق امروز: {target_time.strftime('%H:%M')}")
        print(
            f"نوتیفیکیشن هشدار در ساعت: {notification_dt.strftime('%H:%M')} ارسال خواهد شد."
        )

        # حلقه اصلی برای چک کردن زمان
        while True:
            now = datetime.datetime.now()
            if now >= notification_dt:
                send_shutdown_notification()
                # بعد از ارسال اولین نوتیفیکیشن، حلقه تمام می‌شود
                # چون بقیه منطق در توابع callback مدیریت می‌شود
                break

            # هر ۳۰ ثانیه یک بار زمان را چک می‌کند
            time.sleep(30)
    else:
        print("زمانی وارد نشد. برنامه بسته می‌شود.")
