import tkinter
from PIL import ImageTk, Image
from tkinter import *
from tkinter import messagebox
import requests
import ast

root = tkinter.Tk()
root.title("ChatRobo Application")
root.iconbitmap(r"./picc.ico")
root.geometry("750x400")
root.configure(bg='light pink')
root.option_add('*Font', '19')


def press():
    root.destroy()
    newWindow = Tk()
    newWindow.title("ChatRobo Application")
    newWindow.iconbitmap(r"./picc.ico")
    newWindow.geometry("450x510")
    newWindow.configure(bg="light pink")
    newWindow.resizable(width=FALSE, height=FALSE)

    def choice(option):

        if option == "yes":
            messagebox.showinfo("Feedback", " Yes! We are glad that you liked our app!\n \n Thanks for the feedback!")
            pop.destroy()
        else:
            messagebox.showinfo("Feedback", " Thanks for the feedback!")
            pop.destroy()

    def quit():
        newWindow.destroy()
        global pop
        pop = tkinter.Tk()
        pop.title("Feedback")
        pop.geometry("400x300+250+250")
        pop.config(bg="light pink")

        pop_label = tkinter.Label(pop, text='Did you enjoy chatting with ChatRobo?', fg="blue", bg="light blue",
                                  font=("Times New Roman", 14, "bold"))
        pop_label.grid(row=2, column=2, columnspan=1, padx=10, pady=10)

        yes = Button(pop, text="Yes", command=lambda: choice("yes"), bg="orange")
        yes.grid(row=4, column=2, columnspan=1, padx=10, pady=10)

        no = Button(pop, text="No", command=lambda: choice("no"), bg="yellow")
        no.grid(row=4, column=3, columnspan=1, padx=10, pady=10)

        # Quit Button to quit message

    QuitButton = Button(newWindow, font=("Verdana", 12, 'bold'), text="Quit", width="12", height=5,
                        bd=0, bg="#32de97", activebackground="light pink", fg='#ffffff',
                        command=quit)

    def send():
        msg = EntryBox.get("1.0", 'end-1c').strip()
        EntryBox.delete("0.0", END)

        if msg != '':
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 12))

            # response from bot
            #url = 'http://localhost:5005/webhooks/rest/webhook'
            url = 'http://20.185.176.92:5050/webhooks/rest/webhook'

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

    def refresh():
        ChatLog.delete("0.0", END)

    def clear():
        EntryBox.delete("0.0", END)

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
    ClearButton = Button(newWindow, font=("Verdana", 12, 'bold'), text="Clear", width="12", height=5,
                         bd=0, bg="#32de97", activebackground="light pink", fg='#ffffff',
                         command=clear)

    # Refresh Button to clear message
    RefreshButton = Button(newWindow, font=("Verdana", 12, 'bold'), text="Refresh", width="12", height=5,
                           bd=0, bg="#32de97", activebackground="light pink", fg='#ffffff',
                           command=refresh)

    # Create the box to enter message
    EntryBox = Text(newWindow, bd=0, bg="white", width="29", height="5", font="Arial")
    # EntryBox.bind("<Return>", send)

    # Place all components on the screen
    scrollbar.place(x=420, y=6, height=386, width=20)
    ChatLog.place(x=6, y=6, height=386, width=430)
    EntryBox.place(x=174, y=401, height=100, width=265)
    SendButton.place(x=6, y=401, height=50, width=75)
    RefreshButton.place(x=90, y=401, height=50, width=75)
    ClearButton.place(x=6, y=455, height=50, width=75)
    QuitButton.place(x=90, y=455, height=50, width=75)


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