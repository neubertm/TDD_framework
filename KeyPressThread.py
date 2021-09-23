import threading
import readchar


class KeyboardThread(threading.Thread):
    b_keyPressed: bool

    def __init__(self):
        threading.Thread.__init__(self, name="KeyPressThread")
        self.b_keyPressed = False
        self.start()

    def run(self):
        while(True):
            int_key = readchar.readchar()
            print("KeyPress -> Finishing threads.")
            break

        self.b_keyPressed = True
        pass

    def isAnyKeyPressed(self):
        return(self.b_keyPressed)

# Next class is only for debbug purpose


class KeyboardThreadDbg():
    b_keyPressed: bool

    def __init__(self):
        self.b_keyPressed = False

    def run(self):
        pass

    def isAnyKeyPressed(self):
        return(self.b_keyPressed)
