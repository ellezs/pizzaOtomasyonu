import sqlite3
import tkinter
from tkinter import ttk
from tkinter import messagebox

vt=sqlite3.connect("pizza.db")
cursor=vt.cursor()

def getCityList():
    command="select ilAdi from iller"
    cursor.execute(command)
    cities=cursor.fetchall()
    return cities

def getDistrictList(eventObject):   #callback fonksiyonu
    command=f"select ID from iller where ilAdi='{cityCombobox.get()}'"
    cursor.execute(command)
    selectCity=cursor.fetchone()
    global cityID
    cityID=int(selectCity[0])
    command=f"select ilceAdi from ilceler where ilID='{str(cityID)}'"
    cursor.execute(command)
    districtList=cursor.fetchall()
    districtCombobox["values"]=districtList
    try:    #ilk ilçe seçili gelsin
        districtCombobox.current(1)
    except: #liste boş ise hata vermemesi için
        districtCombobox.current((-1))

def saveUserInformation():
    from customer import customer
    buyer=customer()    #nesne oluştur
    if usernameEntry.get().strip() == '':
        messagebox.showinfo("UYARI", "Kullanıcı adı alanını boş geçemezsiniz")
    elif nameEntry.get().strip() == '':
        messagebox.showinfo("UYARI", "Adınız Soyadınız alanını boş geçemezsiniz")
    elif passwordEntry.get().strip() == '':
        messagebox.showinfo("UYARI", "Şifre alanını boş geçemezsiniz")
    elif checkPasswordEntry.get().strip() == '':
        messagebox.showinfo("UYARI", "Şifre kontrolü alanını boş geçemezsiniz")
    elif cityCombobox.get().strip() == '':
        messagebox.showinfo("UYARI", "Şehir seçimi alanını boş geçemezsiniz")
    elif districtCombobox.get().strip() == '':
        messagebox.showinfo("UYARI", "İlçe seçimi alanını boş geçemezsiniz")
    elif addressText.get("1.0", "end-1c").strip() == '':
        messagebox.showinfo("UYARI", "Adres alanını boş geçemezsiniz")
    else:
        buyername=usernameEntry.get().strip().lower()
        if customer.checkUser(buyername):
            messagebox.showinfo("UYARI","Bu kullanıcı adı daha önce alınmıştır")
        else:
            if passwordEntry.get()!=checkPasswordEntry.get():
                messagebox.showerror("HATA", "girilen şifreler uyuşmuyor")
            else:
                buyer.username = usernameEntry.get().lower().strip()
                buyer.nameSurname = nameEntry.get().strip()
                buyer.password=passwordEntry.get().strip()
                buyer.city = cityCombobox.get()
                buyer.district = districtCombobox.get()
                buyer.address = addressText.get("1.0", "end-1c").strip()
                customer.saveUser(buyer)
                root.destroy()
                import logInPanel
                logInPanel.root.mainloop()

root=tkinter.Tk()
root.geometry("500x360")
root.title("Yeni Kullanıcı Kayıt Ekranı")
root.iconbitmap('icon.ico')

usernameLabel=tkinter.Label(root,text = "Kullanıcı adı     : ",font=("Consolas",12))
usernameLabel.grid(row=0,column=0,sticky="W",pady=7)
usernameEntry = tkinter.Entry(root,width=47,bd=3)
usernameEntry.grid(row=0,column=1,pady=7,sticky="W")

nameLabel=tkinter.Label(root,text = "Adınız Soyadınız  : ",font=("Consolas",12))
nameLabel.grid(row=1,column=0,sticky="W",pady=7)
nameEntry = tkinter.Entry(root,width=47,bd=3)
nameEntry.grid(row=1,column=1,pady=7,sticky="W")

passwordLabel=tkinter.Label(root,text = "Şifre             : ",font=("Consolas",12))
passwordLabel.grid(row=2,column=0,sticky="W",pady=7)
passwordEntry = tkinter.Entry(root,width=47,bd=3)
passwordEntry.grid(row=2,column=1,pady=7,sticky="W")

checkPasswordLabel=tkinter.Label(root,text = "Şifre Tekrar      : ",font=("Consolas",12))
checkPasswordLabel.grid(row=3,column=0,sticky="W",pady=7)
checkPasswordEntry = tkinter.Entry(root,width=47,bd=3)
checkPasswordEntry.grid(row=3,column=1,pady=7,sticky="W")

cityLabel=tkinter.Label(root,text="Şehir Seçiniz     : ",font=("Consolas",12))
cityLabel.grid(row=4,column=0,sticky="W",pady=7)
cityList = getCityList()
cityCombobox = ttk.Combobox(root,values=cityList,width=44)
cityCombobox.bind("<<ComboboxSelected>>",getDistrictList)
cityCombobox.grid(row=4,column=1,pady=7,sticky="W")

districtLabel=tkinter.Label(root,text="İlçe Seçiniz      : ",font=("Consolas",12))
districtLabel.grid(row=5,column=0,sticky="W",pady=7)
districtCombobox = ttk.Combobox(root,values="",width=44)
districtCombobox.grid(row=5,column=1,pady=7,sticky="W")

addressLabel=tkinter.Label(root,text="Adres             :",font=("Consolas",12))
addressLabel.grid(row=6,column=0,pady=7,sticky="WN")
addressText= tkinter.Text(root,font=("Consolas",12),height=4,width=30)
addressText.grid(row=6,column=1,pady=7,sticky="W")

saveButton = tkinter.Button(root,text="KAYDET",command=saveUserInformation,width="17",bd=3)
saveButton.grid(row=8,column=1)

root.mainloop()