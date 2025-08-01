import os
import datetime
from plyer import notification

now = datetime.datetime.now()
current_time = now.strftime("%H:%M")
notification.notify(
    title=" سلام ایرانی ! ",
    message=f"ساعت  {current_time} است",
    timeout=5
)


