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

try:
    kitap = openpyxl.load_workbook('insta.xlsx')
    sayfa = kitap.get_sheet_by_name('Sheet')

    print(sayfa)

    A1_verisi = sayfa['A1'].value
    P1_verisi = sayfa['P1'].value

    if (A1_verisi == None or P1_verisi == None):
        sayfa['A1'] = sayfa['P1'] = str(h1text)
        print("Profil isminiz işlenmiştir:")
        print(h1text)

    else:
        cell = sayfa['P1'].value
        print(cell)

        if (cell == h1text):
            print('Değişiklik yoktur')
        else:
            sayfa.append([h1text])

        sayfa['P1'] = str(h1text)
        print(str(h1text))
except IOError as e:
    print("Kayıt datanız oluşturuldu, lütfen tekrar derleyiniz")
    kitap = Workbook()
    sayfa = kitap.active
    kitap.save("insta.xlsx")
except ValueError:
    print("h")







kitap.save("insta.xlsx")
kitap.close()