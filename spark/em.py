#!/usr/bin/env python
"recive content email."
import re
import poplib
import email


class vpsMailContent():

        """fetch vps content links"""

        def __init__(self,
                     emailserver="pop.gmail.com",
                     username="",
                     passwd=""):
            """ init """
            self.emailserver = emailserver
            self.username = username
            self.passwd = passwd
            self.sp = None
            self.mailcount = 0
            self.totalsize = 0
            self.mailheader = ""
            self.mailContent = ""

        def _connect(self):
                self.sp = poplib.POP3_SSL(self.emailserver)
                self.sp.user(self.username)
                self.sp.pass_(self.passwd)
                self.sp.set_debuglevel(1)

                (self.mailcount, self.totalsize) = self.sp.stat()
                if self.mailcount > 0:
                        (self.mailheader,
                         self.mailContent, oct) = self.sp.retr(self.mailcount)
                self.sp.quit()

        def vpsresult(self):
                self._connect()
                if len(self.mailContent) > 10:
                        return "\n".join(self.mailContent)
                return ""


def mail_main():
    """ pop3 recive email"""

    s = 'pop.gmail.com'
    u = 'youremailfeedfromvpngate@gmail.com'
    p = 'youemailpass'

    cont = vpsMailContent(s, u, p).vpsresult()

    file_object = open('tmp.txt', 'w+')
    file_object.writelines(cont)
    file_object.close()
    print "done"

    message = email.message_from_string(cont)

    subject = message.get("subject")
    h = email.Header.Header(subject)
    dh = email.Header.decode_header(h)
    subject = dh[0][0]
    print "subject:", subject
    print "from: ", email.utils.parseaddr(message.get("from"))[1]
    print "to: ", email.utils.parseaddr(message.get("to"))[1]

    link = []
    for c in message.walk():
            payload = c.get_payload(decode=True)
            link = re.findall(r"http.*?\:[0-9]{3,5}\/", str(payload))
    return link


if __name__ == '__main__':
    lk = mail_main()
    print '\n'.join(lk)


