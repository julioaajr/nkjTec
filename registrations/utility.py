from datetime import *
import smtplib
from email.mime.text import MIMEText
from datetime import timedelta


class Time:

    def convertweekday(self,dates):
        dates = dates.split("/")
        dates = datetime(int(dates[2]),int(dates[1]),int(dates[0]))
        return (dates.weekday())

    def convertehora(self, hora):
        return  (timedelta(hours=int(hora[0:2]), minutes=int(hora[3:])))

    
    #schedule espera um dict com begin end e interval e busy espera uma lista
    def FreeSchedule(self,beginx,endx,intervalx,busy):
        begin = timedelta(hours=int(beginx.split(':')[0]),minutes=int(beginx.split(':')[1]))
        end = timedelta(hours=int(endx.split(':')[0]),minutes=int(endx.split(':')[1]))
        interval = timedelta(minutes= int(intervalx))
        free = []
        busylist = []
        for i in busy:
            busylist.append(timedelta(hours = int(i.split(":")[0]), minutes= int(i.split(":")[1])))
        while begin <= end:
            if begin not in busylist:
                aux = str(begin).split(':')[0]+":"+str(begin).split(':')[1]
                if len(aux) == 4:
                    aux = "0"+aux
                free.append(aux)
            begin+=interval
        return (free)

class Emails:
    #3 strings email assunto e conteudo
    def sendmails(self, receiver, subject, content):
        fromx = 'barbeariaebenezerlondrina@gmail.com'
        pwd = 'barbershop'
        to  = receiver
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = fromx
        msg['To'] = to
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.ehlo()
        try:
            server.login(fromx, pwd)
            server.sendmail(fromx, to, msg.as_string())
            server.quit()
            return(True)
        except:
            return (False)


class Users:
    def selfuser(self,id):
        pass


beginx='08:00'
endx='18:00'
intervalx='60'
busyx = ['15:00', '09:00', '18:00']

print(Time().FreeSchedule(beginx,endx,intervalx,busyx))