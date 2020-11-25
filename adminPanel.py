import sqlite3
import tkinter
from tkinter import ttk, HORIZONTAL,messagebox
from customer import customer

db=sqlite3.connect("pizza.db")
cursor=db.cursor()

def getOrders():
    import sqlite3
    db = sqlite3.connect("pizza.db")
    cursor = db.cursor()
    if check1.get()==True:
        command=f"select * from siparisler"
    else:
        command = f"select * from siparisler where durum=0"
    cursor.execute(command)
    valueList=cursor.fetchall()
    db.close()
    return valueList

def readOrders(orders):
    import sqlite3
    db = sqlite3.connect("pizza.db")
    cursor = db.cursor()
    read=list()
    for i in range(len(orders)):
        read.append(list())
        #0. eleman ID - değiştirmeden ekle
        read[i].append(orders[i][0])
        #1. eleman Müşteri No - müşteri ismini ekle
        command = f"select adSoyad from musteriler where id='{orders[i][1]}'"
        cursor.execute(command)
        value=cursor.fetchone()
        read[i].append(value[0])
        # 2. eleman Ebat
        command = f"select ebat from pizzaEbatlar where id='{orders[i][2]}'"
        cursor.execute(command)
        value=cursor.fetchone()
        read[i].append(value[0])
        # 3. eleman Pizza Tipi
        command = f"select tur from pizzaTuru where id='{orders[i][3]}'"
        cursor.execute(command)
        value=cursor.fetchone()
        read[i].append(value[0])
        # 4. eleman kenar Tipi
        command = f"select tip from kenarTipi where id='{orders[i][4]}'"
        cursor.execute(command)
        value=cursor.fetchone()
        read[i].append(value[0])
        # 5. Eleman Malzemeler
        tops = orders[i][5]  # [1, 2, 4, 5, 8, 9, 10]
        tops = tops[1:len(tops) - 1].split(',')
        topsText = str()
        for item in tops:
            command = f"select malzeme from malzemeler where id='{int(item)}'"
            cursor.execute(command)
            value = cursor.fetchone()
            topsText = topsText + value[0] + ', '
        topsText = topsText[:len(topsText) - 2]
        read[i].append(topsText)
        #6. eleman adet
        read[i].append(orders[i][6])
        #7. eleman tutar
        read[i].append(orders[i][7])
        #8. eleman tamamlanma durumu
        read[i].append('Tamamlandı') if orders[i][8]==True else read[i].append('Bekliyor')
    return read



def showOrders():
    orderFrame.place_configure(x=10, y=40)
    newProductFrame.place_forget()
    global orders
    orders=getOrders()
    orders=readOrders(orders)
    orderTable.delete(*orderTable.get_children()) #tablodaki bütün verileri sil
    orderTable.grid(row=1, column=0)
    for i in range(len(orders)):
        orderTable.insert('','end',values=orders[i])
    doneButton.configure(state=tkinter.NORMAL)


def doneOrder():
    try:
        focused = orderTable.focus()  #I001
        selectedItem=orderTable.item(focused)
        #{'text': '', 'image': '','values': [1, 'Bruce Wayne', 'Büyük', 'Türk', 'Kalın', 'Sosis, Ançuez, Zeytin, Peynir', 1, 104, 'Bekliyor'],'open': 0, 'tags': ''} bööyle bir sözlük oluşuyor.
        selectedID=selectedItem['values'][0]
        selectedItem['values'][8]='Tamamlandı'

        #bir elemanı değiştirmeyi bulamadım hepsini silip baştan yazıyorum
        orderTable.delete(*orderTable.get_children())
        for i in range(len(orders)):
            if orders[i][0]==selectedID:
                orders[i]=selectedItem['values']
            orderTable.insert('','end',values=orders[i])

        #database de aynı değişikliği yapmak için:
        import sqlite3
        db = sqlite3.connect("pizza.db")
        cursor = db.cursor()
        cursor.execute(f"update siparisler set durum=1 where id='{selectedID}'")
        db.commit()
        db.close()
    except:
        messagebox.showerror("HATA","Bir hata oluştu. Seçim yaptığınızdan emin olunuz.")


def addNewProduct():
    newProductFrame.place_configure(x=10, y=40)
    orderFrame.place_forget()
    doneButton.configure(state=tkinter.DISABLED)

def getValues(table):   #database de bulunan hangi sütunun adı girilirse ona göre veri döndürür
    import sqlite3
    db = sqlite3.connect("pizza.db")
    cursor = db.cursor()
    command=f"select * from {table}"
    cursor.execute(command)
    valueList=cursor.fetchall()
    db.close()
    return valueList

def listItems():
    namesInDatabase=['pizzaEbatlar','pizzaTuru','kenarTipi','malzemeler'] #databasedeki isimler
    #catalogList ile aynı sırada
    itemList=getValues(namesInDatabase[catalogList.index(catalogCombobox.get())])
    productTable.delete(*productTable.get_children()) #tablodaki bütün verileri sil
    # productTable.grid(row=1, column=0)
    for i in range(len(itemList)):
        productTable.insert('','end',values=itemList[i])

def addProduct():
    namesInDatabase = ['pizzaEbatlar', 'pizzaTuru', 'kenarTipi', 'malzemeler']
    headingsInDatabase = ['ebat', 'tur', 'tip', 'malzeme']
    table=namesInDatabase[catalogList.index(catalogCombobox.get())]
    heading=headingsInDatabase[catalogList.index(catalogCombobox.get())]
    name=addItemNameEntry.get()
    price=int(addItemPriceEntry.get())
    import sqlite3
    db = sqlite3.connect("pizza.db")
    cursor = db.cursor()
    command=f"insert into {table}({heading},fiyat) values (?,?)"
    cursor.execute(command,(name,price))
    db.commit()
    db.close()


# command="insert into pizzaEbatlar(ebat,fiyat) values (?,?)"
# cursor.execute(command,('Büyük',50))

def closeDown():
    root.destroy()

root=tkinter.Tk()
root.geometry("960x460")
root.title("Admin Paneli")
root.iconbitmap('icon.ico')

menuFrame=tkinter.Frame(root, width=900, height=40, bg="Blue")
menuFrame.place(x=10, y=5)

orderButton=tkinter.Button(menuFrame,text="Siparişleri Göster", font="Consolas 8", width=18, command=showOrders)
orderButton.grid(row=0,column=0, padx=10, pady=1)

newProductButton=tkinter.Button(menuFrame,text="Yeni Ürün Ekle", font="Consolas 8", width=18, command=addNewProduct)
newProductButton.grid(row=0,column=1, padx=10, pady=1)

doneButton=tkinter.Button(menuFrame,text="Siparişi Tamamla", font="Consolas 8", width=18, command=doneOrder)
doneButton.grid(row=0,column=2, padx=10, pady=1)

check1=tkinter.IntVar()
doneCheck = tkinter.Checkbutton(menuFrame, text="Tamamlananları Göster", font="Consolas 8", variable=check1, onvalue=True, offvalue=False)
doneCheck.grid(row=0,column=3, padx=10, pady=1)

exitButton=tkinter.Button(menuFrame,text="Çıkış", font="Consolas 8", width=18, command=closeDown)
exitButton.grid(row=0,column=5, padx=10, pady=1)

orderFrame=tkinter.Frame(root, width=900, height=300)
orderFrame.place(x=10, y=40)
tkinter.Label(orderFrame,text='Siparişler Listeleniyor'.ljust(260),anchor='w').grid(row=0,column=0)
tableHeads=['ID','Müşteri','Ebat','Usül','Kenar','Malzemeler','Ad.','Tutar','Durum']
cols=['I','Mu','E','U','K','Ma','A','T','D']
orderTable=tkinter.ttk.Treeview(orderFrame,columns=cols,show='headings',height=16)
wi=[10,100,50,60,50,460,30,40,90] #sütun genişlikleri
for i in range(len(cols)):
    orderTable.column(cols[i],width=wi[i], anchor='w')
    orderTable.heading(cols[i], text=tableHeads[i])
orderTable.grid(row=1,column=0)
scrollbar = tkinter.Scrollbar(orderFrame,orient=HORIZONTAL,width=8)
scrollbar.grid(row=2,column=0,ipadx=420,ipady=2)
orderTable.config(xscrollcommand = scrollbar.set)
scrollbar.config(command = orderTable.xview)


newProductFrame=tkinter.Frame(root, width=900, height=300)
# newProductFrame.place(x=10, y=40) # program ilk çalıştığında görünmeyecek

catalogLabel=tkinter.Label(newProductFrame,text='Eklenecek bilgi türü'.ljust(30),font='Consolas 8')
catalogLabel.grid(row=1,column=0,padx=10,pady=5,columnspan=4)
catalogList=['Ebatlar','Usul','Kenar Tipi', 'Malzemeler']
catalogCombobox = ttk.Combobox(newProductFrame,values=catalogList,width=44)
catalogCombobox.grid(row=1,column=4,pady=5,sticky="W",padx=10,columnspan=4)
catalogCombobox.current(0)

ListItemsButton=tkinter.Button(newProductFrame,text='Mevcut bilgileri görüntüle'.ljust(30), font="Consolas 10", width=30, command=listItems)
ListItemsButton.grid(row=1,column=8,padx=10,pady=5,columnspan=4)

addItemNameLabel=tkinter.Label(newProductFrame,text='Eklenecek ürün ismi'.ljust(24),font='Consolas 8')
addItemNameLabel.grid(row=2,column=0,padx=10,pady=5,columnspan=3)
addItemNameEntry=tkinter.Entry(newProductFrame,font='Consolas 8',width=30)
addItemNameEntry.grid(row=2,column=3,padx=10,pady=5,columnspan=3)

addItemPriceLabel=tkinter.Label(newProductFrame,text='Eklenecek ürün fiyatı'.ljust(24),font='Consolas 8')
addItemPriceLabel.grid(row=2,column=6,padx=10,pady=5,columnspan=3)
addItemPriceEntry=tkinter.Entry(newProductFrame,font='Consolas 8',width=30)
addItemPriceEntry.grid(row=2,column=9,padx=10,pady=5,columnspan=3)

tkinter.Label(newProductFrame,text='Ürünler Listeleniyor'.ljust(30),anchor='nw').grid(row=3,column=0,columnspan=3)

addProductButton=tkinter.Button(newProductFrame,text='Ürünü Ekle', font="Consolas 8", width=20, command=addProduct)
addProductButton.grid(row=3,column=4,padx=10,pady=5,columnspan=4)

tableHeads=['ID','isim','Fiyat']
cols=['Id','Is','F']
productTable=tkinter.ttk.Treeview(newProductFrame,columns=cols,show='headings',height=6)
wi=[20,200,40] #sütun genişlikleri
for i in range(len(cols)):
    productTable.column(cols[i],width=wi[i], anchor='w')
    productTable.heading(cols[i], text=tableHeads[i])
productTable.grid(row=4,column=0,columnspan=6,pady=5)



root.mainloop()