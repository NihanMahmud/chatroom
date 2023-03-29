import socket
import threading

HEADER=24
servername=input("Enter Server Name : ")
PORT=int(input("Enter PORT NUMBER : "))
mainserver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ADDRESS=(servername,PORT)
FORMAT='utf-8'
DISCONNET="!DISCONNECT"

client= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)
print(f"CONNECTED WITH {servername}!")

MESSAGES=client.recv(2048).decode(FORMAT)

CONNECTED=True

def sendtoserver(msg):
    msg=f"{NICKNAME} : {msg}"
    client.send(msg.encode(FORMAT))
def receivemsg():
    while CONNECTED:
        msg=client.recv(2048).decode(FORMAT)
        if msg:
            print(f"{msg}")

def fixname(NICKNAME):
    while True:
        client.send(NICKNAME.encode(FORMAT))
        msg=client.recv(1024).decode()
        if msg=="INVALID":
            print("NICKNAME TAKEN : Try a different nickname")
            return False
        elif msg=="SUCCESSFULL!":
            return True
        else:
            pass


while True:
    NICKNAME=input("Your nickname : ")
    if True==fixname(NICKNAME):
        break

print(MESSAGES)
client.send(f"{NICKNAME} has CONNECTED!".encode(FORMAT))

threading.Thread(target=receivemsg).start()

while CONNECTED:
    msg=input()
    if msg==DISCONNET:
        client.send(f"{NICKNAME} has DISCONNECTED!".encode(FORMAT))
        client.send("!DISCONNECT".encode(FORMAT))
        CONNECTED=False
        break
    sendtoserver(msg)
