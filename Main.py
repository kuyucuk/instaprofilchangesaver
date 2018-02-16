import urllib.request
import bs4 as bs
import datetime
import difflib
import openpyxl
from openpyxl import Workbook


sauce = urllib.request.urlopen('https://www.instagram.com/tlgkyck').read()
soup = bs.BeautifulSoup(sauce,'lxml')

h1data=soup.title
h1text=h1data.text

try: #kayıtlı data varsa çek
    kitap = openpyxl.load_workbook('insta.xlsx')
    sayfa = kitap.worksheets[0]

except IOError as e: #kayıtlı data yoksa oluştur
    kitap = Workbook()
    sayfa = kitap.active
    kitap.save("insta.xlsx")

A1_verisi = sayfa['A1'].value
P1_verisi = sayfa['P1'].value

if (A1_verisi == None or P1_verisi == None): #sütunlar boşsa verileri ekle
    sayfa['A1'] = sayfa['P1'] = str(h1text)
    print("Profil ismi işlenmiştir:")
    print(h1text)

else:

    if (P1_verisi == h1text):
        print('Değişiklik yoktur')
    else:
        sayfa.append([h1text])

    sayfa['P1'] = str(h1text)
    print(str(h1text))





kitap.save("insta.xlsx")
kitap.close()