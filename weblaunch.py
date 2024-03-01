import socket
import os

HOST = "10.131.184.9"
PORT = 65432
running = True

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as connect_socket:
    connect_socket.bind((HOST,PORT))
    print(connect_socket.getsockname())
    while running:
        connect_socket.listen()
        conn, addr = connect_socket.accept()
        with conn:
            print(f"connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                sdata = data.decode()
                if sdata[0:5] == "felix":
                    sdata=sdata.split("#")
                    sdata = sdata[1]
                    print(sdata)
                    if sdata == "stop":
                        running = False
                    elif sdata == "start":
                        os.system('python bot.py')
                conn.sendall(data)