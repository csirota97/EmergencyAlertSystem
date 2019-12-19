import socket, os, config, atexit,threading
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
    if msg != "EXIT":
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
           \nTo send alert, enter: FIRE")

    while True:
        msg = s.recv(1024).decode('utf-8')
        if msg != "EXIT" or msg == "":
            print(msg)
        if msg == 'FIRE':
            os.system('open ALERT.html')
        if msg == 'TEST':
            os.system('open TEST.html')
        if msg == "EXIT":
            killed = True
            keyboard = Controller()
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            exit()
except KeyboardInterrupt:
    killed = True
    exit()
