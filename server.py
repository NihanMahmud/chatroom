import socket 
import threading

HEADER = 24
PORT = 60000
servername="127.0.0.1" 
# so basically this server is used for localhost, but if you want to use in the web you can use ngrok!

ADDRESS=(servername,PORT)
FORMAT='utf-8'
DISCONNET="!DISCONNECT"

MESSAGES = "MESSAGES : \n"
# all the messages will be stored here so that if anyone joins, he can read previous message

mainserver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mainserver.bind(ADDRESS)

CONNECTIONS = []
NICKNAMES = []
DIC = {}

def handle_client(con,addr):

    global MESSAGES
    con.send(MESSAGES.encode(FORMAT))

    print(f"[{addr}] CONNECTED")
    while True:
        nickname=con.recv(HEADER).decode(FORMAT)
        if nickname in NICKNAMES:
            con.send("INVALID".encode(FORMAT))
        else:
            con.send("SUCCESSFULL!".encode(FORMAT))
            NICKNAMES.append(nickname)
            DIC[addr[1]]=nickname
            break
    
    CONNECTIONS.append(con)

    connected=True
    while connected:
        try:
            msg=con.recv(2048).decode(FORMAT)
            if msg:
                if msg == DISCONNET:
                    connected=False                
                    con.close()
                    CONNECTIONS.remove(con)
                    for cons in CONNECTIONS:
                        msg=f"{DIC[addr[1]]} has disconnected"
                        cons.send(msg.encode(FORMAT))    
                    NICKNAMES.remove(DIC[addr[1]])
                    print(f"[{addr}] : DISCONNECTED!")
                else:
                    MESSAGES = MESSAGES + msg + '\n'
                    for cons in CONNECTIONS:
                        if cons!=con:
                            cons.send(msg.encode(FORMAT))    

        except:
                connected=False                
                con.close()
                CONNECTIONS.remove(con)
                for cons in CONNECTIONS:
                    cons.send(f"{DIC[addr[1]]} has DISCONNECTED".encode(FORMAT)) 
                NICKNAMES.remove(DIC[addr[1]])
                print(f"[{addr}] : DISCONNECTED!")

def start():
    mainserver.listen()
    print(f"LISTENING ON {servername} ")
    while True:
        con,addr=mainserver.accept()
        thread=threading.Thread(target=handle_client,args=(con,addr))
        thread.start()
        print(f"[{threading.activeCount() -1}] are CONNECTED right now!")

start()