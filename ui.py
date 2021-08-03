import tkinter
from PIL import ImageTk, Image
from tkinter import *
import requests
import ast

root = tkinter.Tk()
root.title("ChatRobo Application")
root.iconbitmap(r"D:\STUDY\CapstoneProject\app\picc.ico")
root.geometry("750x400")
root.configure(bg='light pink')
root.option_add('*Font', '19')


def press():
    newWindow = tkinter.Toplevel(root)
    newWindow.title("ChatRobo Application")
    newWindow.iconbitmap(r"D:\STUDY\CapstoneProject\app\picc.ico")
    newWindow.geometry("450x480")
    newWindow.configure(bg="light pink")
    newWindow.resizable(width=FALSE, height=FALSE)

    def send():
        msg = EntryBox.get("1.0", 'end-1c').strip()
        EntryBox.delete("0.0", END)

        if msg != '':
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 12))

            # res = chatbot_response(msg)
            # ChatLog.insert(END, "Bot: " + res + '\n\n')
            # ChatLog.config(state=DISABLED)
            # response from bot
            url = 'http://localhost:5005/webhooks/rest/webhook'
            # url = 'http://localhost:5055/webhook'
            myobj = {
                "message": msg,
                "sender": "User"
            }
            x = requests.post(url, json=myobj)
            ast.literal_eval(x.text)
            print(ast.literal_eval(x.text))
            reply = ast.literal_eval(x.text)[0]["text"]
            ChatLog.insert(END, "ChatRoBo: " + reply + '\n\n')
            ChatLog.yview(END)

    def clear():
        ChatLog.delete("0.0", END)

        # Create Chat window

    ChatLog = Text(newWindow, bd=0, bg="white", height="8", width="50", font="Arial", )
    ChatLog.config(state=DISABLED)

    # Bind scrollbar to Chat window
    scrollbar = Scrollbar(newWindow, command=ChatLog.yview, cursor="heart", bg="#32de97")
    ChatLog['yscrollcommand'] = scrollbar.set

    # Create Button to send message
    SendButton = Button(newWindow, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                        bd=0, bg="#32de97", activebackground="light pink", fg='#ffffff',
                        command=send)

    # Create Button to clear message
    ClearButton = Button(newWindow, font=("Verdana", 12, 'bold'), text="Refresh", width="12", height=5,
                         bd=0, bg="#32de97", activebackground="light pink", fg='#ffffff',
                         command=clear)

    # Create the box to enter message
    EntryBox = Text(newWindow, bd=0, bg="white", width="29", height="5", font="Arial")
    # EntryBox.bind("<Return>", send)

    # Place all components on the screen
    scrollbar.place(x=420, y=6, height=386, width=20)
    ChatLog.place(x=6, y=6, height=386, width=430)
    EntryBox.place(x=174, y=401, height=50, width=265)
    SendButton.place(x=6, y=401, height=50, width=75)
    ClearButton.place(x=90, y=401, height=50, width=75)


# Creating a function
lab1 = tkinter.Label(root, text='Welcome to ChatRobo!', fg="blue", bg="light blue",
                     font=("Times New Roman", 30, "bold"))
lab2 = tkinter.Label(root, text='Click here to proceed further!', fg="blue", bg="light blue",
                     font=("Times New Roman", 12, "italic"))
bt = tkinter.Button(root, text='  click', fg="yellow", bg="light yellow", command=press,
                    font=("Times New Roman", 12, "bold"))
lab1.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
lab2.grid(row=20, column=3, columnspan=1, padx=10, pady=10)
bt.grid(row=20, column=4, columnspan=1, padx=10, pady=30)
root.mainloop()  # event loop