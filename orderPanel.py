import sqlite3
import tkinter
from tkinter import ttk, HORIZONTAL,messagebox
from customer import customer

db=sqlite3.connect("pizza.db")
cursor=db.cursor()

def getValues(table):   #database de bulunan hangi sütunun adı girilirse ona göre veri döndürür
    db = sqlite3.connect("pizza.db")
    cursor = db.cursor()
    command=f"select * from {table}"
    cursor.execute(command)
    valueList=cursor.fetchall()
    db.close()
    return valueList

def createPizza():
    '''
    root da seçilen objeleri okuyup liste olarak kaydeder
    # pizza = [ebat, tur, kenar, malzeme(liste),adet]
    :return: ID lerden oluşan bir bilgi döndürür
    '''
    try:
        pizza=list()
        sizeP=sizeCombobox.get()
        pizza.append(sizeValues[[i for i in range(len(sizeValues)) if sizeValues[i][1]==sizeP][0]][0])
        typeP=typeList.get(typeList.curselection())
        pizza.append(typeValues[[i for i in range(len(typeValues)) if typeValues[i][1] == typeP][0]][0])
        edgeP=r.get()
        pizza.append(edgeP)
        toppingP=[topsVar[i].get() for i in range(len(toppingList)) if topsVar[i].get() != 0]
        pizza.append(toppingP)
        return pizza #[2, 3, 2, [1, 5, 8]] böyle bir şey
    except:
        pass #seçilmeyen alanlar varsa hata vermesin

def calcPrice():
    '''
    pizza fiyatını hesaplamaya yarar, ve ekranda tutar etiketine yazar
    :return: [[pizza bilgilerini içeren liste],adet,fiyat]
    '''
    try:
        price = 0
        pizza=createPizza() #[2, 3, 2, [1, 5, 8]] böyle bir şey
        # print(f"ebat fiyatı{sizeValues[[i for i in range(len(sizeValues)) if sizeValues[i][0] == pizza[0]][0]][2]}")
        price+=sizeValues[[i for i in range(len(sizeValues)) if sizeValues[i][0]==pizza[0]][0]][2]
        #sizeValues: içinde büyük,küçük,orta bilgilerini tutan liste #[(1, 'Büyük', 50), (2, 'Orta', 40), (3, 'Küçük', 30)]
        #sizeValues[i][0]:id #pizza[0]:seçilen ebat ın IDsi
        # [i for i in range(len(sizeValues)) if sizeValues[i][0]==pizza[0]]:bu ifade seçilen tek elemanlı bir listedir. bu nedenle yanına [0] ifadesi eklenip integer değer elde ediliyor. bu integer değer sizeValues in kaçıncı elemanını-(id,ebat,fiyat) içeren tuple- almamız gerektiğini belirtir.
        #sondaki [2], tuple in 2. indisinde fiyat olduğunu belirtir. Bulunan değer price'a eklenir.
        price+=typeValues[[i for i in range(len(typeValues)) if typeValues[i][0]==pizza[1]][0]][2]
        price += edgeList[[i for i in range(len(edgeList)) if edgeList[i][0] == pizza[2]][0]][2]
        for item in toppingList: #her bir item şöyle: (1, 'Dana Jambon', 10)
            price += item[2] if item[0] in pizza[3] else 0 #malzeme kullanılmışsa fiyatını ekle, kullanılmamışsa 0 ekle
            # pizza[3]- kullanılan malzemelerin ID lerini içeren bir listedir.
            # item[3]: malzemenin fiyat bilgisi
        qty=int(qtySpin.get()) #adet bilgisi
        price*=qty #pizza fiyatını adetle çarp
        amount=f'{price}.00'.rjust(8) #sondaki .00 sadece görsel amaçlı
        priceLabel.configure(text=f"Tutar        = {amount} TL") #tutar labelindeki veriyi degiştirir
        return [pizza,qty,price]
    except:
        messagebox.showwarning("UYARI","Lütfen bütün seçimleri yaptığınızdan emin olunuz.") #seçim yapılmamışsa uyarı veriyor. Başka bir hata olursa yine bu uyarıyı verece. düzeltilmeli

def addToBasket():
    '''
    Bilgileri oluşan pizza ürününü sepete ekler. database de işlem yapmaz sadece ekranda görünür.
    '''
    try:
        order=calcPrice()  #hesapla butonuna basıldıktan sonra seçimler değiştirilip hesapla demeden sepete ekle denme ihtimaline karşın hesaplama baştan yapılıyor.

        if order is not None:
            basket.append(order) #basket dışarıda boş olarak oluşturulmuş bir liste.
            #iki ürün eklenmiş basket: #[[[2, 3, 2, [1, 5, 8]],qty,price],[[2, 3, 2, [1, 5, 8]],qty,price]]
            toppings=str() #malzemeler listesindeki veriyi stringe çevireceğiz
            for item in basket[-1][0][3]: # [[2, 3, 2, [1, 5, 8]],qty,price] -1 inci eleman bu.
                toppings=toppings+toppingList[[i for i in range(len(toppingList)) if toppingList[i][0]==item][0]][1]+', '
            basketText=sizeValues[[i for i in range(len(sizeValues)) if sizeValues[i][0] == basket[-1][0][0]][0]][1]+' boy, '+ typeValues[[i for i in range(len(typeValues)) if typeValues[i][0] == basket[-1][0][1]][0]][1]+' usulü, '+edgeList[[i for i in range(len(edgeList)) if edgeList[i][0] == basket[-1][0][2]][0]][1]+' kenar, '+'Malzemeler: '+toppings+' Adet:'+str(basket[-1][1])+', Tutar:'+str(basket[-1][2])+'TL'
            # basket: [[[1, 2, 2, [2, 3, 4, 5, 8, 10]], 1, 106]]
            # basketText: Büyük boy, İtalyan usulü, İnce kenar, Malzemeler: Sosis, Mısır, Ançuez, Zeytin, Mantar, Peynir,  Adet:1, Tutar:106TL
            basketList.insert(basketList.size()+1, basketText) #basketText sepet penceresinde görünsün diye
            sumBasket = 0 #sepetin toplam tutarı
            for item in basket: #[[pizza1,qty,price],[pizza2,qty,price]] #iki item içeren basket
                sumBasket += item[2] #item[2]:fiyat
            totalAmount = f'{sumBasket}.00'.rjust(8) #sum basketi text e çevirdim. bboyutunu ayarlamak daha kolay yazı sağa sola kaymıyor.
            totalPriceLabel.configure(text=f"Toplam Tutar = {totalAmount} TL")
    except:
        pass #bilgi eksik ise hata vermesin.

def confirmOrder():
    '''
    bbasket öğesinin elemanlarını sepete database e gönderiyor
    '''
    try:
        import sqlite3
        db = sqlite3.connect("pizza.db")
        cursor = db.cursor()
        for i in range(len(basket)): #[[[2, 3, 2, [1, 5, 8]],qty,price],[[1, 2, 4, [1, 3, 5, 8, 10]],qty,price]]
            command = "insert into siparisler(musteriID,ebat,pizzaTipi,kenar, malzemeler, adet,tutar, durum) values (?,?,?,?,?,?,?,?)"
            cursor.execute(command,(activeUser.customerNo,basket[i][0][0],basket[i][0][1],basket[i][0][2],str(basket[i][0][3]),basket[i][1],basket[i][2],0))
        db.commit()
        db.close()
        messagebox.showinfo("BAŞARILI", "Siparişiniz alınmıştır")
    except:
        messagebox.showerror("HATA","İşlem Sırasında bir hata oluştu")

def removeItem():
    '''
    Sepete eklenen pizzaları listeden siler
    '''
    itemNo=basketList.curselection()[0]
    basketList.delete(itemNo)
    del basket[itemNo]
    sumBasket = 0  # sepetin toplam tutarı
    for item in basket:  # [[pizza1,qty,price],[pizza2,qty,price]] #iki item içeren basket
        sumBasket += item[2]  # item[2]:fiyat
    totalAmount = f'{sumBasket}.00'.rjust(
        8)  # sum basketi text e çevirdim. bboyutunu ayarlamak daha kolay yazı sağa sola kaymıyor.
    totalPriceLabel.configure(text=f"Toplam Tutar = {totalAmount} TL")

def closeDown():
    '''
    Güvenli çıkış: database de giriş yapan kişi bilgisini siliyor
    '''
    import sqlite3
    db = sqlite3.connect("pizza.db")
    cursor = db.cursor()
    cursor.execute(f"update temp set data='0' where key='activeUser'") #database de bulunan aktif kullanıcı idsini siliyor.
    db.commit()
    db.close()
    root.destroy()
    #tempdeki data=0 iken main.py yerine orderPanel.py çalıştırınca loginPanel.py ye ynlendiriyor. Daha sonra giriş yapıp orderPanel.py açılıp tekrar güvenli çıkış denilince destroy hata veriyor: _tkinter.TclError: can't invoke "button" command: application has been destroyed

root=tkinter.Tk()
root.geometry("700x480")
root.title("Pizza Sipariş Ekranı")
root.iconbitmap('icon.ico')

activeUser=customer()
command="select data from temp where key='activeUser'"
cursor.execute(command)
customerNo=cursor.fetchone()[0]
if customerNo=='0':     #eğer main.py yerine doğrudan orderPanel çalıştırılırsa aktif kullanıcı bilgisinin oluşması için tekrar giriş yapılması isteniyor.
    messagebox.showwarning("UYARI", "Sisteme giriş yapılmalıdır.")
    root.destroy()
    import logInPanel
    logInPanel.root.mainloop()
else:
    activeUser = customer.getUserInfo(customerNo)
    welcomeLabel = tkinter.Label(root, text=f"Hoşgeldiniz {activeUser.nameSurname}", font="Ariel 12", width=72)
    welcomeLabel.place(x=10, y=10)

exitButton=tkinter.Button(root,text="Güvenli Çıkış", font="Consolas 8", width=18, command=closeDown)
exitButton.place(x=540, y=10)

selectorsFrame=tkinter.Frame(root, width=300, height=400)
selectorsFrame.place(x=10, y=40)

sizeLabel=tkinter.Label(selectorsFrame,text="Ebat".ljust(16), font="Consolas 9")
sizeLabel.grid(row=0,column=0,padx=10,pady=10,sticky="W")
sizeValues=getValues('pizzaEbatlar')
sizeCombobox=ttk.Combobox(selectorsFrame,values=([sizeValues[i][1] for i in range(len(sizeValues))]), width=22)
sizeCombobox.grid(row=0,column=1,padx=10,pady=10,sticky="W")
sizeCombobox.current(0)

typeLabel=tkinter.Label(selectorsFrame,text="Pizza Türü".ljust(16), font="Consolas 9")
typeLabel.grid(row=1,column=0,padx=10,pady=10,sticky="WN")
typeValues=getValues('pizzaTuru')
typeList=tkinter.Listbox(selectorsFrame, height=5, width=25)
for i in range(len(typeValues)):
    typeList.insert(typeValues[i][0],typeValues[i][1])
typeList.grid(row=1,column=1,padx=10,pady=10,sticky="W")

edgeLabel=tkinter.Label(selectorsFrame,text="Kenar Tipi".ljust(16),font="Consolas 9")
edgeLabel.grid(row=2,column=0,padx=10,pady=10,sticky="WN")
edgeFrame=tkinter.Frame(selectorsFrame,width=160, height=100)
edgeFrame.grid(row=2,column=1,padx=10,pady=10,sticky="W")
edgeList=getValues('kenarTipi')
edgeVar=list()
r=tkinter.IntVar()
for i in range(len(edgeList)): #kenar tipi sayısı artsa bile çalışır
    edgeVar.append(i)
    edgeVar[i]=tkinter.Radiobutton(edgeFrame,text=f"{edgeList[i][1]}",font="Ariel 9", variable=r, value=edgeList[i][0])
    edgeVar[i].grid(row=i//2,column=i%2,sticky="W")

toppingFrame=tkinter.Frame(selectorsFrame,width=300, height=100)
toppingFrame.grid(row=3,column=0,padx=10,pady=10,sticky="W",columnspan=2)
toppingLabel=tkinter.Label(toppingFrame,text="Malzemeler",font="Consolas 9")
toppingLabel.grid(row=0,column=0,sticky="W")
toppingList=getValues('malzemeler')

topsVar=list()
for i in range(len(toppingList)): #malzeme sayısı artsa bile çalışır
    topsVar.append(tkinter.IntVar())
    topCheck = tkinter.Checkbutton(toppingFrame, text=toppingList[i][1].ljust(16), font="Ariel 8", variable=topsVar[i],onvalue=toppingList[i][0], offvalue=0)
    topCheck.grid(row=(i//3)+1, column=i%3, sticky="W")

qtyLabel=tkinter.Label(selectorsFrame, text="Adet".ljust(16), font="Consolas 10")
qtyLabel.grid(row=4,column=0,padx=10,pady=10,sticky="W")
qtySpin=tkinter.Spinbox(selectorsFrame,from_=1, to=10)
qtySpin.grid(row=4,column=1,padx=10,pady=10,sticky="W")

calculatorsFrame=tkinter.Frame(root, width=200, height=100)
calculatorsFrame.place(x=330, y=40)

calculateButton=tkinter.Button(calculatorsFrame,text="Hesapla", font="Consolas 10", width=12, command=calcPrice)
calculateButton.grid(row=0,column=0,padx=10,pady=10,sticky="W")

amount=str().rjust(8)
priceLabel=tkinter.Label(calculatorsFrame,text=f"Tutar        = {amount} TL",font="Consolas 10", width=26)
priceLabel.grid(row=0,column=1,padx=14,pady=10,sticky="W")

basketButton=tkinter.Button(calculatorsFrame,text="Sepete Ekle", font="Consolas 10", width=12, command=addToBasket)
basketButton.grid(row=1,column=0,padx=10,pady=10,sticky="W")

totalAmount=str().rjust(8)
totalPriceLabel=tkinter.Label(calculatorsFrame,text=f"Toplam Tutar = {totalAmount} TL",font="Consolas 10", width=26)
totalPriceLabel.grid(row=1,column=1,padx=14,pady=10,sticky="W")

basketFrame=tkinter.Frame(root, width=330, height=200)
basketFrame.place(x=330, y=140)
basketLabel=tkinter.Label(basketFrame, text="Sepetteki Ürünler",font="Consolas 10")
basketLabel.grid(row=0,column=0,padx=10,pady=5,sticky="W")
basket = list() #addTOBasket buraya ekliyor
listFrame=tkinter.Frame(basketFrame, width=330, height=200)
listFrame.grid(row=1,column=0,padx=0,pady=0,ipadx=0,ipady=0,columnspan=2)
basketList=tkinter.Listbox(listFrame, height=12, width=50)
basketList.grid(row=0,column=0,padx=10,pady=0,ipadx=4,ipady=4,sticky="W")
scrollbar = tkinter.Scrollbar(listFrame,orient=HORIZONTAL,width=8)
scrollbar.grid(row=1,column=0,ipadx=130,ipady=2)
basketList.config(xscrollcommand = scrollbar.set)
scrollbar.config(command = basketList.xview)

removeButton=tkinter.Button(basketFrame,text="Listeden Çıkar", font="Consolas 10", width=16, command=removeItem)
removeButton.grid(row=2,column=0,padx=20,pady=10,sticky="W")

okButton=tkinter.Button(basketFrame,text="Siparişi Onayla", font="Consolas 10", width=16, command=confirmOrder)
okButton.grid(row=2,column=1,padx=20,pady=10,sticky="W")


root.mainloop()
db.close()