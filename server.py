import socket, threading, time, config, atexit

client_ips=[]
admin_ips=[]
threads = []

alerts = config.ALERTS

host = config.SERVER_IP
client_port=config.SC_PORT
admin_port=config.SA_PORT

client_in_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_in_socket.bind((host,client_port))
client_in_socket.listen(10)


admin_in_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
admin_in_socket.bind((host,admin_port))
admin_in_socket.listen(10)



print("\033[1;34;40m----------------\n Server Started\n----------------")

def exiting(client):
    try:
        while client[0].recv(1024).decode('utf-8') != "EXIT":
            pass
    except OSError:
        return
    client_ips.remove(client)
    client[0].shutdown(socket.SHUT_RDWR)
    client[0].close()
    print("\033[1;31;40mClient has disconnected")
    print (client_ips)


def accepting():
    while True:
        client_side_socket, client_ip = client_in_socket.accept()
        client_ips.append((client_side_socket, client_ip))
        print(f'\033[1;32;40mConnection from {client_ip} has been established')
        threading.Thread(target=exiting,args=[(client_side_socket, client_ip)]).start()
        client_side_socket.send(bytes("Welcome To The Emergency Alert System", 'utf-8'))
        time.sleep(.2)

def admin_exiting(client):
    global client_ips
    print("\033[1;34;40mEXIT THREAD RUNNING")
    msg=client[0].recv(1024).decode('utf-8')
    out=False
    while msg != "EXIT":
        if msg in alerts:
            ALERT(client,msg)
        if msg == "CLEAN":
            out = True
            for c in client_ips:
                if c[1] != client[1]:
                    try:
                        c[0].send(bytes("EXIT",'utf-8'))
                    except:
                        pass
                    try:
                        admin_ips.remove(c)
                    except:
                        pass
                    try:
                        c[0].shutdown(socket.SHUT_RDWR)
                        c[0].close()
                    except:
                        pass


        if out:
            client_ips = []
            break
        print("\033[1;33;40mPING")
        msg=client[0].recv(1024).decode('utf-8')

    client[0].send(bytes("EXIT",'utf-8'))
    try:
        admin_ips.remove(client)
    except:
        pass
    try:
        client_ips.remove(client)
    except:
        pass
    client[0].shutdown(socket.SHUT_RDWR)
    client[0].close()
    if msg == "CLEAN":

        print("\033[1;31;40mAll Clients Disconnected")
        print (client_ips)
        print("\033[1;31;40mAll Admins Disconnected")
        print (admin_ips)
        return
    else:

        print("\033[1;31;40mAdmin has disconnected")
        print (admin_ips)

def admin_accepting():
    while True:
        client_side_socket, client_ip = admin_in_socket.accept()
        client_ips.append((client_side_socket, client_ip))
        admin_ips.append((client_side_socket, client_ip))
        print(f'\033[1;32;40mConnection from {client_ip} has been established')
        threading.Thread(target=admin_exiting,args=[(client_side_socket, client_ip)]).start()
        client_side_socket.send(bytes("Welcome To The Emergency Alert System", 'utf-8'))
        time.sleep(.2)




accept_clients = threading.Thread(target=accepting)
accept_clients.start()
accept_admins = threading.Thread(target=admin_accepting)
accept_admins.start()
def ALERT(admin, alert):
    print("\033[1;34;40mALERT THREAD RUNNING")
    if alert == "CUSTOM":
        admin[0].send(bytes("recv","utf-8"))
        name = admin[0].recv(1024).decode('utf-8')
        admin[0].send(bytes("recv","utf-8"))
        desc = admin[0].recv(1024).decode('utf-8')
        admin[0].send(bytes("recv","utf-8"))
        print(name)
        print(desc)
    for client in client_ips:
        try:
            if alert == "CUSTOM":
                delim = ']#['
                client[0].send(bytes(alert+delim+name+delim+desc,"utf-8"))
            else:
                client[0].send(bytes(alert,"utf-8"))
        except BrokenPipeLineError:
            print(f"Could not send")
    print("DONE")

