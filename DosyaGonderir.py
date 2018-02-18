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

sauce = urllib.request.urlopen('https://www.instagram.com/tlgkyck').read()
soup = bs.BeautifulSoup(sauce,'lxml')

titledata=soup.title
titletext=titledata.text

file = "insta.xlsx"

try: #kayıtlı data varsa çek
    kitap = openpyxl.load_workbook(file)
    sayfa = kitap.worksheets[0]

except IOError as e: #kayıtlı data yoksa oluştur
    kitap = Workbook()
    sayfa = kitap.active
    kitap.save(file)

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

    kitap.save(file)
    kitap.close()

else:
    if (Z1_verisi == titletext):
        print('Değişiklik yoktur')
    else:
        sayfa.append({'A': titletext, 'K': datetime.datetime.now()})

        sayfa['Z1'] = str(titletext)

        kitap.save(file)
        kitap.close()

        try:
            recipients = ['tolga_k94@hotmail.com']
            emaillist = [elem.strip().split(',') for elem in recipients]

            msg = MIMEMultipart()
            msg['Subject'] = str(file)
            msg['From'] = 'usertolga@gmail.com'
            msg['Reply-to'] = 'tolga_k94@hotmail.com'
            msg.preamble = 'Multipart massage.\n'

            part = MIMEText("Profil adı değişti!")
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