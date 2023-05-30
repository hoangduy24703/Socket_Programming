import socket
import threading
import json

try:
    file = open("menu.txt", mode ='r', encoding='utf-8')
    menu = file.read()    
finally:
    file.close()

Line = []
Line = menu.split("\n")

def Price(menu,food):
    Line = []
    Line = menu.split("\n")
    Line.pop(0)
    orderList = []

    for i in range(0,len(Line)):
        Line[i]=" ".join(Line[i].split())
    i = 0

    while len(Line)-1 > i:
        orderList.append ([])
        orderList[i] = Line[i].split(" ")
    
        tmp = []
        tmp = orderList[i][0].split("-")
        orderList[i][0] = tmp[1]

        tmp = []    
        tmp = orderList[i][1].split("$")
        orderList[i][1] = tmp[0]
        
        i+=1
        
    i = 0
    while food != orderList[i][0]:
        i+=1
    
    return int(orderList[i][1])
def Bill(req):
    Line = []
    Line = req.split("\n")
    orderList = []

    i = 0
    while True:
        orderList.append([])
        orderList[i] = Line[i].split(" ")
        if orderList[i][0] == "end":
            break
        i+=1
        
    bill = 0
    j = 0
    
    for j in range(0,i):
        bill += (Price(menu,orderList[j][0])*int(orderList[j][1]))
    
    return "Bill: " + str(bill) + "$."
def sendImg(name,client):
    try:
        file = open(name,"rb")
        img_data = file.read(1024)

        while img_data:
            client.sendall(bytes(img_data))
            img_data = file.read(1024)
    except:
        file.close()
def sendImgSteps(name):
    try:
        file = open(name,"rb")
        img_data = file.read(1024)
        steps = -1 
        while img_data:
            steps+=1
            img_data = file.read(1024)
    except:
        file.close()

    return steps
def imgName(menu):
    Line = []
    Line = menu.split("\n")
    Line.pop(0)
    List = []
    Food = []
    for i in range(0,len(Line)):
        Line[i]=" ".join(Line[i].split())
    i = 0

    while len(Line)-1 > i:
        List.append ([])
        List[i] = Line[i].split(" ")
    
        tmp = []
        tmp = List[i][0].split("-")
        tmp[1] += ".jpg"
        Food.append(tmp[1])
        i+=1
    
    strFood = " ".join(Food)
    return strFood  
def saveBill(bill):
    with open('billList.json','r+') as f:
        file_data = json.load(f)
        file_data["Bill"].append(bill)
        f.seek(0)
        json.dump(file_data, f, indent = 4)
 
#-------------------------------------------------------------

IP = socket.gethostbyname(socket.gethostname())
PORT = 8000
FORMAT = 'utf-8'
SIZE = 1024

#----------------------------------------------------
def handle_client(client, addr):
    try:
        print(f"[NEW CONNECTION] {addr} connected.")
        #---------------TEXT---------------
        intro = "Welcome to Mr.Bean \n\n View menu_Enter: 1 \n Order food_Enter: 2 \n Payment method : 3 \n Extra order (Just before 2 hours) : 4 \n Finish : 5 \n"
        #----------------------------------

        connected = True
        while connected:
            client.sendall(bytes(intro,FORMAT))
            client.sendall(bytes(str(addr),FORMAT))
            req = client.recv(1024).decode(FORMAT)
            while (req != "Finish"):
                if req == "Menu":
                    client.sendall(bytes(menu,FORMAT))
                    client.sendall(bytes(imgName(menu),FORMAT))
                    Food = imgName(menu).split(" ")  
                    for i in range (0,len(Food)):
                        client.sendall(bytes(str(sendImgSteps(Food[i])),FORMAT))
                        sendImg(Food[i],client)
                elif req == "Order":
                    client.sendall(bytes("Order accepted",FORMAT))
                    req = client.recv(1024).decode()
                    client.sendall(bytes(Bill(req),FORMAT)) 
                elif req == "Payment": 
                    option = client.recv(1024).decode(FORMAT)
                    if (option == "2"):
                        print(f"[CONNECTION] {addr} [PAY]")
                        idcard = client.recv(1024).decode(FORMAT)
                        bill = client.recv(1024).decode(FORMAT)
                        print("[RECEIVED]")
                        print(bill)
                        saveBill(bill)
                    else:
                        print(f"[CONNECTION] {addr} [PAY]")
                        bill = client.recv(1024).decode(FORMAT)
                        print("[RECEIVED]")
                        print(bill)
                        saveBill(bill)
                elif req == "Extra":
                    client.sendall(bytes("Extra order accepted",FORMAT))
                    req = client.recv(1024).decode()
                    client.sendall(bytes(Bill(req),FORMAT))
        
                req = client.recv(1024).decode(FORMAT)
      
            if req == "Finish":
                print(addr,"disconnected!")
                client.sendall(bytes("Thanks for choosing us!",FORMAT))
                connected= False
    except:
        print(addr,"disconnected!")
        client.close()

#-----------------------------------------------------
def main():

    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = 'localhost'
    server.bind((HOST,PORT))
    
    print("[STATUS]Server created")

    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    print("[STATUS]Waiting for connection \n")

    data={
        "Bill":[
        ]
    }
    with open('billList.json','w') as f:
        json.dump(data,f,indent=4)

    while True:
        client, addr = server.accept()
        print("Connected by ", addr)
            
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()
        print("[ACTIVE CONNECTIONS]", threading.activeCount() - 1)

    server.close()

if __name__ == "__main__":
    main()
    