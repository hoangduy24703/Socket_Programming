import socket
import time
                
def checkid(idcard):
    digits = 0
    for i in range(0,len(idcard)):
        if idcard[i].isdigit():
            digits = digits + 1
        else:
            return False
    if (digits == 10):
        return True
    else:
        return False  

def checkorder(list1):
   s1 = list1.replace("[","")
   s2 = s1.replace("]","")
   s3 = s2.replace("'","")
   s4 = s3.replace(",","")
   newlist=[]
   mylist = s4.split()
   for i in range(1,5):
        name = convertFood(str(i))

        count1 = mylist.count(name)
        if (count1 >= 1):
            num = 0
            for i in range(0,count1):
                ind = mylist.index(name)
                num += int(mylist[ind + 1])
                mylist.pop(ind)

            seq1 = (name, str(num))
            seq2 = " ".join(seq1)
            newlist.append(seq2) 

   return newlist

def recvImg(name,client,steps):
    try:
        file = open(name,"wb")
        img_chunk = client.recv(1024)

        while steps != 0:
            file.write(img_chunk)
            img_chunk = client.recv(1024)
            steps -=1
    except:
        file.close()


def convertFood (name):
    if name == "1":
        name = "Beef_Steak"
    if name == "2":
        name = "Spaghetti"
    if name == "3":
        name = "Pasta"
    if name == "4":
        name = "Pizza"
    if name == "5":
        name = "Burger"
    return name


HOST = 'localhost'
PORT = 8000
FORMAT = 'utf-8'
server_address = (HOST,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

resp = client.recv(1024).decode()
print(resp)
addr = client.recv(1024).decode()


introOrder = "Please enter the ordinal number and quantity of the food you want to order"
introOrder2 = "Please enter the ordinal number and quantity of the food you want to order extra"
connected = True
while connected:
    try:
        orderList = []
        temp = 0
        option = int(input("Option: "))

        while (option != 5):
            if option == 1:
                client.sendall(bytes("Menu",FORMAT))
                resp = client.recv(1024).decode()
                print(resp)

                food = client.recv(1024).decode()
                Food = food.split(" ")

                for i in range (0,len(Food)):
                    steps = int(client.recv(1024).decode())
                    recvImg(Food[i],client,steps)
            
            elif (option == 2):
                orderList.clear()
                temp = 1
                print(introOrder)
                check = ""
                while True:

                    if check == "N" or check == "n":
                        break
                    name = input("Dish: ")
                    name = convertFood(name)
                    quantity = input("Quantity: ")

                    seq = (name,quantity)
                    order = " ".join(seq)
                    orderList.append(order)

                    print("Keep ordering [Y/N]: ")
                    check = input()
                
                req = "\n".join(orderList)
                req += "\nend"

                client.sendall(bytes("Order",FORMAT))
                rep = client.recv(1024).decode(FORMAT)
                print(rep)

                client.sendall(bytes(req,FORMAT))
                resp = client.recv(1024).decode()
                print(resp)
                
            elif (option == 3):

               if (temp == 0):
                    print("No order before. Please try again!!!")
                    break
               
               print("Choose your payments: ")
               print("1. Pay cash")
               print("2. Credit card (Include 10 numbers)") 

               option2 = input("Option payment: ")

               if (option2 == "1"):
                    client.sendall(bytes("Payment",FORMAT))
                    client.sendall(bytes("1",FORMAT))
                    print("Your option is paying cash.")
               if (option2 == "2"):
                    print("Your option is credit card.")
                    idcard=input("Please enter your id card:  ")

                    while (checkid(idcard) == False):
                        print("Your id card is invalid")
                        print("Please enter your id card again: ")  
                        idcard=input()

                    client.sendall(bytes("Payment",FORMAT))
                    client.sendall(bytes("2",FORMAT))
                    client.sendall(bytes(idcard,FORMAT))
                    print("Your id card is valid.")

               orderList = checkorder(str(orderList))
               orderList.insert(0,addr)
               orderList.append("Already paid")

               bill = " ".join(orderList)
               client.sendall(bytes(bill,FORMAT))

               temp = 0
               orderList.clear()

               option = 5
               break
            elif (option == 4):
                if (temp == 0):
                    print("No order before. Please try again!!!")
                    break
                print(introOrder2)
                check = ""
                while True:

                    if check == "N" or check == "n":
                        break
                    
                    name = input("Dish: ")
                    name = convertFood(name)
                    quantity = input("Quantity: ")

                    seq = (name,quantity)
                    order = " ".join(seq)
                    orderList.append(order)

                    print("Keep ordering [Y/N]: ")
                    check = input()
            
                req = "\n".join(orderList)
                req += "\nend"
                client.sendall(bytes("Extra",FORMAT))
                rep = client.recv(1024).decode(FORMAT)
                print(rep)

                client.sendall(bytes(req,FORMAT))
                resp = client.recv(1024).decode()
                print("Latest",resp)

            option = int(input("Option: "))
            
        if (option == 5):
            client.sendall(bytes("Finish",FORMAT))
            resp = client.recv(1024).decode()
            print(resp)
            time.sleep(5)
            connected = False
            client.close()
            break
    except:
        client.close()



