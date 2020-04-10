import socket
import time
from tkinter import *
import threading

#ADDRESS FAMILY ->> IPv4 
#PROTOCOL->> TCP

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port=60555
server='192.168.133.136'
tries=0 #AFTER TRYING 5 TIMES CLIENT IS ASKED TO WAIT AS THE SERVER MAY BE VERY BUSY
tag_name=0


def closing():
    try:
        print("CLosing")
        text_box.delete("1.0", END)
        text_box.insert("1.0 ", "quit")
        send()
        print("CLosed")
        x.destroy()
    except socket.error:
        x.destroy()
    return

def new_msg(msg=" ", by="u"):

    msg_box.config(state="normal")
    
    i1=str(msg_box.index(END))
    print("i1--->>"+i1)

    if (msg[0]=="*"):
        by="*"
        msg=msg[1:]
    else: 
        pass

    msg=str("\n"+msg)
    
    msg_box.insert(END, msg)

    i2=str(msg_box.index(END))
    print("i2--->>"+i2)
    
    global tag_name
    tag_name=int(tag_name)
    tag_name=str(tag_name+1)

    msg_box.tag_add(tag_name, i1, i2)
        
    if (by == "i"):
        
        msg_box.tag_configure(tag_name, background= "#FF303F", justify="right")
    
    elif (by == "u"):
        
        msg_box.tag_configure(tag_name, background= "#4BBCC3", justify="left")
    
    elif (by == "*"):
        
        msg_box.tag_configure(tag_name, background= "#FB800B", justify="center")
    
    else:
        
        pass

    msg_box.config(state="disabled")
    
    return

def connect():
    
    global tries
    
    try:

        if tries==5:
            
            msg="Server Is Busy! "+"\n"+"Please Try Again Later."
            print(msg)
            new_msg("*"+msg)
            text_box.insert(END, "CLOSE AND TRY AGAIN Later!")
            text_box.config(state="disabled")
            sendB.config(state="disabled")

            return

        else:

            client.connect((server, port))
            t=threading.Thread(target=connection)
            t.start()

    except socket.error:
        
        tries+=1
        connect()


def connection():	
    
    flag=True
    while flag:
        try:
            print("Coonection Function Start")
            msg = client.recv(1024)
            msg=msg.decode("utf-8")
            new_msg(msg)

            print(msg)
        
        except:
            flag=False

def send():

    msg= text_box.get(1.0, END)
    msg=msg.strip()
    text_box.delete(1.0, END)

    if len(msg)==0:
        return

    elif msg.lower()=="quit":

        print(client, "leaving")
        client.send(msg.encode("UTF-8"))
        new_msg("*BYE BYE! \n Thank you.")
        text_box.config(state="disabled")
        sendB.config(state="disabled")
        client.close()
        #x.quit()
        return

    else: 
        
        new_msg("YOU >>"+msg+"  ","i")
        client.sendall(msg.encode("UTF-8"))
        return



class MainWindow(Tk):

    def __init__(self, title, len, bre):
    
        super().__init__()
        self.geometry(str(len)+"x"+str(bre))
        self['bg']="#1ABC9C"
        self.title(title)

x=MainWindow("BOOM CHATTER", 1224, 520)

head=Label(x,  bg="#2C3E50",  fg="#ECF0F1",  text="BOOM CHAT ROOM",  font="impact 40 bold underline", pady="0.3c")
head.grid(row=0,  column=0,  columnspan=2,  sticky="nsew")


f=Frame(x)
f.grid(row=1, column=0, columnspan=2, sticky="nsew")
msg_box=Text(f,  bg="#F1C40F",  fg="#ECF0F1",  font="impact 20 italic",  height=10,  width=86)
msg_box.pack(fill="x", side="left")
#msg_box.grid(row=1, column=0, columnspan=2, sticky="nsew")
#f.pack_propagate(False)
scroll=Scrollbar(f, command=msg_box.yview, orient="vertical")
msg_box['yscrollcommand']=scroll.set

scroll.pack(fill="y", side="right")

text_box=Text(x,  bg="#95A5A6",  fg="#ECF0F1",  font="impact 20 italic",  height=2, width=70)
text_box.grid(row=2, column=0, sticky="nsew")

sendB=Button(x,  bg="#1ABC9C",  fg="#ECF0F1",  text="SEND",  font="impact 30 italic", padx=1, command=send)
sendB.grid(row=2, column=1, sticky="nsew")

x.protocol("WM_DELETE_WINDOW", closing)


if __name__=="__main__":
    connect()

x.mainloop()
