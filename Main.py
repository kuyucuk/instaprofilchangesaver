import urllib.request
import bs4 as bs
import datetime
import openpyxl
import difflib
import smtplib
from openpyxl import Workbook

sauce = urllib.request.urlopen('https://www.instagram.com/tlgkyck').read()
soup = bs.BeautifulSoup(sauce,'lxml')

titledata=soup.title
titletext=titledata.text

try: #kayıtlı data varsa çek
    kitap = openpyxl.load_workbook('insta.xlsx')
    sayfa = kitap.worksheets[0]

except IOError as e: #kayıtlı data yoksa oluştur
    kitap = Workbook()
    sayfa = kitap.active
    kitap.save("insta.xlsx")

A1_verisi = sayfa['A1'].value #başlangıç verisi
Z1_verisi = sayfa['Z1'].value #son veri yedeği

text1_lines=titletext.splitlines()
text2_lines=Z1_verisi.splitlines()

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
print('\n'.join(diff))

if (A1_verisi == None or Z1_verisi == None): #sütunlar boşsa başlangıç verilerini ekle
    sayfa['A1'] = sayfa['Z1'] = str(titletext)
    sayfa['K1'] = datetime.datetime.now()
    print("Profil ismi işlenmiştir:")
    print(titletext)

else:
    if (Z1_verisi == titletext):
        print('Değişiklik yoktur')
    else:
        sayfa.append({'A': titletext, 'K': datetime.datetime.now()})

    sayfa['Z1'] = str(titletext)
    print(str(titletext))

kitap.save("insta.xlsx")
kitap.close()

#####################################################################################

# Hesap bilgilerimiz
kullanıcı = "mail@gmail.com"
kullanıcı_sifresi = 'şifre'

alıcı = 'mail'  # alıcının mail adresi
konu = 'Selam'
msj = titletext.encode('utf-8')

# bilgileri bir metinde derledik
email_text = """
From: {}
To: {}
Subject: {}
{}
""".format(kullanıcı, alıcı, konu, msj)

try:
    server = smtplib.SMTP('smtp.gmail.com:587')  # servere bağlanmak için gerekli host ve portu belirttik

    server.starttls()  # serveri TLS(bütün bağlantı şifreli olucak bilgiler korunucak) bağlantısı ile başlattık

    server.login(kullanıcı, kullanıcı_sifresi)  # Gmail SMTP server'ına giriş yaptık

    server.sendmail(kullanıcı, alıcı, email_text)  # Mail'imizi gönderdik

    server.close()  # SMTP serverimizi kapattık

    print('email gönderildi')

except:
    print("bir hata oluştu")
