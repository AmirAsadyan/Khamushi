import os
import datetime
import time
import tkinter as tk
from tkinter import simpledialog
import sys
import logging

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


def cancel_shutdown_process():
    """کل فرآیند خاموشی را برای امروز لغو می‌کند."""
    notification = Notification(
        app_id="Khamushi",
        title="عملیات لغو شد",
        msg="فرآیند خاموشی برای امروز به طور کامل لغو شد.",
        duration="short",
    )
    notification.show()
    # برنامه به طور طبیعی تمام می‌شود


# ===== این تابع جدید برای ساخت پنجره سفارشی است =====
def ask_shutdown_options():
    """یک پنجره سفارشی با سه دکمه برای تصمیم‌گیری کاربر باز می‌کند."""
    root = tk.Tk()
    root.title("!!! هشدار قطعی برق !!!")
    root.geometry("350x120")
    root.resizable(False, False)

    # متغیر برای نگهداری جواب کاربر
    user_choice = tk.StringVar()
    user_choice.set("")  # مقدار اولیه

    def set_choice_and_close(choice):
        user_choice.set(choice)
        root.destroy()

    label = tk.Label(
        root,
        text="قراره برق‌ها بره، فایل‌هات رو ذخیره کن!\n\nمی‌خوای سیستم رو خاموش کنم؟",
        pady=10,
    )
    label.pack()

    frame = tk.Frame(root)
    frame.pack(pady=5)

    btn_yes = tk.Button(
        frame,
        text="آره، خاموش کن",
        width=15,
        command=lambda: set_choice_and_close("yes"),
    )
    btn_yes.pack(side=tk.LEFT, padx=5)

    btn_postpone = tk.Button(
        frame,
        text="نه، ۳۰ دقیقه بعد",
        width=15,
        command=lambda: set_choice_and_close("postpone"),
    )
    btn_postpone.pack(side=tk.LEFT, padx=5)

    btn_cancel = tk.Button(
        frame, text="لغو کامل", width=15, command=lambda: set_choice_and_close("cancel")
    )
    btn_cancel.pack(side=tk.LEFT, padx=5)

    # این تابع پنجره را تا زمانی که بسته شود، نگه می‌دارد
    root.mainloop()
    return user_choice.get()


# ===== این تابع برای استفاده از پنجره جدید اصلاح شد =====
def send_shutdown_notification():
    """پرسیدن سوال خاموشی از طریق پنجره سفارشی"""
    answer = ask_shutdown_options()

    if answer == "yes":
        shutdown_computer()
    elif answer == "postpone":
        postpone_shutdown()
    elif answer == "cancel":
        cancel_shutdown_process()
    # اگر کاربر پنجره را ببندد، هیچ کاری انجام نمی‌شود


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
