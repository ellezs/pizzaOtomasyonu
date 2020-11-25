import tkinter
from tkinter import messagebox
from customer import customer

def userLogin():
    enteredUsername=usernameEntry.get().lower().strip()
    enteredPassword=passwordEntry.get().strip()
    if enteredUsername=='' or enteredPassword=='':
        messagebox.showwarning("UYARI", "Adınız ve/veya Şifreniz alanlarını boş geçemezsiniz!!!")
    else:   #kullanıcı adı ve şifre düzgün şekilde girilmişse #buyer adında bir nesne oluşturur
        buyer=customer()
        buyer=customer.getUser(enteredUsername,enteredPassword)
        if buyer: #getUser fonksiyonu kullanıcı adı ve şifre kontrolü yaptığı için tekrar kontröle gerek yok.
            messagebox.showwarning("GİRİŞ BAŞARILI", "Giriş başarılıdır")
            root.destroy()
            import sqlite3
            db = sqlite3.connect("pizza.db")
            cursor = db.cursor()
            cursor.execute(f"update temp set data='{buyer.customerNo}' where key='activeUser'")
            db.commit()
            db.close()
            import orderPanel  # db.commit ten daha üstte yazınca hata temp teki veriye hatalı okuyor.
            orderPanel.root.mainloop()
        else: #buyer: değeri None dönerse
            messagebox.showwarning("GİRİŞ BAŞARISIZ", "Lütfen bilgilerinizi kontrol ediniz")


def adminLogin():
    enteredUsername=usernameEntry.get().lower().strip()
    enteredPassword=passwordEntry.get().strip()
    if enteredUsername=='' or enteredPassword=='':
        messagebox.showwarning("UYARI", "Adınız ve Şifreniz alanlarını boş geçemezsiniz!!!")
    elif enteredUsername=='admin' and enteredPassword=='admin': #database yok şifre kontrolü burada
        messagebox.showwarning("GİRİŞ BAŞARILI","Giriş başarılıdır")
        root.destroy()
        import adminPanel
        adminPanel.root.mainloop()
    else:
        messagebox.showwarning("GİRİŞ BAŞARISIZ", "Lütfen bilgilerinizi kontrol ediniz")

def newUser():
    root.withdraw()
    import signUpPanel
    signUpPanel.root.mainloop()


root=tkinter.Tk()
root.geometry("380x340")
root.title("Kullanıcı Girişi")
root.iconbitmap('icon.ico')


img = tkinter.PhotoImage(file="logo.gif")
img = img.subsample(2,2)
lbl_img =tkinter.Label(root,image=img)
lbl_img.grid(row=0,column=0,columnspan=3)

usernameLabel=tkinter.Label(root,text="Kullanıcı adı",font=("Consolas",12))
usernameLabel.grid(row=1,column=0,sticky="W")
usernameEntry=tkinter.Entry(root,width="40",bd=3)
usernameEntry.grid(row=1,column=1,columnspan=2)

passwordLabel=tkinter.Label(root,text="Şifre",font=("Consolas",12))
passwordLabel.grid(row=2,column=0,sticky="W")
passwordEntry=tkinter.Entry(root,width="40",bd=3)
passwordEntry.grid(row=2,column=1,columnspan=2)

logInButton=tkinter.Button(root,text="GİRİŞ",command=userLogin,width="16",bd=3)
logInButton.grid(row=4,column=1)

signUpButton=tkinter.Button(root,text="YENİ KULLANICI",command=newUser,width="16",bd=3)
signUpButton.grid(row=4,column=2)

adminButton=tkinter.Button(root,text="YÖNETİCİ GİRİŞİ",command=adminLogin,width="16",bd=3)
adminButton.grid(row=5,column=1)

root.mainloop()