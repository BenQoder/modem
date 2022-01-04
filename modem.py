import huaweisms.api.user
import huaweisms.api.wlan
import huaweisms.api.sms
import huaweisms.api.device
import rumps
import time
import re

phone_number_window = rumps.Window(title="Phone Number", ok="Continue", cancel="Cancel", dimensions=(200, 40))
amount_window = rumps.Window(title="Enter Amount (500 or Below)", ok="Send Data", cancel="Cancel", dimensions=(200, 40))

class MyModemStatusBarTools(rumps.App):
    def __init__(self):
        super(MyModemStatusBarTools, self).__init__("My Tools")
        self.menu = ["Check Data Balance", "Send Data", "Send Quick Data To Self", " ", "Reboot Device"]

    @rumps.clicked("Check Data Balance")
    def check_data_balance(self, _):
        ctx = huaweisms.api.user.quick_login("admin", "admin")
        send_sms = huaweisms.api.sms.send_sms(ctx, ["131"], "2")

        time.sleep(1)
        latest_sms = huaweisms.api.sms.get_sms(ctx, qty=1)
        message = latest_sms["response"]["Messages"]["Message"][0]

        while message["Phone"] != "131":
            time.sleep(1)

            latest_sms = huaweisms.api.sms.get_sms(ctx, qty=1)
            message = latest_sms["response"]["Messages"]["Message"][0]

        balance = re.search("balance:\n(.*)\n", message["Content"]).group(1)
        
        rumps.notification("Data Balance", " ", balance)

    @rumps.clicked("Send Data")
    def send_data(self, _):

        phone_number = phone_number_window.run()

        if len(phone_number.text) != 11 or phone_number.clicked == 0:
            rumps.notification("Error", " ", "Cancelled By User or Invalid Phone Number")
            return

        amount = amount_window.run()

        if int(amount.text) > 500 or amount.clicked == 0:
            rumps.notification("Error", " ", "Cancelled By User or Amount must be less than 500")
            return

        ctx = huaweisms.api.user.quick_login("admin", "admin")
        
        send_sms = huaweisms.api.sms.send_sms(ctx, ["131"], "Transfer {} {}".format(phone_number.text, amount.text))
        time.sleep(2)
        send_sms = huaweisms.api.sms.send_sms(ctx, ["131"], "Yes")
        
        rumps.notification("Transfer Successful", " ", "{}MB Data Transfer To {} Successful".format(int(amount.text), phone_number.text))

    @rumps.clicked("Send Quick Data To Self")
    def send_data_to_self(self, _):

        phone_number = "07035082751"

        amount = 200
        ctx = huaweisms.api.user.quick_login("admin", "admin")
        
        send_sms = huaweisms.api.sms.send_sms(ctx, ["131"], "Transfer {} {}".format(phone_number, amount))
        time.sleep(2)
        send_sms = huaweisms.api.sms.send_sms(ctx, ["131"], "Yes")
        
        rumps.notification("Transfer Successful", " ", "{}MB Data Transfer To {} Successful".format(int(amount), phone_number))

    @rumps.clicked("Reboot Device")
    def send_data_to_self(self, _):

        ctx = huaweisms.api.user.quick_login("admin", "admin")
        
        rumps.notification("Transfer Successful", " ", "{}MB Data Transfer To {} Successful".format(int(amount), phone_number))
if __name__ == "__main__":
    MyModemStatusBarTools().run()