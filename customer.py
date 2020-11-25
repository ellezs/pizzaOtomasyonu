import sqlite3
from tkinter import messagebox
db=sqlite3.connect('pizza.db')
cursor=db.cursor()

class customer:
    customerNo=0            #integer    kullanıcı id si
    def __init__(self):
        self.username=""    #string
        self.nameSurname="" #string
        self.password=""    #string
        self.city=0         #integer    şehir id si
        self.district=0     #integer    ilçe id si
        self.address=""     #string

    @classmethod
    def checkUser(cls,uName): #database de, bu kullanıci adı varsa True yoksa False Dndürür
        '''
        database de bu isimde bir kullanıcı olup olmadığını kontrol eder
        :param uName: kullanıcı adı bilgisi
        :return: True-False
        '''
        db = sqlite3.connect('pizza.db')
        cursor = db.cursor()
        command=f"select kullaniciAdi from musteriler where kullaniciAdi='{str(uName)}'"
        cursor.execute(command)
        isUser=bool(len(cursor.fetchall())) #0=False, 1=True
        return isUser

    @classmethod
    def saveUser(cls,customer):
        '''
        içine yazılan nesnenin verilerini veritabanına kaydeder.
        :param customer: müşteri nesnesi
        :return:
        '''
        db=sqlite3.connect("pizza.db")
        cursor=db.cursor()
        try:
            command=f"select id from iller where ilAdi='{customer.city}'"
            cursor.execute(command)
            customer.city=str(cursor.fetchone()[0])
            command=f"select id from ilceler where ilID='{customer.city}' and ilceAdi='{customer.district}'"
            cursor.execute(command)
            customer.district=(cursor.fetchone()[0])
            command="insert into musteriler(kullaniciAdi,adSoyad,password,il,ilce,adres) values (?,?,?,?,?,?)"
            cursor.execute(command,(customer.username,customer.nameSurname,customer.password,customer.city,customer.district,customer.address))
            db.commit()
            messagebox.showinfo("KAYIT BAŞARILI","Kayıt tamamlanmıştır.")
            db.close()
        except:
            messagebox.showerror("HATA","Veritabanına kayıt sırasında hata oluştu.")
            db.close()

    @classmethod
    def getUser(cls,uName,pwd):
        '''
        :param uName: kullanıcı adı
        :param pwd: şifre
        :return: eğer girilen kullanıcı adı ve şifreye sahip kullanıcı varsa bu kişiyi bütün bilgileriyle nesne olarak döndürür yoksa false döner
        '''
        db=sqlite3.connect('pizza.db')
        cursor = db.cursor()
        try:
            command=f"select * from musteriler where kullaniciAdi='{str(uName)}' and password='{str(pwd)}'"
            cursor.execute(command)
            userInfo=cursor.fetchone()
            db.close()
            user=customer()
            user.customerNo=userInfo[0]
            user.username=userInfo[1]
            user.nameSurname=userInfo[2]
            user.password=userInfo[3]
            user.city=userInfo[4]
            user.district=userInfo[5]
            user.address=userInfo[6]
        except:
            db.close()
            return None
        return user

    @classmethod
    def getUserInfo(cls,userID):
        '''
        :param userID: kullanıcı ID si
        :return: ID ye sahip kullanıcıyı nesne olarak döndürür. orderPanel de aktifkullancı bilgisinde kullanıyorum.
        '''
        db=sqlite3.connect('pizza.db')
        cursor = db.cursor()
        try:
            command=f"select * from musteriler where id='{str(userID)}'"
            cursor.execute(command)
            userInfo=cursor.fetchone()
            db.close()
            user=customer()
            user.customerNo=userInfo[0]
            user.username=userInfo[1]
            user.nameSurname=userInfo[2]
            user.password=userInfo[3]
            user.city=userInfo[4]
            user.district=userInfo[5]
            user.address=userInfo[6]
        except:
            db.close()
            return None
        return user
