from flask import Blueprint

import win10toast
import schedule 
import time 
 
noti = win10toast.ToastNotifier()

water_blueprint = Blueprint('water_blueprint', __name__)

@water_blueprint.route('/water')
def index():
    print('water reminder app!!')

    def waterReminder():
        print('notification')
        noti.show_toast('Time to drink water!', duration= 15)
     
     
    schedule.every(1).hour.do(waterReminder)
    while True:
        schedule.run_pending()
        time.sleep(1)

    return "water reminder"
