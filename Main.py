import urllib.request
import bs4 as bs
import datetime
import openpyxl
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

if (A1_verisi == None or Z1_verisi == None): #sütunlar boşsa verileri ekle
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
