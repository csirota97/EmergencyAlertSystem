import socket, os, config, atexit,threading,time
from sys import platform
from pynput.keyboard import Key, Controller


SERVER_IP=config.SERVER_IP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP,config.SA_PORT))

killed = False
new_message = None

def input_loop():
    global killed, new_message

    while not killed:
        new_message = input()

def send_input():
    global killed, new_message

    keyboard = Controller()

    threading.Thread(target=input_loop).start()

    while True:
        if killed == True:
            s.send(bytes("EXIT",'utf-8'))
            exit()
        if new_message != None:
            s.send(bytes(new_message,'utf-8'))
            if new_message == "CUSTOM":
                s.send(bytes(input("Headline:\n"),'utf-8'))
                time.sleep(.1)
                s.send(bytes(input("Description:\n"),'utf-8'))
            new_message = None



send_input_thread = threading.Thread(target=send_input)
send_input_thread.start()


def exiting():
    global killed
    killed = True
    keyboard = Controller()
    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)

atexit.register(exiting)

try:
    msg = s.recv(1024).decode('utf-8')
    if msg in config.ALERTS:
        print(msg)
    if msg == "EXIT":
        killed = True
        print("BALLSSSS")
        keyboard = Controller()
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        exit()
    if msg == 'FIRE':
        if platform == "linux" or platform == "linux2":
            # linux
            os.system("xdg-open \"\" ALERT.html")
        elif platform == "darwin":
            os.system('open ALERT.html')
            # OS X
        elif platform == "win32":
            # Windows...
            os.system("start \"\" ALERT.html    ")

    print("\nTo test system, enter: TEST\
           \nTo send alert, enter: FIRE\
           \nTo send a custom alert, enter: CUSTOM\
           \nTo reset the system, enter: CLEAN")

    while True:
        msg = s.recv(1024).decode('utf-8')
        if msg in config.ALERTS:
            print(msg)
        if msg == 'FIRE':
            if platform == "linux" or platform == "linux2":
                # linux
                os.system("xdg-open \"\" ALERT.html")
            elif platform == "darwin":
                os.system('open ALERT.html')
                # OS X
            elif platform == "win32":
                # Windows...
                os.system("start \"\" ALERT.html    ")

        if msg == 'TEST':
            if platform == "linux" or platform == "linux2":
                # linux
                os.system("xdg-open \"\" TEST.html")
            elif platform == "darwin":
                os.system('open TEST.html')
                # OS X
            elif platform == "win32":
                # Windows...
                os.system("start \"\" TEST.html    ")
        if msg[0:6] == 'CUSTOM':
            components = msg.split(']#[')
            name = components[1]
            desc = components[2]
            print(name)
            print(desc)
            f = open("CUSTOM.html", 'w')
            f.write(
                f"<!DOCTYPE html>\n\
                <html>\n\
                \t\t<head>\n\
                \t\t<title>{name}</title>\n\
                \t\t<link rel=\"stylesheet\" type=\"text/css\" href=\"ALERT.css\">\n\
                \t</head>\n\
                \t<body>\n\
                \t\t<div class=\"alert\">{name}</div>\n\
                \t\t<div class=\"alert_message\">{desc}</div>\n\
                \t</body>\
                </html>")
            f.close()
            if platform == "linux" or platform == "linux2":
                # linux
                os.system("xdg-open \"\" CUSTOM.html")
            elif platform == "darwin":
                os.system('open CUSTOM.html')
                # OS X
            elif platform == "win32":
                # Windows...
                os.system("start \"\" CUSTOM.html    ")

        if msg == "EXIT":
            killed = True
            keyboard = Controller()
            keyboard.press(Key.enter)
            time.sleep(0.1)
            keyboard.release(Key.enter)
            exit()
except KeyboardInterrupt:
    killed = True
    exit()
