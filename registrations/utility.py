from datetime import *
import smtplib
from email.mime.text import MIMEText
from datetime import timedelta, datetime
from decouple import config

class Time:

    def convertweekday(self,dates):
        dates = dates.split("/")
        dates = datetime(int(dates[2]),int(dates[1]),int(dates[0]))
        return (dates.weekday())

    #converte a data de yyyy-mm-dd para dd/mm/aaaa
    def convertdate(self,dates):
        dates = dates.split("-")
        return (f"{dates[2]}/{dates[1]}/{dates[0]}")

    def convertdateBRtoUS(self,dates):
        dates = dates.split("/")
        return datetime(int(dates[2]),int(dates[1]),int(dates[0]))
    

    def convertehora(self, hora):
        return  (timedelta(hours=int(hora[0:2]), minutes=int(hora[3:])))

    #schedule = dict(begin='08:00', end='18:00', interval='60')    #busy = ['15:00', '09:00', '18:00']
    #schedule espera um dict com begin end e interval e busy espera uma lista
    def FreeSchedule(self,schedule,busy):
        begin = timedelta(hours=int(schedule.begin.split(':')[0]),minutes=int(schedule.begin.split(':')[1]))
        end = timedelta(hours=int(schedule.end.split(':')[0]),minutes=int(schedule.end.split(':')[1]))
        interval = timedelta(minutes= int(schedule.interval))
        free = []
        busylist = []
        for i in busy:
            busylist.append(timedelta(hours = int(i.apphour.split(":")[0]), minutes= int(i.apphour.split(":")[1])))
        while begin <= end:
            if begin not in busylist:
                aux = str(begin).split(':')[0]+":"+str(begin).split(':')[1]
                if len(aux) == 4:
                    aux = "0"+aux
                free.append(aux)
            begin+=interval
        for app in busy:
            beginTD = timedelta(hours= app.appbegin.hour,minutes= app.appbegin.minute)
            endTD = timedelta(hours= app.append.hour,minutes= app.append.minute)
            for horarios in free[:]:
                freeTD = timedelta(hours= int(horarios.split(':')[0]), minutes= int(horarios.split(':')[1]))
                if(freeTD > beginTD and freeTD < endTD):
                    free.remove(horarios)
        return (free)



class Emails:
    #3 strings email assunto e conteudo
    def sendmails(self, receiver, subject, content):
        fromx = config('fromx')
        pwd =config('pwd')
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


