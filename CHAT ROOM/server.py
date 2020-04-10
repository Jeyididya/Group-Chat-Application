import socket
import threading

hosts=''
port=60555
all_clients=[] #list of all connected sockets
ip_user={} 

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((hosts,port))

def accept_connections():

    while True:
    
        global all_clients, client   
        
        client, client_adds = server.accept()  #client rcving socket object and a tuple receiving address object i.e., (ip,port)
        print(client_adds[0], " is Connected") 
        all_clients.append(client)
        
        #client.send("*WELCOME TO THE CHAT ROOM\n".encode("utf-8"))
        client.send("*Enter *QUIT* TO LEAVE THE CHAT ROOM".encode("utf-8"))
    
        t=threading.Thread(target=communication, args=(client,client_adds))
        t.start()

    return

def communication(client,client_adds):
    
    global ip_user
    
    client.send(("*ENTER YOUR NAME").encode("UTF-8"))
    x=client.recv(1024).decode("UTF-8")
    ip_user[client_adds[0]]=str(x)
    msg=str("*"+x+" HAS JOINED THE CHAT!")
    print(msg)
    print(ip_user)
    print(all_clients,"\n")
    broadcast(msg,client)

    while True:
        try:
            msg=client.recv(1024).decode("UTF-8")
            msg=str(msg)

            if(len(msg)>0):
                if(msg.lower()=="quit"):
                    leaving(client,client_adds[0])
                    break
                else:
                    print(msg)
                    msg=str(ip_user[client_adds[0]]+" >>"+msg)
                    broadcast(msg,client)    
            else: 
                return
    
        except socket.error:
            print(client, " has left ")
    
    
    
    return

def broadcast(msg,c_sender):
    try:
        for i in all_clients:
            if(i!=c_sender):
                i.send(msg.encode("UTF-8"))
                print("\nBROADCAST--->> "+msg)
            else: 
                pass
    except:
        print("NO USERS IN CHATROOM")
    return

def leaving(client,ip_leaver):
    global all_clients
    global ip_user
    msg=str("*"+ip_user[ip_leaver]+" HAS LEFT THE CHAT ROOM.")
    del all_clients[all_clients.index(client)]
    del ip_user[ip_leaver]
    broadcast(msg,client)
    client.close()
    
    return

if __name__=="__main__":
    server.listen(5)
    print("Waiting for connections......")
    accept_t=threading.Thread(target=accept_connections)
    accept_t.start()
    accept_t.join()
    server.close()