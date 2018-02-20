import urllib.request
import bs4 as bs
import datetime
import openpyxl
import difflib
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from openpyxl import Workbook

#webLink = input("Link giriniz: ")
#sendMail= input("Mail adresinizi giriniz: ")

kaynak= int(input("Taranmasını istediğiniz kaynağı seçiniz.\n(1) title\n(2) h1\n(3) h2\n(4) body\n--> "))

webLink= 'https://ubersem.com/'
sendMail= 'tolga_k94@hotmail.com'

sauce = urllib.request.urlopen(webLink.strip()).read()
soup = bs.BeautifulSoup(sauce,'lxml')


try:
    titledata = soup.title
    titletext = titledata.text

    h1data = soup.h1
    h1text = h1data.text

    h2data = soup.h2
    h2text = h2data.text

    bodydata = soup.body
    bodytext = bodydata.text
except:
    print("Bu URL, girilen datalara ulaşılmasına izin vermiyor.")



if (kaynak == 1):
    data = titletext
    dataAdi = "title"
elif (kaynak == 2):
    data = h1text
    dataAdi = "h1"
elif (kaynak == 3):
    data = h2text
    dataAdi = "h2"
elif (kaynak == 4):
    data = bodytext
    dataAdi = "body"

print(type(soup.h1))
print(data)

file = str(dataAdi+"DataBase.xlsx")

def mailGonder (text):
    try:
        recipients = [sendMail]  # değişim varsa mail gönder
        emaillist = [elem.strip().split(',') for elem in recipients]

        msg = MIMEMultipart()
        msg['Subject'] = str(file)
        msg['From'] = 'usertolga@gmail.com'
        msg['Reply-to'] = sendMail
        msg.preamble = 'Multipart massage.\n'

        part = MIMEText(text)
        msg.attach(part)

        part = MIMEApplication(open(file, "rb").read())
        part.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login("usertolga@gmail.com", "gmailsifresi")

        server.sendmail(msg['From'], emaillist, msg.as_string())

        print("Mail gönderilmiştir")

    except:
        print("bir hata oluştu")

try: #kayıtlı data varsa çek
    kitap = openpyxl.load_workbook(file)
    sayfa = kitap.worksheets[0]

except IOError as e: #kayıtlı data yoksa oluştur
    kitap = Workbook()
    sayfa = kitap.active
    kitap.save(file)

C1_verisi = sayfa['C1'].value #başlangıç verisi
Z1_verisi = sayfa['Z1'].value #son veri yedeği

if (C1_verisi == None or Z1_verisi == None): #sütunlar boşsa başlangıç verilerini ekle
    sayfa['C1'] = sayfa['Z1'] = str(data)
    sayfa['A1'] = datetime.datetime.now()
    textPI= "Veri dosyası oluşturulmuş ve ilk veri işlenmiştir!"
    print(data)

    kitap.save(file)
    kitap.close()

    mailGonder(textPI)
else:
    if (Z1_verisi == data):
        print('Değişiklik yoktur')
    else:
        textPD = "Veri değişikliği algılandı"
        sayfa.append({'C': data, 'A': datetime.datetime.now()})

        sayfa['Z1'] = str(data)

        text1_lines = data.splitlines()
        text2_lines = Z1_verisi.splitlines()

        d = difflib.Differ()
        diff = d.compare(text1_lines, text2_lines)
        print('\n'.join(diff))

        kitap.save(file)
        kitap.close()

        mailGonder(textPD)