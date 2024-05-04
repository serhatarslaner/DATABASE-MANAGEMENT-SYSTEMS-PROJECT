import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem




db = sqlite3.connect('gezginGemiSirketi.db')

db.execute('''CREATE TABLE IF NOT EXISTS YOLCUGEMISI
                 (
                    seri_no INTEGER PRIMARY KEY,
                    ad TEXT NOT NULL,
                    agirlik REAL NOT NULL,
                    yapim_yili INTEGER NOT NULL,
                    yolcu_kapasitesi INTEGER                    
                    )''')

db.execute('''CREATE TABLE IF NOT EXISTS PETROLGEMISI
                 (
                    seri_no INTEGER PRIMARY KEY,
                    ad TEXT NOT NULL,
                    agirlik REAL NOT NULL,
                    yapim_yili INTEGER NOT NULL,
                    petrol_kapasite INTEGER
                    )''')

db.execute('''CREATE TABLE IF NOT EXISTS KONTEYNERGEMISI
                 (
                    seri_no INTEGER PRIMARY KEY,
                    ad TEXT NOT NULL,
                    agirlik REAL NOT NULL,
                    yapim_yili INTEGER NOT NULL,
                    konteyner_sayisi INTEGER,
                    maks_agirlik INTEGER
                    )''')

db.execute('''CREATE TABLE IF NOT EXISTS SEFERLER 
                 (
                    sefer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    yola_cikis_tarihi TEXT NOT NULL,
                    donus_tarihi TEXT NOT NULL,
                    cikis_limani TEXT NOT NULL
                    )''')

db.execute('''CREATE TABLE IF NOT EXISTS LIMANLAR
                 (
                    liman_adi TEXT ,
                    liman_ulkesi TEXT ,
                    nufus INTEGER NOT NULL,
                    pasaport_sorgu TEXT NOT NULL,
                    demirleme_ucret INTEGER NOT NULL,
                    PRIMARY KEY(liman_adi,liman_ulkesi)
                    )''')

db.execute('''CREATE TABLE IF NOT EXISTS KAPTANLAR
                 (
                    kaptan_id INTEGER PRIMARY KEY ,
                    kaptan_ad TEXT NOT NULL,
                    kaptan_soyad TEXT NOT NULL,
                    kaptan_adres TEXT NOT NULL,
                    kaptan_vatandaslik TEXT NOT NULL,
                    kaptan_dogum_tarihi INTEGER NOT NULL,
                    kaptan_iseGiris INTEGER NOT NULL, 
                    kaptan_lisans TEXT NOT NULL                                
                    )''')

db.execute('''CREATE TABLE IF NOT EXISTS MURETTABAT 
                 (
                    murettebat_id INTEGER PRIMARY KEY ,
                    murettebat_ad TEXT NOT NULL,
                    murettebat_soyad TEXT NOT NULL,
                    murettebat_adres TEXT NOT NULL,
                    murettebat_vatandaslik TEXT NOT NULL,
                    murettebat_dogum_tarihi INTEGER NOT NULL,
                    murettebat_gorev TEXT NOT NULL,
                    murettebat_iseGiris INTEGER NOT NULL 
                    )''')

db.execute('''CREATE TABLE IF NOT EXISTS SEFEROLUSTUR
                 (
                    sefer_id INTEGER PRIMARY KEY ,
                    kaptan_id TEXT NOT NULL,
                    murettebat_id TEXT NOT NULL,
                    gemi_seri_no TEXT NOT NULL,
                    gidilecek_liman TEXT NOT NULL
                    )''')
db.commit()

class veriKontrol():
    def __init__(self,tableName):
        self.db = sqlite3.connect('gezginGemiSirketi.db')
        self.sorgu = self.db.cursor()
        self.tableName = tableName
       
    def listele(self):
        listeleme = self.sorgu.execute('select * from {}'.format(self.tableName)).fetchall()
        return listeleme
    
class seferolustur(veriKontrol):
    def ekleme(self,sefer_id,kaptan_id,murettebat_id,gemi_seri_no,gidilecek_liman):
            try:
                self.sorgu.execute('insert into SEFEROLUSTUR values(?,?,?,?,?)',(sefer_id,kaptan_id,murettebat_id,gemi_seri_no,gidilecek_liman))
                self.db.commit()
            except sqlite3.IntegrityError:
                pass

    
    def silme(self,sefer_id):
        self.sorgu.execute("Delete  from SEFEROLUSTUR where sefer_id=?",(sefer_id,)) 
        self.db.commit()

    

    def guncelle(self,sefer_id,kaptan_id,murettebat_id,gemi_seri_no,gidilecek_liman):
        self.sorgu.execute("UPDATE SEFEROLUSTUR SET kaptan_id=?,murettebat_id=?,gemi_seri_no=?,gidilecek_liman=? WHERE sefer_id=? ",(kaptan_id,murettebat_id,gemi_seri_no,gidilecek_liman,sefer_id))   
        self.db.commit()


class yolcuGemi(veriKontrol):
    def ekleme(self,seri_no,ad,agirlik,yapim_yili,yolcu_kapasitesi):
        try:
            self.sorgu.execute('insert into YOLCUGEMISI values(?,?,?,?,?)',(seri_no,ad,agirlik,yapim_yili,yolcu_kapasitesi))
            self.db.commit()
        except sqlite3.IntegrityError:
            pass
    
    def silme(self,seri_no):
        self.sorgu.execute("Delete  from YOLCUGEMISI where seri_no=?",(seri_no,)) 
        self.db.commit()

    

    def guncelle(self,seri_no,ad,agirlik,yapim_yil,yolcu_kapastesi):
        self.sorgu.execute("UPDATE YOLCUGEMISI SET ad=?,agirlik=?,yapim_yili=?,yolcu_kapasitesi=? WHERE seri_no=? ",(ad,agirlik,yapim_yil,yolcu_kapastesi,seri_no))   
        self.db.commit()

class petrolGemi(veriKontrol):
    def ekleme(self,seri_no,ad,agirlik,yapim_yili,petrol_kapasite):
        try:
            self.sorgu.execute('insert into PETROLGEMISI values(?,?,?,?,?)',(seri_no,ad,agirlik,yapim_yili,petrol_kapasite))
            self.db.commit()
        except sqlite3.IntegrityError:
            pass

    def silme(self,seri_no):
        self.sorgu.execute("Delete  from PETROLGEMISI where seri_no=?",(seri_no,))
        self.db.commit()

    def guncelle(self,seri_no,ad,agirlik,yapim_yili,petrol_kapasite):
        self.sorgu.execute("UPDATE PETROLGEMISI SET ad=?,agirlik=?,yapim_yili=?,petrol_kapasite=? WHERE seri_no=? ",(ad,agirlik,yapim_yili,petrol_kapasite,seri_no))   
        self.db.commit()
    

class konteynerGemi(veriKontrol):
    def ekleme(self,seri_no,ad,agirlik,yapim_yili,konteyner_sayisi,maks_agirlik):
        try:
            self.sorgu.execute('insert into KONTEYNERGEMISI values(?,?,?,?,?,?)',(seri_no,ad,agirlik,yapim_yili,konteyner_sayisi,maks_agirlik))
            self.db.commit()
        except sqlite3.IntegrityError:
            pass
    def silme(self,seri_no):
        self.sorgu.execute("Delete  from KONTEYNERGEMISI where seri_no=?",(seri_no,))
        self.db.commit()

    def guncelle(self,seri_no,ad,agirlik,yapim_yili,konteyner_sayisi,maks_agirlik):
        self.sorgu.execute("UPDATE KONTEYNERGEMISI SET ad=?,agirlik=?,yapim_yili=?,konteyner_sayisi=?,maks_agirlik=? WHERE seri_no=? ",(ad,agirlik,yapim_yili,konteyner_sayisi,maks_agirlik,seri_no))   
        self.db.commit()

class seferler(veriKontrol):
    def ekleme(self,sefer_id,yola_cikis_tarihi,donus_tarihi,cikis_limani):
        try:
            self.sorgu.execute('insert into SEFERLER values(?,?,?,?)',(sefer_id,yola_cikis_tarihi,donus_tarihi,cikis_limani))
            self.db.commit()
        except sqlite3.IntegrityError:
            pass
    def silme(self,sefer_id):
        self.sorgu.execute("Delete  from SEFERLER where sefer_id=?",(sefer_id,))
        self.db.commit()

    def guncelle(self,sefer_id,yola_cikis_tarihi,donus_tarihi,cikis_limani):
        self.sorgu.execute("UPDATE SEFERLER SET yola_cikis_tarihi=?,donus_tarihi=?,cikis_limani=? WHERE sefer_id=? ",(yola_cikis_tarihi,donus_tarihi,cikis_limani,sefer_id))   
        self.db.commit()

class liman(veriKontrol):
    def ekleme(self,liman_adi,liman_ulkesi,nufus,pasaport_sorgu,demirleme_ucret):
        try:
            self.sorgu.execute('insert into LIMANLAR values(?,?,?,?,?)',(liman_adi,liman_ulkesi,nufus,pasaport_sorgu,demirleme_ucret))
            self.db.commit()
        except sqlite3.IntegrityError:
            pass
    def silme(self,liman_adi):
        self.sorgu.execute("Delete  from LIMANLAR where liman_adi=?",(liman_adi,)) 
        self.db.commit()

    def guncelle(self,liman_adi,liman_ulkesi,nufus,pasaport_sorgu,demirleme_ucret):
        self.sorgu.execute("UPDATE LIMANLAR SET liman_ulkesi=?,nufus=?,pasaport_sorgu=?,demirleme_ucret=? WHERE liman_adi=? ",(liman_ulkesi,nufus,pasaport_sorgu,demirleme_ucret,liman_adi))   
        self.db.commit()


class kaptanlar(veriKontrol):
    def ekleme(self,kaptan_id,kaptan_ad,kaptan_soyad,kaptan_adres,kaptan_vatandaslik,kaptan_dogum_tarihi,kaptan_iseGiris,kaptan_lisans):
        try:
            self.sorgu.execute('insert into KAPTANLAR values(?,?,?,?,?,?,?,?)',(kaptan_id,kaptan_ad,kaptan_soyad,kaptan_adres,kaptan_vatandaslik,kaptan_dogum_tarihi,kaptan_iseGiris,kaptan_lisans))
            self.db.commit()
        except sqlite3.IntegrityError:
            pass
    def silme(self,kaptan_id):
        self.sorgu.execute("Delete  from KAPTANLAR where kaptan_id=?",(kaptan_id,))
        self.db.commit()

    def guncelle(self,kaptan_id,kaptan_ad,kaptan_soyad,kaptan_adres,kaptan_vatandaslik,kaptan_dogum_tarihi,kaptan_iseGiris,kaptan_lisans):
        self.sorgu.execute("UPDATE KAPTANLAR SET kaptan_ad=?,kaptan_soyad=?,kaptan_adres=?,kaptan_vatandaslik=?,kaptan_dogum_tarihi=?,kaptan_iseGiris=?,kaptan_lisans=? WHERE kaptan_id=? ",(kaptan_ad,kaptan_soyad,kaptan_adres,kaptan_vatandaslik,kaptan_dogum_tarihi,kaptan_iseGiris,kaptan_lisans,kaptan_id))   
        self.db.commit()

class murettebat(veriKontrol):
    def ekleme(self,murettebat_id,murettebat_ad,murettebat_soyad,murettebat_adres,murettebat_vatandaslik,murettebat_dogum_tarihi,murettebat_gorev,murettebat_iseGiris):
        try:
            self.sorgu.execute('insert into MURETTABAT values(?,?,?,?,?,?,?,?)',(murettebat_id,murettebat_ad,murettebat_soyad,murettebat_adres,murettebat_vatandaslik,murettebat_dogum_tarihi,murettebat_gorev,murettebat_iseGiris))
            self.db.commit()
        except sqlite3.IntegrityError:
            pass

    def silme(self,murettebat_id):
        self.sorgu.execute("Delete  from MURETTABAT where murettebat_id=?",(murettebat_id,))
        self.db.commit()

    def guncelle(self,murettebat_id,murettebat_ad,murettebat_soyad,murettebat_adres,murettebat_vatandaslik,murettebat_dogum_tarihi,murettebat_gorev,murettebat_iseGiris):
        self.sorgu.execute("UPDATE MURETTABAT SET murettebat_ad=?,murettebat_soyad=?,murettebat_adres=?,murettebat_vatandaslik=?,murettebat_dogum_tarihi=?,murettebat_gorev=?,murettebat_iseGiris=? WHERE murettebat_id=? ",
         (murettebat_ad,murettebat_soyad,murettebat_adres,murettebat_vatandaslik,murettebat_dogum_tarihi
        ,murettebat_gorev,murettebat_iseGiris,murettebat_id))  

        self.db.commit()




seferekletable=seferolustur("SEFEROLUSTUR")
yolcutable=yolcuGemi("YOLCUGEMISI")
konteynertable=konteynerGemi("KONTEYNERGEMISI")
petroltable=petrolGemi("PETROLGEMISI")
sefertable=seferler("SEFERLER")
limantable=liman("LIMANLAR")
kaptantable=kaptanlar("KAPTANLAR")
murettebattable=murettebat("MURETTABAT")







class Ui_MainWindow(object):

    def sefer_ekle_click_guncelle(self,sefer_id,kaptan_id,murettebat_id,gemi_seri_no,gidilecek_liman):
        
        if self.seferOlusturEkleC.isChecked() and self.seferOlusturGuncelleC.isChecked():
            return 
        
        if self.seferOlusturEkleC.isChecked():

            seferekletable.ekleme(sefer_id,kaptan_id,murettebat_id,gemi_seri_no,gidilecek_liman)                                                                #Yolcu gemileri
        if self.seferOlusturGuncelleC.isChecked():

            seferekletable.guncelle(sefer_id,kaptan_id,murettebat_id,gemi_seri_no,gidilecek_liman)
    
    def sefer_silme(self,sefer_id):

        seferekletable.silme(sefer_id)

    

    def Y_button_click_ekle_guncelle(self,seri_no,ad,agirlik,yapim_yil,yolcu_kapasitesi):
        
        if self.yolcuEkleCheck.isChecked() and self.yolcuGuncelleCheck.isChecked():
            return 
        
        if self.yolcuEkleCheck.isChecked():

            yolcutable.ekleme(seri_no,ad,agirlik,yapim_yil,yolcu_kapasitesi)                                                                #Yolcu gemileri
        if self.yolcuGuncelleCheck.isChecked():

            yolcutable.guncelle(seri_no,ad,agirlik,yapim_yil,yolcu_kapasitesi)
        
        
        
    def Y_button_click_sil(self,seri_no):

        yolcutable.silme(seri_no)
        
    def K_button_click_ekle_guncelle(self,seri_no,ad,agirlik,yapim_yili,konteyner_sayisi,maks_agirlik,):
    
        if self.konteynerEkleCheck.isChecked() and self.konteynerGuncelleCheck.isChecked():
            return 
        
        if self.konteynerEkleCheck.isChecked():

            konteynertable.ekleme(seri_no,ad,agirlik,yapim_yili,konteyner_sayisi,maks_agirlik)
                                                                                                                                    #Konteyner gemileri
        if self.konteynerGuncelleCheck.isChecked():
            konteynertable.guncelle(seri_no,ad,agirlik,yapim_yili,konteyner_sayisi,maks_agirlik)
            
    def K_button_click_sil(self,seri_no):

        konteynertable.silme(seri_no)

    def P_button_click_ekle_guncelle(self,seri_no,ad,agirlik,yapim_yili,petrol_kapasite):
    
        if self.petrolEkleCheck.isChecked() and self.petrolGuncelleCheck.isChecked():
            return 
        
        if self.petrolEkleCheck.isChecked():

            petroltable.ekleme(seri_no,ad,agirlik,yapim_yili,petrol_kapasite)

        if self.petrolGuncelleCheck.isChecked():
            petroltable.guncelle(seri_no,ad,agirlik,yapim_yili,petrol_kapasite)
            
    def P_button_click_sil(self,seri_no):
                                                                                                                    #Petrol gemileri
        petroltable.silme(seri_no)

    def S_button_click_ekle_guncelle(self,sefer_id,yola_cikis_tarihi,donus_tarihi,cikis_limani):
    
        if self.seferEkleCheck.isChecked() and self.seferGuncelleCheck.isChecked():
            return 
                                                                                                                            #Seferler
        if self.seferEkleCheck.isChecked():

            sefertable.ekleme(sefer_id,yola_cikis_tarihi,donus_tarihi,cikis_limani)

        if self.seferGuncelleCheck.isChecked():
            sefertable.guncelle(sefer_id,yola_cikis_tarihi,donus_tarihi,cikis_limani)
            
    def S_button_click_sil(self,seri_no):

        sefertable.silme(seri_no)


    def L_button_click_ekle_guncelle(self,liman_adi,liman_ulkesi,nufus,pasaport_sorgu,demirleme_ucret):
    
        if self.limanEkleCheck.isChecked() and self.limanGuncelleCheck.isChecked():
            return 
        
        if self.limanEkleCheck.isChecked():                                                                                     ####Liman

            limantable.ekleme(liman_adi,liman_ulkesi,nufus,pasaport_sorgu,demirleme_ucret)

        if self.limanGuncelleCheck.isChecked():
            limantable.guncelle(liman_adi,liman_ulkesi,nufus,pasaport_sorgu,demirleme_ucret)
            
    def L_button_click_sil(self,liman_adi):

        limantable.silme(liman_adi)


    def Kapt_button_click_ekle_guncelle(self,kaptan_id,kaptan_ad,kaptan_soyad,kaptan_adres,kaptan_vatandaslik,kaptan_dogum_tarihi,kaptan_iseGiris,kaptan_lisans):
    
        if self.kaptanEkleCheck.isChecked() and self.kaptanGuncelleCheck.isChecked():
            return 
        
        if self.kaptanEkleCheck.isChecked():                                                                                    #Kaptanlar

            kaptantable.ekleme(kaptan_id,kaptan_ad,kaptan_soyad,kaptan_adres,kaptan_vatandaslik,kaptan_dogum_tarihi,kaptan_iseGiris,kaptan_lisans)

        if self.kaptanGuncelleCheck.isChecked():
            kaptantable.guncelle(kaptan_id,kaptan_ad,kaptan_soyad,kaptan_adres,kaptan_vatandaslik,kaptan_dogum_tarihi,kaptan_iseGiris,kaptan_lisans)
            
    def Kapt_button_click_sil(self,kaptan_id):

        kaptantable.silme(kaptan_id)

    def M_button_click_ekle_guncelle(self,murettebat_id,murettebat_ad,murettebat_soyad,murettebat_adres,murettebat_vatandaslik,murettebat_dogum_tarihi,murettebat_gorev,murettebat_iseGiris):
    
        if self.murettabatEkleCheck.isChecked() and self.murettabatGuncelleCheck.isChecked():
            return 
        
        if self.murettabatEkleCheck.isChecked():                                                                                   

            murettebattable.ekleme(murettebat_id,murettebat_ad,murettebat_soyad,murettebat_adres,murettebat_vatandaslik,murettebat_dogum_tarihi,murettebat_gorev,murettebat_iseGiris)

        if self.murettabatGuncelleCheck.isChecked():
            murettebattable.guncelle(murettebat_id,murettebat_ad,murettebat_soyad,murettebat_adres,murettebat_vatandaslik,murettebat_dogum_tarihi,murettebat_gorev,murettebat_iseGiris)
            
    def M_button_click_sil(self,murettebat_id):

        murettebattable.silme(murettebat_id)

    def veriTabaniGoster_clicked(self):
        self.second_window = SecondWindow()
    
        
        

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1116, 890)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(640, 230, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(630, 0, 121, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(590, 520, 61, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(140, 520, 101, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(90, 230, 111, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1000, 530, 81, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(100, 10, 71, 16))
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(10, 70, 21, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(10, 100, 47, 13))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(0, 130, 51, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(0, 160, 81, 16))
        self.label_14.setObjectName("label_14")
        self.seri_noYolcu = QtWidgets.QLineEdit(self.centralwidget)
        self.seri_noYolcu.setGeometry(QtCore.QRect(80, 40, 113, 16))
        self.seri_noYolcu.setObjectName("seri_noYolcu")
        self.adYolcu = QtWidgets.QLineEdit(self.centralwidget)
        self.adYolcu.setGeometry(QtCore.QRect(80, 70, 113, 16))
        self.adYolcu.setObjectName("adYolcu")
        self.yolcuAgirlik = QtWidgets.QLineEdit(self.centralwidget)
        self.yolcuAgirlik.setGeometry(QtCore.QRect(80, 100, 113, 16))
        self.yolcuAgirlik.setObjectName("yolcuAgirlik")
        self.yolcuKapasite = QtWidgets.QLineEdit(self.centralwidget)
        self.yolcuKapasite.setGeometry(QtCore.QRect(80, 160, 113, 16))
        self.yolcuKapasite.setObjectName("yolcuKapasite")
        self.yolcuGemiEklemeButon = QtWidgets.QPushButton(self.centralwidget)
        self.yolcuGemiEklemeButon.setGeometry(QtCore.QRect(100, 190, 75, 23))
        self.yolcuGemiEklemeButon.setObjectName("yolcuGemiEklemeButon")

        self.yolcuGemiEklemeButon.clicked.connect(lambda: self.Y_button_click_ekle_guncelle(self.seri_noYolcu.text(),self.adYolcu.text(),self.yolcuAgirlik.text(),self.yolcuYapimYili.text(),self.yolcuKapasite.text()))        #Yolcu gemisi ekleme/güncelleme 

        self.yolcuSeriNoSilButon = QtWidgets.QPushButton(self.centralwidget)
        self.yolcuSeriNoSilButon.setGeometry(QtCore.QRect(280, 80, 75, 23))
        self.yolcuSeriNoSilButon.setObjectName("yolcuSeriNoSilButon")

        self.yolcuSeriNoSilButon.clicked.connect(lambda : self.Y_button_click_sil(self.yolcuSeriNoSil.text()))              

        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(300, 30, 47, 13))
        self.label_15.setObjectName("label_15")
        self.yolcuSeriNoSil = QtWidgets.QLineEdit(self.centralwidget)
        self.yolcuSeriNoSil.setGeometry(QtCore.QRect(280, 50, 101, 16))
        self.yolcuSeriNoSil.setObjectName("yolcuSeriNoSil")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(570, 40, 47, 13))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(590, 60, 47, 13))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(580, 80, 47, 13))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(560, 110, 47, 13))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(530, 140, 101, 20))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(530, 170, 71, 20))
        self.label_21.setObjectName("label_21")
        self.seriNoKonteyner = QtWidgets.QLineEdit(self.centralwidget)
        self.seriNoKonteyner.setGeometry(QtCore.QRect(620, 40, 113, 16))
        self.seriNoKonteyner.setObjectName("seriNoKonteyner")
        self.adKonteyner = QtWidgets.QLineEdit(self.centralwidget)
        self.adKonteyner.setGeometry(QtCore.QRect(620, 60, 113, 16))
        self.adKonteyner.setObjectName("adKonteyner")
        self.agirlikKonteyner = QtWidgets.QLineEdit(self.centralwidget)
        self.agirlikKonteyner.setGeometry(QtCore.QRect(620, 80, 113, 16))
        self.agirlikKonteyner.setObjectName("agirlikKonteyner")
        self.konteynerSayisi = QtWidgets.QLineEdit(self.centralwidget)
        self.konteynerSayisi.setGeometry(QtCore.QRect(620, 140, 113, 16))
        self.konteynerSayisi.setObjectName("konteynerSayisi")
        self.maksAgirlikKonteyner = QtWidgets.QLineEdit(self.centralwidget)
        self.maksAgirlikKonteyner.setGeometry(QtCore.QRect(620, 170, 113, 16))
        self.maksAgirlikKonteyner.setObjectName("maksAgirlikKonteyner")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(10, 260, 47, 13))
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(10, 290, 47, 13))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(10, 310, 47, 13))
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(10, 340, 51, 20))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.centralwidget)
        self.label_26.setGeometry(QtCore.QRect(10, 380, 81, 20))
        self.label_26.setObjectName("label_26")
        self.seriNoPetrol = QtWidgets.QLineEdit(self.centralwidget)
        self.seriNoPetrol.setGeometry(QtCore.QRect(90, 260, 113, 16))
        self.seriNoPetrol.setObjectName("seriNoPetrol")
        self.adPetrol = QtWidgets.QLineEdit(self.centralwidget)
        self.adPetrol.setGeometry(QtCore.QRect(90, 290, 113, 16))
        self.adPetrol.setObjectName("adPetrol")
        self.agirlikPetrol = QtWidgets.QLineEdit(self.centralwidget)
        self.agirlikPetrol.setGeometry(QtCore.QRect(90, 320, 113, 16))
        self.agirlikPetrol.setObjectName("agirlikPetrol")
        self.petrolKapasite = QtWidgets.QLineEdit(self.centralwidget)
        self.petrolKapasite.setGeometry(QtCore.QRect(90, 380, 113, 16))
        self.petrolKapasite.setObjectName("petrolKapasite")
        self.KonteynerEkleButon = QtWidgets.QPushButton(self.centralwidget)
        self.KonteynerEkleButon.setGeometry(QtCore.QRect(640, 200, 75, 23))
        self.KonteynerEkleButon.setObjectName("KonteynerEkleButon")

        self.KonteynerEkleButon.clicked.connect(lambda: self.K_button_click_ekle_guncelle(self.seriNoKonteyner.text(),self.adKonteyner.text(),self.agirlikKonteyner.text(),
                                                                                          self.yapimYilikonteyner.text(),self.konteynerSayisi.text(),self.maksAgirlikKonteyner.text()))

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(780, 40, 47, 13))
        self.label.setObjectName("label")
        self.konteynerSeriNoSil = QtWidgets.QLineEdit(self.centralwidget)
        self.konteynerSeriNoSil.setGeometry(QtCore.QRect(750, 60, 113, 16))
        self.konteynerSeriNoSil.setObjectName("konteynerSeriNoSil")
        self.konteynerSeriNoSilButon = QtWidgets.QPushButton(self.centralwidget)
        self.konteynerSeriNoSilButon.setGeometry(QtCore.QRect(770, 80, 75, 23))
        self.konteynerSeriNoSilButon.setObjectName("konteynerSeriNoSilButon")

        self.konteynerSeriNoSilButon.clicked.connect(lambda : self.K_button_click_sil(self.konteynerSeriNoSil.text()))

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(310, 240, 47, 13))
        self.label_9.setObjectName("label_9")
        self.petrolSeriNoSil = QtWidgets.QLineEdit(self.centralwidget)
        self.petrolSeriNoSil.setGeometry(QtCore.QRect(270, 270, 111, 16))
        self.petrolSeriNoSil.setObjectName("petrolSeriNoSil")
        self.petrolSilmeButon = QtWidgets.QPushButton(self.centralwidget)
        self.petrolSilmeButon.setGeometry(QtCore.QRect(290, 300, 75, 23))
        self.petrolSilmeButon.setObjectName("petrolSilmeButon")
        self.petrolEkle = QtWidgets.QPushButton(self.centralwidget)
        self.petrolEkle.setGeometry(QtCore.QRect(110, 410, 75, 23))
        self.petrolEkle.setObjectName("petrolEkle")

        self.petrolEkle.clicked.connect(lambda: self.P_button_click_ekle_guncelle(self.seriNoPetrol.text(),self.adPetrol.text(),self.agirlikPetrol.text(),self.yapimYiliPetrol.text(),self.petrolKapasite.text()))

        self.petrolSilmeButon.clicked.connect(lambda : self.P_button_click_sil(self.petrolSeriNoSil.text()))

        self.label_27 = QtWidgets.QLabel(self.centralwidget)
        self.label_27.setGeometry(QtCore.QRect(560, 260, 47, 13))
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.centralwidget)
        self.label_28.setGeometry(QtCore.QRect(560, 280, 51, 16))
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        self.label_29.setGeometry(QtCore.QRect(550, 300, 71, 20))
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.centralwidget)
        self.label_30.setGeometry(QtCore.QRect(550, 330, 71, 20))
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.centralwidget)
        self.label_31.setGeometry(QtCore.QRect(520, 360, 101, 20))
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.centralwidget)
        self.label_32.setGeometry(QtCore.QRect(520, 390, 101, 20))
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.centralwidget)
        self.label_33.setGeometry(QtCore.QRect(540, 420, 91, 20))
        self.label_33.setObjectName("label_33")
        self.label_34 = QtWidgets.QLabel(self.centralwidget)
        self.label_34.setGeometry(QtCore.QRect(550, 450, 81, 20))
        self.label_34.setObjectName("label_34")
        self.kaptanID = QtWidgets.QLineEdit(self.centralwidget)
        self.kaptanID.setGeometry(QtCore.QRect(620, 260, 113, 16))
        self.kaptanID.setObjectName("kaptanID")
        self.kaptanAd = QtWidgets.QLineEdit(self.centralwidget)
        self.kaptanAd.setGeometry(QtCore.QRect(620, 280, 113, 16))
        self.kaptanAd.setObjectName("kaptanAd")
        self.kaptanSoyad = QtWidgets.QLineEdit(self.centralwidget)
        self.kaptanSoyad.setGeometry(QtCore.QRect(620, 310, 113, 16))
        self.kaptanSoyad.setObjectName("kaptanSoyad")
        self.kaptanAdres = QtWidgets.QLineEdit(self.centralwidget)
        self.kaptanAdres.setGeometry(QtCore.QRect(620, 340, 113, 16))
        self.kaptanAdres.setObjectName("kaptanAdres")
        self.kaptanVatandaslik = QtWidgets.QLineEdit(self.centralwidget)
        self.kaptanVatandaslik.setGeometry(QtCore.QRect(620, 360, 113, 16))
        self.kaptanVatandaslik.setObjectName("kaptanVatandaslik")
        self.kaptanIseGrs = QtWidgets.QLineEdit(self.centralwidget)
        self.kaptanIseGrs.setGeometry(QtCore.QRect(620, 430, 113, 16))
        self.kaptanIseGrs.setObjectName("kaptanIseGrs")
        self.kaptanLisans = QtWidgets.QLineEdit(self.centralwidget)
        self.kaptanLisans.setGeometry(QtCore.QRect(620, 460, 113, 16))
        self.kaptanLisans.setObjectName("kaptanLisans")
        self.kaptanEkleButon = QtWidgets.QPushButton(self.centralwidget)
        self.kaptanEkleButon.setGeometry(QtCore.QRect(640, 480, 75, 23))
        self.kaptanEkleButon.setObjectName("kaptanEkleButon")
        self.label_35 = QtWidgets.QLabel(self.centralwidget)
        self.label_35.setGeometry(QtCore.QRect(770, 240, 51, 16))
        self.label_35.setObjectName("label_35")
        self.kaptanIDsILME = QtWidgets.QLineEdit(self.centralwidget)
        self.kaptanIDsILME.setGeometry(QtCore.QRect(750, 260, 113, 16))
        self.kaptanIDsILME.setObjectName("kaptanIDsILME")
        self.kaptanSilmeButon = QtWidgets.QPushButton(self.centralwidget)
        self.kaptanSilmeButon.setGeometry(QtCore.QRect(770, 280, 75, 23))
        self.kaptanSilmeButon.setObjectName("kaptanSilmeButon")


        self.kaptanEkleButon.clicked.connect(lambda: self.Kapt_button_click_ekle_guncelle(self.kaptanID.text(),self.kaptanAd.text(),self.kaptanSoyad.text(),self.kaptanAdres.text(),
                                                                                          self.kaptanVatandaslik.text(),self.kaptanDogumTarihi.text(),self.kaptanIseGrs.text(),self.kaptanLisans.text()))

        self.kaptanSilmeButon.clicked.connect(lambda:self.Kapt_button_click_sil(self.kaptanIDsILME.text()))

        self.label_36 = QtWidgets.QLabel(self.centralwidget)
        self.label_36.setGeometry(QtCore.QRect(10, 560, 71, 16))
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.centralwidget)
        self.label_37.setGeometry(QtCore.QRect(10, 590, 71, 16))
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.centralwidget)
        self.label_38.setGeometry(QtCore.QRect(10, 620, 91, 16))
        self.label_38.setObjectName("label_38")
        self.label_39 = QtWidgets.QLabel(self.centralwidget)
        self.label_39.setGeometry(QtCore.QRect(10, 650, 91, 16))
        self.label_39.setObjectName("label_39")
        self.label_40 = QtWidgets.QLabel(self.centralwidget)
        self.label_40.setGeometry(QtCore.QRect(10, 680, 121, 16))
        self.label_40.setObjectName("label_40")
        self.label_41 = QtWidgets.QLabel(self.centralwidget)
        self.label_41.setGeometry(QtCore.QRect(10, 710, 121, 16))
        self.label_41.setObjectName("label_41")
        self.label_42 = QtWidgets.QLabel(self.centralwidget)
        self.label_42.setGeometry(QtCore.QRect(10, 740, 121, 16))
        self.label_42.setObjectName("label_42")
        self.label_43 = QtWidgets.QLabel(self.centralwidget)
        self.label_43.setGeometry(QtCore.QRect(10, 770, 111, 16))
        self.label_43.setObjectName("label_43")
        self.murettebatADRES = QtWidgets.QLineEdit(self.centralwidget)
        self.murettebatADRES.setGeometry(QtCore.QRect(130, 650, 113, 16))
        self.murettebatADRES.setObjectName("murettebatADRES")
        self.murettebatVatandaslik = QtWidgets.QLineEdit(self.centralwidget)
        self.murettebatVatandaslik.setGeometry(QtCore.QRect(130, 680, 113, 16))
        self.murettebatVatandaslik.setObjectName("murettebatVatandaslik")
        self.murettebatSOYAD = QtWidgets.QLineEdit(self.centralwidget)
        self.murettebatSOYAD.setGeometry(QtCore.QRect(130, 620, 113, 16))
        self.murettebatSOYAD.setObjectName("murettebatSOYAD")
        self.murettebatAD = QtWidgets.QLineEdit(self.centralwidget)
        self.murettebatAD.setGeometry(QtCore.QRect(130, 590, 113, 16))
        self.murettebatAD.setObjectName("murettebatAD")
        self.murettebatID = QtWidgets.QLineEdit(self.centralwidget)
        self.murettebatID.setGeometry(QtCore.QRect(130, 560, 113, 16))
        self.murettebatID.setObjectName("murettebatID")
        self.murettebatGorev = QtWidgets.QLineEdit(self.centralwidget)
        self.murettebatGorev.setGeometry(QtCore.QRect(130, 740, 113, 16))
        self.murettebatGorev.setObjectName("murettebatGorev")
        self.murettebatISEGIRIS = QtWidgets.QLineEdit(self.centralwidget)
        self.murettebatISEGIRIS.setGeometry(QtCore.QRect(130, 770, 113, 16))
        self.murettebatISEGIRIS.setObjectName("murettebatISEGIRIS")
        self.murettebatEKLEBUTON = QtWidgets.QPushButton(self.centralwidget)
        self.murettebatEKLEBUTON.setGeometry(QtCore.QRect(150, 800, 75, 23))
        self.murettebatEKLEBUTON.setObjectName("murettebatEKLEBUTON")
        self.label_44 = QtWidgets.QLabel(self.centralwidget)
        self.label_44.setGeometry(QtCore.QRect(330, 550, 81, 16))
        self.label_44.setObjectName("label_44")
        self.murettebatIDsilme = QtWidgets.QLineEdit(self.centralwidget)
        self.murettebatIDsilme.setGeometry(QtCore.QRect(310, 570, 113, 16))
        self.murettebatIDsilme.setObjectName("murettebatIDsilme")
        self.murettebatSilButon = QtWidgets.QPushButton(self.centralwidget)
        self.murettebatSilButon.setGeometry(QtCore.QRect(320, 590, 75, 23))
        self.murettebatSilButon.setObjectName("murettebatSilButon")

        self.murettebatEKLEBUTON.clicked.connect(lambda : self.M_button_click_ekle_guncelle(self.murettebatID.text(),self.murettebatAD.text(),self.murettebatSOYAD.text(),self.murettebatADRES.text(),
                                                 self.murettebatVatandaslik.text(),self.murettebatDogumTarihi.text(),self.murettebatGorev.text(),self.murettebatISEGIRIS.text()))
        
        self.murettebatSilButon.clicked.connect(lambda:self.M_button_click_sil(self.murettebatIDsilme.text()))

        self.label_45 = QtWidgets.QLabel(self.centralwidget)
        self.label_45.setGeometry(QtCore.QRect(490, 560, 47, 13))
        self.label_45.setObjectName("label_45")
        self.label_46 = QtWidgets.QLabel(self.centralwidget)
        self.label_46.setGeometry(QtCore.QRect(490, 590, 61, 16))
        self.label_46.setObjectName("label_46")
        self.label_47 = QtWidgets.QLabel(self.centralwidget)
        self.label_47.setGeometry(QtCore.QRect(500, 630, 47, 13))
        self.label_47.setObjectName("label_47")
        self.label_48 = QtWidgets.QLabel(self.centralwidget)
        self.label_48.setGeometry(QtCore.QRect(470, 660, 81, 20))
        self.label_48.setObjectName("label_48")
        self.label_49 = QtWidgets.QLabel(self.centralwidget)
        self.label_49.setGeometry(QtCore.QRect(470, 690, 81, 20))
        self.label_49.setObjectName("label_49")
        self.limanAD = QtWidgets.QLineEdit(self.centralwidget)
        self.limanAD.setGeometry(QtCore.QRect(550, 560, 113, 16))
        self.limanAD.setObjectName("limanAD")
        self.limanULKE = QtWidgets.QLineEdit(self.centralwidget)
        self.limanULKE.setGeometry(QtCore.QRect(550, 590, 113, 16))
        self.limanULKE.setObjectName("limanULKE")
        self.limanNUFUS = QtWidgets.QLineEdit(self.centralwidget)
        self.limanNUFUS.setGeometry(QtCore.QRect(550, 630, 113, 16))
        self.limanNUFUS.setObjectName("limanNUFUS")
        self.limanPasaportSorgu = QtWidgets.QLineEdit(self.centralwidget)
        self.limanPasaportSorgu.setGeometry(QtCore.QRect(550, 660, 113, 16))
        self.limanPasaportSorgu.setObjectName("limanPasaportSorgu")
        self.limanDemirlemeUcret = QtWidgets.QLineEdit(self.centralwidget)
        self.limanDemirlemeUcret.setGeometry(QtCore.QRect(550, 690, 113, 16))
        self.limanDemirlemeUcret.setObjectName("limanDemirlemeUcret")
        self.limanEkleButon = QtWidgets.QPushButton(self.centralwidget)
        self.limanEkleButon.setGeometry(QtCore.QRect(560, 720, 75, 23))
        self.limanEkleButon.setObjectName("limanEkleButon")
        self.label_50 = QtWidgets.QLabel(self.centralwidget)
        self.label_50.setGeometry(QtCore.QRect(740, 550, 47, 13))
        self.label_50.setObjectName("label_50")
        self.limanAdiSil = QtWidgets.QLineEdit(self.centralwidget)
        self.limanAdiSil.setGeometry(QtCore.QRect(720, 570, 113, 16))
        self.limanAdiSil.setObjectName("limanAdiSil")
        self.limanSilButon = QtWidgets.QPushButton(self.centralwidget)
        self.limanSilButon.setGeometry(QtCore.QRect(740, 590, 75, 23))
        self.limanSilButon.setObjectName("limanSilButon")

        self.limanEkleButon.clicked.connect(lambda: self.L_button_click_ekle_guncelle(self.limanAD.text(),self.limanULKE.text(),self.limanNUFUS.text(),self.limanPasaportSorgu.text(),self.limanDemirlemeUcret.text()))
        self.limanSilButon.clicked.connect(lambda : self.L_button_click_sil(self.limanAdiSil.text()))
        

        self.label_51 = QtWidgets.QLabel(self.centralwidget)
        self.label_51.setGeometry(QtCore.QRect(880, 570, 47, 13))
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.centralwidget)
        self.label_52.setGeometry(QtCore.QRect(870, 600, 81, 20))
        self.label_52.setObjectName("label_52")
        self.label_53 = QtWidgets.QLabel(self.centralwidget)
        self.label_53.setGeometry(QtCore.QRect(870, 630, 81, 20))
        self.label_53.setObjectName("label_53")
        self.label_54 = QtWidgets.QLabel(self.centralwidget)
        self.label_54.setGeometry(QtCore.QRect(870, 680, 71, 20))
        self.label_54.setObjectName("label_54")
        self.seferID = QtWidgets.QLineEdit(self.centralwidget)
        self.seferID.setGeometry(QtCore.QRect(950, 570, 113, 16))
        self.seferID.setObjectName("seferID")
        self.seferLiman = QtWidgets.QLineEdit(self.centralwidget)
        self.seferLiman.setGeometry(QtCore.QRect(950, 680, 113, 16))
        self.seferLiman.setObjectName("seferLiman")
        self.sefeEkleButon = QtWidgets.QPushButton(self.centralwidget)
        self.sefeEkleButon.setGeometry(QtCore.QRect(960, 710, 75, 23))
        self.sefeEkleButon.setObjectName("sefeEkleButon")
        self.label_55 = QtWidgets.QLabel(self.centralwidget)
        self.label_55.setGeometry(QtCore.QRect(970, 770, 47, 13))
        self.label_55.setObjectName("label_55")
        self.sefeIDsilme = QtWidgets.QLineEdit(self.centralwidget)
        self.sefeIDsilme.setGeometry(QtCore.QRect(940, 790, 113, 20))
        self.sefeIDsilme.setObjectName("sefeIDsilme")
        self.seferSILBUTON = QtWidgets.QPushButton(self.centralwidget)
        self.seferSILBUTON.setGeometry(QtCore.QRect(960, 820, 75, 23))
        self.seferSILBUTON.setObjectName("seferSILBUTON")

        self.sefeEkleButon.clicked.connect(lambda: self.S_button_click_ekle_guncelle(self.seferID.text(),self.seferYOLACIKIS.text(),self.sefeDonusTarih.text(),self.seferLiman.text()))

        self.seferSILBUTON.clicked.connect(lambda : self.S_button_click_sil(self.sefeIDsilme.text()))


        self.yolcuGuncelleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.yolcuGuncelleCheck.setGeometry(QtCore.QRect(190, 190, 70, 17))
        self.yolcuGuncelleCheck.setObjectName("yolcuGuncelleCheck")
        self.yolcuEkleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.yolcuEkleCheck.setGeometry(QtCore.QRect(10, 190, 70, 17))
        self.yolcuEkleCheck.setObjectName("yolcuEkleCheck")
        self.petrolEkleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.petrolEkleCheck.setGeometry(QtCore.QRect(20, 410, 70, 17))
        self.petrolEkleCheck.setObjectName("petrolEkleCheck")
        self.petrolGuncelleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.petrolGuncelleCheck.setGeometry(QtCore.QRect(200, 410, 70, 17))
        self.petrolGuncelleCheck.setObjectName("petrolGuncelleCheck")
        self.murettabatEkleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.murettabatEkleCheck.setGeometry(QtCore.QRect(60, 800, 70, 17))
        self.murettabatEkleCheck.setObjectName("murettabatEkleCheck")
        self.murettabatGuncelleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.murettabatGuncelleCheck.setGeometry(QtCore.QRect(240, 800, 70, 17))
        self.murettabatGuncelleCheck.setObjectName("murettabatGuncelleCheck")
        self.limanEkleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.limanEkleCheck.setGeometry(QtCore.QRect(480, 720, 70, 17))
        self.limanEkleCheck.setObjectName("limanEkleCheck")
        self.limanGuncelleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.limanGuncelleCheck.setGeometry(QtCore.QRect(650, 720, 70, 17))
        self.limanGuncelleCheck.setObjectName("limanGuncelleCheck")
        self.kaptanEkleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.kaptanEkleCheck.setGeometry(QtCore.QRect(550, 480, 70, 17))
        self.kaptanEkleCheck.setObjectName("kaptanEkleCheck")
        self.kaptanGuncelleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.kaptanGuncelleCheck.setGeometry(QtCore.QRect(730, 480, 70, 17))
        self.kaptanGuncelleCheck.setObjectName("kaptanGuncelleCheck")
        self.konteynerEkleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.konteynerEkleCheck.setGeometry(QtCore.QRect(560, 200, 70, 17))
        self.konteynerEkleCheck.setObjectName("konteynerEkleCheck")
        self.konteynerGuncelleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.konteynerGuncelleCheck.setGeometry(QtCore.QRect(730, 200, 70, 17))
        self.konteynerGuncelleCheck.setObjectName("konteynerGuncelleCheck")
        self.seferEkleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.seferEkleCheck.setGeometry(QtCore.QRect(860, 710, 70, 17))
        self.seferEkleCheck.setObjectName("seferEkleCheck")
        self.seferGuncelleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.seferGuncelleCheck.setGeometry(QtCore.QRect(1040, 710, 70, 17))
        self.seferGuncelleCheck.setObjectName("seferGuncelleCheck")
        self.veriTabaniGoster = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.veriTabaniGoster.setGeometry(QtCore.QRect(880, 360, 191, 41))
        self.veriTabaniGoster.setObjectName("veriTabaniGoster")
        self.veriTabaniGoster.clicked.connect(self.veriTabaniGoster_clicked)
        self.label_56 = QtWidgets.QLabel(self.centralwidget)
        self.label_56.setGeometry(QtCore.QRect(970, 10, 141, 20))
        self.label_56.setObjectName("label_56")
        self.label_57 = QtWidgets.QLabel(self.centralwidget)
        self.label_57.setGeometry(QtCore.QRect(900, 40, 47, 13))
        self.label_57.setObjectName("label_57")
        self.label_58 = QtWidgets.QLabel(self.centralwidget)
        self.label_58.setGeometry(QtCore.QRect(890, 80, 51, 16))
        self.label_58.setObjectName("label_58")
        self.label_59 = QtWidgets.QLabel(self.centralwidget)
        self.label_59.setGeometry(QtCore.QRect(870, 110, 71, 20))
        self.label_59.setObjectName("label_59")
        self.label_60 = QtWidgets.QLabel(self.centralwidget)
        self.label_60.setGeometry(QtCore.QRect(870, 150, 71, 20))
        self.label_60.setObjectName("label_60")
        self.label_61 = QtWidgets.QLabel(self.centralwidget)
        self.label_61.setGeometry(QtCore.QRect(870, 180, 71, 20))
        self.label_61.setObjectName("label_61")
        self.seferOlusturSefer_id = QtWidgets.QLineEdit(self.centralwidget)
        self.seferOlusturSefer_id.setGeometry(QtCore.QRect(950, 40, 113, 16))
        self.seferOlusturSefer_id.setObjectName("seferOlusturSefer_id")
        self.seferOlusturKaptan_id = QtWidgets.QLineEdit(self.centralwidget)
        self.seferOlusturKaptan_id.setGeometry(QtCore.QRect(950, 80, 113, 16))
        self.seferOlusturKaptan_id.setObjectName("seferOlusturKaptan_id")
        self.seferOlusturMurettabat_id = QtWidgets.QLineEdit(self.centralwidget)
        self.seferOlusturMurettabat_id.setGeometry(QtCore.QRect(950, 110, 113, 16))
        self.seferOlusturMurettabat_id.setObjectName("seferOlusturMurettabat_id")
        self.seferOlusturGemi_seri_no = QtWidgets.QLineEdit(self.centralwidget)
        self.seferOlusturGemi_seri_no.setGeometry(QtCore.QRect(950, 150, 113, 16))
        self.seferOlusturGemi_seri_no.setObjectName("seferOlusturGemi_seri_no")
        self.seferOlusturGidilecek_liman = QtWidgets.QLineEdit(self.centralwidget)
        self.seferOlusturGidilecek_liman.setGeometry(QtCore.QRect(950, 180, 113, 16))
        self.seferOlusturGidilecek_liman.setObjectName("seferOlusturGidilecek_liman")
        self.seferOlusturOnaylaButon = QtWidgets.QPushButton(self.centralwidget)
        self.seferOlusturOnaylaButon.setGeometry(QtCore.QRect(960, 210, 75, 23))
        self.seferOlusturOnaylaButon.setObjectName("seferOlusturOnaylaButon")
        self.seferOlusturEkleC = QtWidgets.QCheckBox(self.centralwidget)
        self.seferOlusturEkleC.setGeometry(QtCore.QRect(890, 210, 70, 17))
        self.seferOlusturEkleC.setObjectName("seferOlusturEkleC")
        self.seferOlusturGuncelleC = QtWidgets.QCheckBox(self.centralwidget)
        self.seferOlusturGuncelleC.setGeometry(QtCore.QRect(1040, 210, 70, 17))
        self.seferOlusturGuncelleC.setObjectName("seferOlusturGuncelleC")       
        self.label_62 = QtWidgets.QLabel(self.centralwidget)
        self.label_62.setGeometry(QtCore.QRect(970, 260, 71, 16))
        self.label_62.setObjectName("label_62")
        self.label_63 = QtWidgets.QLabel(self.centralwidget)
        self.label_63.setGeometry(QtCore.QRect(900, 280, 47, 13))
        self.label_63.setObjectName("label_63")
        self.seferOlusturSilmeSefer_id = QtWidgets.QLineEdit(self.centralwidget)
        self.seferOlusturSilmeSefer_id.setGeometry(QtCore.QRect(950, 280, 113, 16))
        self.seferOlusturSilmeSefer_id.setObjectName("seferOlusturSilmeSefer_id")
        self.seferOlusturSilmeButon = QtWidgets.QPushButton(self.centralwidget)
        self.seferOlusturSilmeButon.setGeometry(QtCore.QRect(970, 310, 75, 23))
        self.seferOlusturSilmeButon.setObjectName("seferOlusturSilmeButon")

        self.seferOlusturOnaylaButon.clicked.connect(lambda: self.sefer_ekle_click_guncelle(self.seferOlusturSefer_id.text(),
self.seferOlusturKaptan_id.text(),self.seferOlusturMurettabat_id.text(),self.seferOlusturGemi_seri_no.text(),self.seferOlusturGidilecek_liman.text()))
        
        self.seferOlusturSilmeButon.clicked.connect(lambda : self.sefer_silme(self.seferOlusturSilmeSefer_id.text()))

        self.yolcuYapimYili = QtWidgets.QDateEdit(self.centralwidget)
        self.yolcuYapimYili.setGeometry(QtCore.QRect(80, 130, 110, 21))
        self.yolcuYapimYili.setObjectName("yolcuYapimYili")
        self.yapimYiliPetrol = QtWidgets.QDateEdit(self.centralwidget)
        self.yapimYiliPetrol.setGeometry(QtCore.QRect(90, 350, 110, 16))
        self.yapimYiliPetrol.setObjectName("yapimYiliPetrol")
        self.yapimYilikonteyner = QtWidgets.QDateEdit(self.centralwidget)
        self.yapimYilikonteyner.setGeometry(QtCore.QRect(620, 110, 110, 16))
        self.yapimYilikonteyner.setObjectName("yapimYilikonteyner")
        self.murettebatDogumTarihi = QtWidgets.QDateEdit(self.centralwidget)
        self.murettebatDogumTarihi.setGeometry(QtCore.QRect(130, 710, 110, 16))
        self.murettebatDogumTarihi.setObjectName("murettebatDogumTarihi")
        self.kaptanDogumTarihi = QtWidgets.QDateEdit(self.centralwidget)
        self.kaptanDogumTarihi.setGeometry(QtCore.QRect(620, 390, 110, 21))
        self.kaptanDogumTarihi.setObjectName("kaptanDogumTarihi")
        self.seferYOLACIKIS = QtWidgets.QDateEdit(self.centralwidget)
        self.seferYOLACIKIS.setGeometry(QtCore.QRect(950, 600, 110, 21))
        self.seferYOLACIKIS.setObjectName("seferYOLACIKIS")
        self.sefeDonusTarih = QtWidgets.QDateEdit(self.centralwidget)
        self.sefeDonusTarih.setGeometry(QtCore.QRect(950, 640, 110, 21))
        self.sefeDonusTarih.setObjectName("sefeDonusTarih")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KONTROL ARAYUZU"))
        self.label_2.setText(_translate("MainWindow", "KAPTANLAR"))
        self.label_3.setText(_translate("MainWindow", "KONTEYNER GEMISI"))
        self.label_4.setText(_translate("MainWindow", "LIMAN"))
        self.label_5.setText(_translate("MainWindow", "MURETTABAT"))
        self.label_6.setText(_translate("MainWindow", "PETROL GEMISI"))
        self.label_7.setText(_translate("MainWindow", "SEFERLER"))
        self.label_8.setText(_translate("MainWindow", "YOLCU GEMISI"))
        self.label_10.setText(_translate("MainWindow", "seri_no"))
        self.label_11.setText(_translate("MainWindow", "ad"))
        self.label_12.setText(_translate("MainWindow", "agirlik"))
        self.label_13.setText(_translate("MainWindow", "yapim_yili"))
        self.label_14.setText(_translate("MainWindow", "yolcu_kapasitesi"))
        self.yolcuGemiEklemeButon.setText(_translate("MainWindow", "ONAYLA"))
        self.yolcuSeriNoSilButon.setText(_translate("MainWindow", "SIL"))
        self.label_15.setText(_translate("MainWindow", "seri_no"))
        self.label_16.setText(_translate("MainWindow", "seri_no"))
        self.label_17.setText(_translate("MainWindow", "ad"))
        self.label_18.setText(_translate("MainWindow", "agirlik"))
        self.label_19.setText(_translate("MainWindow", "yapim_yili"))
        self.label_20.setText(_translate("MainWindow", "konteyner_sayisi"))
        self.label_21.setText(_translate("MainWindow", "maks_agirlik"))
        self.label_22.setText(_translate("MainWindow", "seri_no"))
        self.label_23.setText(_translate("MainWindow", "ad"))
        self.label_24.setText(_translate("MainWindow", "agirlik"))
        self.label_25.setText(_translate("MainWindow", "yapim_yili"))
        self.label_26.setText(_translate("MainWindow", "petrol_kapasite"))
        self.KonteynerEkleButon.setText(_translate("MainWindow", "ONAYLA"))
        self.label.setText(_translate("MainWindow", "seri_no"))
        self.konteynerSeriNoSilButon.setText(_translate("MainWindow", "SIL"))
        self.label_9.setText(_translate("MainWindow", "seri_no"))
        self.petrolSilmeButon.setText(_translate("MainWindow", "SIL"))
        self.petrolEkle.setText(_translate("MainWindow", "ONAYLA"))
        self.label_27.setText(_translate("MainWindow", "kaptan_id"))
        self.label_28.setText(_translate("MainWindow", "kaptan_ad"))
        self.label_29.setText(_translate("MainWindow", "kaptan_soyad"))
        self.label_30.setText(_translate("MainWindow", "kaptan_adres"))
        self.label_31.setText(_translate("MainWindow", "kaptan_vatandaslik"))
        self.label_32.setText(_translate("MainWindow", "kaptan_dogumtarihi"))
        self.label_33.setText(_translate("MainWindow", "kaptan_iseGiris"))
        self.label_34.setText(_translate("MainWindow", "kaptan_lisans"))
        self.kaptanEkleButon.setText(_translate("MainWindow", "ONAYLA"))
        self.label_35.setText(_translate("MainWindow", "kaptan_id"))
        self.kaptanSilmeButon.setText(_translate("MainWindow", "SIL"))
        self.label_36.setText(_translate("MainWindow", "murettabat_id"))
        self.label_37.setText(_translate("MainWindow", "murettabat_ad"))
        self.label_38.setText(_translate("MainWindow", "murettabat_soyad"))
        self.label_39.setText(_translate("MainWindow", "murettabat_adres"))
        self.label_40.setText(_translate("MainWindow", "murettabat_vatandaslik"))
        self.label_41.setText(_translate("MainWindow", "murettabat_dogumtarihi"))
        self.label_42.setText(_translate("MainWindow", "murettabat_gorev"))
        self.label_43.setText(_translate("MainWindow", "murettabat_iseGiris"))
        self.murettebatEKLEBUTON.setText(_translate("MainWindow", "ONAYLA"))
        self.label_44.setText(_translate("MainWindow", "murettabat_id"))
        self.murettebatSilButon.setText(_translate("MainWindow", "SIL"))
        self.label_45.setText(_translate("MainWindow", "liman_adi"))
        self.label_46.setText(_translate("MainWindow", "liman_ulkesi"))
        self.label_47.setText(_translate("MainWindow", "nufus"))
        self.label_48.setText(_translate("MainWindow", "pasaport_sorgu"))
        self.label_49.setText(_translate("MainWindow", "demırleme_ucret"))
        self.limanEkleButon.setText(_translate("MainWindow", "ONAYLA"))
        self.label_50.setText(_translate("MainWindow", "liman_adi"))
        self.limanSilButon.setText(_translate("MainWindow", "SIL"))
        self.label_51.setText(_translate("MainWindow", "sefer_id"))
        self.label_52.setText(_translate("MainWindow", "yola_cikis_tarihi"))
        self.label_53.setText(_translate("MainWindow", "donus_tarihi"))
        self.label_54.setText(_translate("MainWindow", "cikis_limani"))
        self.sefeEkleButon.setText(_translate("MainWindow", "ONAYLA"))
        self.label_55.setText(_translate("MainWindow", "sefer_id"))
        self.seferSILBUTON.setText(_translate("MainWindow", "SIL"))
        self.yolcuGuncelleCheck.setText(_translate("MainWindow", "GUNCELLE"))
        self.yolcuEkleCheck.setText(_translate("MainWindow", "EKLE"))
        self.petrolEkleCheck.setText(_translate("MainWindow", "EKLE"))
        self.petrolGuncelleCheck.setText(_translate("MainWindow", "GUNCELLE"))
        self.murettabatEkleCheck.setText(_translate("MainWindow", "EKLE"))
        self.murettabatGuncelleCheck.setText(_translate("MainWindow", "GUNCELLE"))
        self.limanEkleCheck.setText(_translate("MainWindow", "EKLE"))
        self.limanGuncelleCheck.setText(_translate("MainWindow", "GUNCELLE"))
        self.kaptanEkleCheck.setText(_translate("MainWindow", "EKLE"))
        self.kaptanGuncelleCheck.setText(_translate("MainWindow", "GUNCELLE"))
        self.konteynerEkleCheck.setText(_translate("MainWindow", "EKLE"))
        self.konteynerGuncelleCheck.setText(_translate("MainWindow", "GUNCELLE"))
        self.seferEkleCheck.setText(_translate("MainWindow", "EKLE"))
        self.seferGuncelleCheck.setText(_translate("MainWindow", "GUNCELLE"))
        self.veriTabaniGoster.setText(_translate("MainWindow", "VERITABANI GOSTER"))
        self.label_56.setText(_translate("MainWindow", "SEFER OLUSTUR"))
        self.label_57.setText(_translate("MainWindow", "sefer_id"))
        self.label_58.setText(_translate("MainWindow", "kaptan_id"))
        self.label_59.setText(_translate("MainWindow", "murettabat_id"))
        self.label_60.setText(_translate("MainWindow", "gemi_seri_no"))
        self.label_61.setText(_translate("MainWindow", "gidilecek_liman"))
        self.seferOlusturOnaylaButon.setText(_translate("MainWindow", "ONAYLA"))
        self.seferOlusturEkleC.setText(_translate("MainWindow", "EKLE"))
        self.seferOlusturGuncelleC.setText(_translate("MainWindow", "GUNCELLE"))
        self.label_62.setText(_translate("MainWindow", "SEFER SIL"))
        self.label_63.setText(_translate("MainWindow", "sefer_id"))
        self.seferOlusturSilmeButon.setText(_translate("MainWindow", "SIL"))


class SecondWindow(QtWidgets.QMainWindow):

    def tablo_guncelleyici(self):
        yolcuverisi=yolcutable.listele()
        if yolcuverisi !=[]:
            
            for row_index,row_data in enumerate(yolcuverisi):
                
                self.yolcuGemisiVeriTabani.insertRow(self.yolcuGemisiVeriTabani.rowCount())
                for column_index,veri in enumerate(row_data):
                    item=QTableWidgetItem(str(veri))
                    self.yolcuGemisiVeriTabani.setItem(row_index,column_index,item)

        konteynerG=konteynertable.listele()
        if konteynerG !=[]:
            
            for row_index,row_data in enumerate(konteynerG):
                
                self.konteynerGVeritabani.insertRow(self.konteynerGVeritabani.rowCount())
                for column_index,veri in enumerate(row_data):
                    item=QTableWidgetItem(str(veri))
                    self.konteynerGVeritabani.setItem(row_index,column_index,item)

        petrolG=petroltable.listele()
        if petrolG !=[]:
            
            for row_index,row_data in enumerate(petrolG):
                
                self.petrolGemisiVeritabani.insertRow(self.petrolGemisiVeritabani.rowCount())
                for column_index,veri in enumerate(row_data):
                    item=QTableWidgetItem(str(veri))
                    self.petrolGemisiVeritabani.setItem(row_index,column_index,item)

        seferT=sefertable.listele()
        if seferT !=[]:
            
            for row_index,row_data in enumerate(seferT):
                
                self.seferlerVeritabani.insertRow(self.seferlerVeritabani.rowCount())
                for column_index,veri in enumerate(row_data):
                    item=QTableWidgetItem(str(veri))
                    self.seferlerVeritabani.setItem(row_index,column_index,item)

        limanT=limantable.listele()
        if limanT !=[]:
            
            for row_index,row_data in enumerate(limanT):
                
                self.limanVeritabani.insertRow(self.limanVeritabani.rowCount())
                for column_index,veri in enumerate(row_data):
                    item=QTableWidgetItem(str(veri))
                    self.limanVeritabani.setItem(row_index,column_index,item)

        kaptanT=kaptantable.listele()
        if kaptanT !=[]:
            
            for row_index,row_data in enumerate(kaptanT):
                
                self.kaptanVeritabani.insertRow(self.kaptanVeritabani.rowCount())
                for column_index,veri in enumerate(row_data):
                    item=QTableWidgetItem(str(veri))
                    self.kaptanVeritabani.setItem(row_index,column_index,item)

        murettebatT=murettebattable.listele()
        if murettebatT !=[]:
            
            for row_index,row_data in enumerate(murettebatT):
                
                self.murettebatVeritabani.insertRow(self.murettebatVeritabani.rowCount())
                for column_index,veri in enumerate(row_data):
                    item=QTableWidgetItem(str(veri))
                    self.murettebatVeritabani.setItem(row_index,column_index,item)

        seferOlusturT = seferekletable.listele()
        if seferOlusturT !=[]:
            
            for row_index,row_data in enumerate(seferOlusturT):
                
                self.seferOlusturVeritabani.insertRow(self.seferOlusturVeritabani.rowCount())
                for column_index,veri in enumerate(row_data):
                    item=QTableWidgetItem(str(veri))
                    self.seferOlusturVeritabani.setItem(row_index,column_index,item)


    def kontrolArayuzu_clicked(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        
        
        
    def __init__(self):
        super().__init__()
             
        MainWindow.resize(1025, 835)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, -40, 851, 131))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.yolcuGemisiVeriTabani = QtWidgets.QTableWidget(self.centralwidget)
        self.yolcuGemisiVeriTabani.setGeometry(QtCore.QRect(30, 90, 301, 192))
        self.yolcuGemisiVeriTabani.setObjectName("yolcuGemisiVeriTabani")
        self.yolcuGemisiVeriTabani.setColumnCount(5)
        self.yolcuGemisiVeriTabani.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.yolcuGemisiVeriTabani.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.yolcuGemisiVeriTabani.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.yolcuGemisiVeriTabani.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.yolcuGemisiVeriTabani.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.yolcuGemisiVeriTabani.setHorizontalHeaderItem(4, item)
        self.konteynerGVeritabani = QtWidgets.QTableWidget(self.centralwidget)
        self.konteynerGVeritabani.setGeometry(QtCore.QRect(360, 90, 291, 192))
        self.konteynerGVeritabani.setObjectName("konteynerGVeritabani")
        self.konteynerGVeritabani.setColumnCount(6)
        self.konteynerGVeritabani.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.konteynerGVeritabani.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.konteynerGVeritabani.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.konteynerGVeritabani.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.konteynerGVeritabani.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.konteynerGVeritabani.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.konteynerGVeritabani.setHorizontalHeaderItem(5, item)
        self.petrolGemisiVeritabani = QtWidgets.QTableWidget(self.centralwidget)
        self.petrolGemisiVeritabani.setGeometry(QtCore.QRect(690, 90, 291, 192))
        self.petrolGemisiVeritabani.setObjectName("petrolGemisiVeritabani")
        self.petrolGemisiVeritabani.setColumnCount(5)
        self.petrolGemisiVeritabani.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.petrolGemisiVeritabani.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.petrolGemisiVeritabani.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.petrolGemisiVeritabani.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.petrolGemisiVeritabani.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.petrolGemisiVeritabani.setHorizontalHeaderItem(4, item)
        self.kaptanVeritabani = QtWidgets.QTableWidget(self.centralwidget)
        self.kaptanVeritabani.setGeometry(QtCore.QRect(30, 340, 301, 192))
        self.kaptanVeritabani.setObjectName("kaptanVeritabani")
        self.kaptanVeritabani.setColumnCount(8)
        self.kaptanVeritabani.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.kaptanVeritabani.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptanVeritabani.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptanVeritabani.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptanVeritabani.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptanVeritabani.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptanVeritabani.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptanVeritabani.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.kaptanVeritabani.setHorizontalHeaderItem(7, item)
        self.seferlerVeritabani = QtWidgets.QTableWidget(self.centralwidget)
        self.seferlerVeritabani.setGeometry(QtCore.QRect(360, 340, 291, 192))
        self.seferlerVeritabani.setObjectName("seferlerVeritabani")
        self.seferlerVeritabani.setColumnCount(4)
        self.seferlerVeritabani.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.seferlerVeritabani.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.seferlerVeritabani.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.seferlerVeritabani.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.seferlerVeritabani.setHorizontalHeaderItem(3, item)
        self.murettebatVeritabani = QtWidgets.QTableWidget(self.centralwidget)
        self.murettebatVeritabani.setGeometry(QtCore.QRect(690, 340, 291, 192))
        self.murettebatVeritabani.setObjectName("murettebatVeritabani")
        self.murettebatVeritabani.setColumnCount(9)
        self.murettebatVeritabani.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.murettebatVeritabani.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.murettebatVeritabani.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.murettebatVeritabani.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.murettebatVeritabani.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.murettebatVeritabani.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.murettebatVeritabani.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.murettebatVeritabani.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.murettebatVeritabani.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.murettebatVeritabani.setHorizontalHeaderItem(8, item)
        self.limanVeritabani = QtWidgets.QTableWidget(self.centralwidget)
        self.limanVeritabani.setGeometry(QtCore.QRect(360, 600, 291, 192))
        self.limanVeritabani.setObjectName("limanVeritabani")
        self.limanVeritabani.setColumnCount(5)
        self.limanVeritabani.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.limanVeritabani.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.limanVeritabani.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.limanVeritabani.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.limanVeritabani.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.limanVeritabani.setHorizontalHeaderItem(4, item)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 60, 121, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(440, 60, 101, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(770, 60, 111, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(120, 310, 91, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(450, 310, 91, 20))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(780, 310, 111, 20))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(450, 570, 101, 20))
        self.label_8.setObjectName("label_8")

        self.kontrolArayuzu = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.kontrolArayuzu.setGeometry(QtCore.QRect(70, 650, 185, 41))
        self.kontrolArayuzu.setObjectName("kontrolArayuzu")
        self.kontrolArayuzu.clicked.connect(self.kontrolArayuzu_clicked)

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(800, 570, 141, 20))
        self.label_9.setObjectName("label_9")
        self.seferOlusturVeritabani = QtWidgets.QTableWidget(self.centralwidget)
        self.seferOlusturVeritabani.setGeometry(QtCore.QRect(690, 600, 291, 192))
        self.seferOlusturVeritabani.setObjectName("seferOlusturVeritabani")
        self.seferOlusturVeritabani.setColumnCount(5)
        self.seferOlusturVeritabani.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.seferOlusturVeritabani.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.seferOlusturVeritabani.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.seferOlusturVeritabani.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.seferOlusturVeritabani.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.seferOlusturVeritabani.setHorizontalHeaderItem(4, item)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tablo_guncelleyici()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VERITABANI BILGI"))
        self.label.setText(_translate("MainWindow", "                                                                 VERITABANI BILGI"))
        item = self.yolcuGemisiVeriTabani.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "seri_no"))
        item = self.yolcuGemisiVeriTabani.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ad"))
        item = self.yolcuGemisiVeriTabani.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "agirlik"))
        item = self.yolcuGemisiVeriTabani.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "yapim_yili"))
        item = self.yolcuGemisiVeriTabani.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "yolcu_kapasitesi"))
        item = self.konteynerGVeritabani.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "seri_no"))
        item = self.konteynerGVeritabani.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ad"))
        item = self.konteynerGVeritabani.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "agirlik"))
        item = self.konteynerGVeritabani.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "yapim_yili"))
        item = self.konteynerGVeritabani.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "konteyner_sayisi"))
        item = self.konteynerGVeritabani.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "maks_agirlik"))
        item = self.petrolGemisiVeritabani.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "seri_no"))
        item = self.petrolGemisiVeritabani.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ad"))
        item = self.petrolGemisiVeritabani.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "agirlik"))
        item = self.petrolGemisiVeritabani.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "yapim_yili"))
        item = self.petrolGemisiVeritabani.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "petrol_kapasite"))
        item = self.kaptanVeritabani.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "kaptan_id"))
        item = self.kaptanVeritabani.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "kaptan_ad"))
        item = self.kaptanVeritabani.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "kaptan_soyad"))
        item = self.kaptanVeritabani.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "kaptan_adres"))
        item = self.kaptanVeritabani.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "kaptan_vatandaslik"))
        item = self.kaptanVeritabani.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "kaptan_dogum_tarihi"))
        item = self.kaptanVeritabani.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "kaptan_iseGiris"))
        item = self.kaptanVeritabani.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "kaptan_lisans"))
        item = self.seferlerVeritabani.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "sefer_id"))
        item = self.seferlerVeritabani.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "yola_cikis_tarihi"))
        item = self.seferlerVeritabani.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "donus_tarihi"))
        item = self.seferlerVeritabani.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "cikis_limani"))
        item = self.murettebatVeritabani.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "murettebat_id"))
        item = self.murettebatVeritabani.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "murettebat_ad"))
        item = self.murettebatVeritabani.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "murettebat_soyad"))
        item = self.murettebatVeritabani.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "murettebat_adres"))
        item = self.murettebatVeritabani.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "murettebat_adres"))
        item = self.murettebatVeritabani.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "murettebat_vatandaslik"))
        item = self.murettebatVeritabani.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "murettebat_dogum_tarihi"))
        item = self.murettebatVeritabani.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "murettebat_gorev"))
        item = self.murettebatVeritabani.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "murettebat_iseGiris"))
        item = self.limanVeritabani.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "liman_adi"))
        item = self.limanVeritabani.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "liman_ulkesi"))
        item = self.limanVeritabani.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "nufus"))
        item = self.limanVeritabani.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "pasaport_sorgu"))
        item = self.limanVeritabani.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "demirleme_ucret"))
        self.label_2.setText(_translate("MainWindow", "YOLCU GEMİSİ"))
        self.label_3.setText(_translate("MainWindow", "KONTEYNER GEMİSİ"))
        self.label_4.setText(_translate("MainWindow", "PETROL GEMİSİ"))
        self.label_5.setText(_translate("MainWindow", "KAPTANLAR"))
        self.label_6.setText(_translate("MainWindow", "SEFERLER"))
        self.label_7.setText(_translate("MainWindow", "MURETTEBAT"))
        self.label_8.setText(_translate("MainWindow", "LIMANLAR"))
        self.kontrolArayuzu.setText(_translate("MainWindow", "KONTROL ARAYUZU"))
        self.label_9.setText(_translate("MainWindow", "SEFER OLUSTUR"))
        item = self.seferOlusturVeritabani.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "sefer_id"))
        item = self.seferOlusturVeritabani.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "kaptan_id"))
        item = self.seferOlusturVeritabani.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "murettabat_id"))
        item = self.seferOlusturVeritabani.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "gemi_seri_no"))
        item = self.seferOlusturVeritabani.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "gidilecek_liman"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
