import socket, os, config, atexit, time, threading
from sys import platform


SERVER_IP=config.SERVER_IP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP,config.SC_PORT))

killed = False

def reconnect(s):
    global killed
    while True:
        for i in range(int(config.RECONNECT_DELAY*60*10)):
            if killed:
                try: 
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
                except:
                    pass
                return
            time.sleep(.1)

        s.send(bytes("EXIT",'utf-8'))
        time.sleep(.1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP,config.SC_PORT))

threading.Thread(target=reconnect, args=[s]).start()

def exiting():
    global killed
    killed = True
    # s.shutdown(socket.SHUT_RDWR)
    # s.close()

atexit.register(exiting)
msg = s.recv(1024).decode('utf-8')
print(msg)
try:
    while True:
        try:
            msg = s.recv(1024).decode('utf-8')
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

            if msg == 'EXIT':
                killed = True
                s.send(bytes("EXIT",'utf-8'))
                exit()

        except OSError:
            pass

except KeyboardInterrupt:
    killed = True
    s.send(bytes("EXIT",'utf-8'))
    exit()
