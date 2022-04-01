import tkinter as tk
from twilio.rest import Client
import random
from time import sleep
import threading

__AUTHOR__ = "Helmsys"
cipher = ""
count = 120

class Main(tk.Tk):
    def __init__(self,sid,token):
        super(Main,self).__init__()
        self.tkWindow()
        self.sid = sid
        self.token = token
        self.r = random.randint(300000,350000)

    def tkWindow(self):
        self.geometry("300x300")
        tk.Label(self,text="Kod Doğrula",font=("arial",15,"bold")).pack()
        self.time = tk.Label(self,text="0 saniye")
        self.time.place(x=240)

        self.var = tk.StringVar()
        self.e1 = tk.Entry(self,font=("arial",12,"bold"),justify="center",textvariable=self.var)
        self.e1.pack()
        self.sendButton = tk.Button(self,text="Kod gönder",command=lambda: threading.Thread(target=self.send).start())
        self.sendButton.pack()

    def topLevel(self):
        self.tl = tk.Toplevel()
        self.tl.geometry("300x400")
        self.tl.title("Sayfa")
        tk.Label(self.tl,text="Hoşgeldiniz !",font=("arial",15,"italic")).pack()

    def settings(self):
        if len(self.var.get()) == 6:
            if cipher == self.var.get():
                print("doğru kod")
                self.topLevel()
                return True
            else:
                return False
        return None

    def whileLoop(self):
        global count
        while count > 0:
            sleep(1)
            count -= 1
            self.time.config(text=str(count)+" saniye")
            if count == 0:
                self.sendButton["state"] = "normal"
                self.time.config(text="0 saniye")
                break
            else:
                if self.settings():
                    self.sendButton["state"] = "normal"
                    self.time.destroy()
                    break

    def send(self):
        self.sendButton["state"] = "disabled"
        self.twilio()
        threading.Thread(target=self.whileLoop()).start()
 
    def twilio(self):
        global cipher
        client = Client(self.sid, self.token)
        message = client.messages.create(body=f'Authentication Code: {self.r}',from_='twilio_number', to='+your_phone_number' )
        for i in message.fetch().body.split(" - ")[1]: 
            if i.isdigit():
                cipher += i
            cipher.strip() 
        tk.Label(self,text="Kod Gönderildi!",font=("arial",15,"bold")).pack()
        return cipher

if __name__ == "__main__":
    account_sid = 'TWILIO_ACCOUNT_SID'
    auth_token = 'TWILIO_AUTH_TOKEN'
    Main(sid=account_sid,token=auth_token).mainloop()
