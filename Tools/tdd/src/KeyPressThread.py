import os
import threading

# Windows
if os.name == 'nt':
    import msvcrt

# Posix
else:
    import sys
    import termios
    import atexit
    from select import select



class KeyboardThread(threading.Thread):
    b_keyPressed: bool

    def __init__(self):
        threading.Thread.__init__(self, name="KeyPressThread")
        self.b_keyPressed = False

        if os.name == 'nt':
            pass
        else:
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)

        self.start()

    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')

        else:
            return sys.stdin.read(1)

    def run(self):
        while(True):
            #int_key = readchar.readchar()
            if self.getch():
                print("KeyPress -> Finishing threads.")
                break

        self.b_keyPressed = True
        self.set_normal_term()

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
