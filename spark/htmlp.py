#-*- encoding:utf-8 -*-
#!/usr/bin/env python

'''
handle_startendtag  处理开始标签和结束标签
handle_starttag     处理开始标签，比如<xx>
handle_endtag       处理结束标签，比如</xx>
handle_charref      处理特殊字符串，就是以&#开头的，一般是内码表示的字符
handle_entityref    处理一些特殊字符，以&开头的，比如 &nbsp;
handle_data         处理数据，就是<xx>data</xx>中间的那些数据
handle_comment      处理注释
handle_decl         处理<!开头的，比如<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
handle_pi           处理形如<?instruction>的东西
'''


import HTMLParser
import urllib2
import json


from  im  import  mail_main


class tinyhtmlparser(HTMLParser.HTMLParser):
    """redefine htmlparser for page"""
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.staticlist = []
        self.contentlist = []
        self.tmplist = []
        self.trigger = False
        self.trcyc = False
        self.tmpstr = ""
        self.feildtrig = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td' and self.trigger and self.trcyc:
            self.feildtrig = True
        if tag == 'table':
            for k, v in attrs:
                if k == 'id' and v == 'vg_hosts_table_id':
                    self.trigger = True

        if self.trigger is True and tag == 'tr':
            self.trcyc = True

    def handle_endtag(self, tag):
        if self.trigger and self.trcyc and self.feildtrig and tag == 'td':
            self.feildtrig = False
            # self.tmpstr += "\n"
            self.tmplist.append(self.tmpstr)
            self.tmpstr = ""

        if self.trigger is True and tag == 'tr' and self.trcyc is True:
            self.trcyc = False
            self.contentlist.append(self.tmplist)
            self.tmplist = []

        if tag == 'table' and self.trigger is True:
            self.trigger = False
            self.staticlist.append(self.contentlist)
            self.contentlist = []

    def handle_data(self, data):
        if self.trigger is True and self.trcyc is True and self.feildtrig:
            # print "-----", data,"====="
            if len(self.tmpstr) == 0:
                self.tmpstr += data
            else:
                self.tmpstr += " "
                self.tmpstr += data

    def result(self, type=2):
        '''
                type = 0 : Recent VPN activity logs around the world (12,796 entries)
                type = 1 : VPN Gate User Countries Realtime Ranking
                type = 2 : Public VPN Relay Servers by volunteers around the world.
        '''
        if type == 0:
            return self.staticlist[0]
        elif type == 1:
            return self.staticlist[1]

        return self.staticlist[2]


def comps(list):
    res = []
    msg = ""
    if len(list) < 8:
        return list

    for it in list:
        if it == '\r\n':
            if len(msg) > 0:
                res.append(msg)
                msg = ""
        else:
            msg += it
    return res


def parser_url_data(data):
    try:
        pr = tinyhtmlparser()
        pr.feed(data)

        keykey = {
            "SSL-VPN Windows (comfortable)": "conn_supported",
            "Volunteer operator's name (+ Operator's message)": "operator",
            "OpenVPN Windows, Mac, iPhone, Android": "openvpn_config",
            "VPN sessions Uptime Cumulative users": "vpn_conn_info",
            "DDNS hostname IP Address (ISP hostname)": "ip_addr",
            "Score (Quality)": "quality",
            "L2TP/IPsec Windows, Mac, iPhone, Android No client required": "platform_no_req",
            "MS-SSTP Windows Vista, 7, 8, RT No client required": "win_no_req",
            "Country (Physical location)": "country",
            "Line quality Throughput and Ping Cumulative transfers Logging policy": "performance"
        }
        li = pr.result()
        cp = li[0]
        content = []
        for x in xrange(1, len(li)):
            dic = {}
            if li[x][1][0] == 'D':
                continue
            for idx, it in enumerate(li[x]):
                dip = {}
                if idx == 1:
                    if len(it) > 22:
                        lip = it.split(' ')
                        dip['ip'] = lip[0]
                        dip['host'] = lip[1].lstrip('(').rstrip(')')
                    else:
                        dip['ip'] = it
                    dic[keykey[li[0][idx]]] = dip
                else:
                    dic[keykey[li[0][idx]]] = it
            content.append(dic)
        return content
    except Exception as e:
        return e


def parser_url(url):
    if not url:
        return
    return parser_url_data(urllib2.urlopen(url).read())


if __name__ == '__main__':
    " test wrap."
    # f = open("./j.html", "r")
    # data = f.read()
    # f.close()

    data = urllib2.urlopen('http://i121-116-40-52.s05.a013.ap.plala.or.jp:29785/').read()

    lst = parser_url_data(data)

    file = open("./rst.json", 'w')
    file.writelines(json.dumps(lst))
    file.close()

