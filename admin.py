import socket, os, config, atexit,threading,time
from pynput.keyboard import Key, Controller


SERVER_IP=config.SERVER_IP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP,config.SA_PORT))

killed = False

def send_input():
    global killed

    keyboard = Controller()
    while True:
        if killed == True:
            s.send(bytes("EXIT",'utf-8'))
            exit()
        message = input()
        s.send(bytes(message,'utf-8'))
        if message == "CUSTOM":
            s.send(bytes(input("Headline:\n"),'utf-8'))
            time.sleep(.1)
            s.send(bytes(input("Description:\n"),'utf-8'))


send_input_thread = threading.Thread(target=send_input)
send_input_thread.start()


def exiting():
    global killed
    killed = True
    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

atexit.register(exiting)

try:
    msg = s.recv(1024).decode('utf-8')
    if msg in config.ALERTS:
        print(msg)
    if msg == "EXIT":
        killed = True
        keyboard = Controller()
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        exit()
    if msg == 'FIRE':
        os.system('open ALERT.html')

    print("\nTo test system, enter: TEST\
           \nTo send alert, enter: FIRE\
           \nTo send a custom alert, enter: CUSTOM\
           \nTo reset the system, enter: CLEAN")

    while True:
        msg = s.recv(1024).decode('utf-8')
        if msg in config.ALERTS:
            print(msg)
        if msg == 'FIRE':
            os.system('open ALERT.html')
        if msg == 'TEST':
            os.system('open TEST.html')
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
            os.system('open CUSTOM.html')

        if msg == "EXIT":
            killed = True
            keyboard = Controller()
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            exit()
except KeyboardInterrupt:
    killed = True
    exit()
